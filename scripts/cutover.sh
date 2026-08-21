#!/usr/bin/env bash
# =============================================================================
# connectomelab.com cutover: Google Sites -> GitHub Pages (new Astro site)
#
# Usage:
#   ./scripts/cutover.sh            # run the cutover (interactive)
#   ./scripts/cutover.sh --status   # just show where things stand
#   ./scripts/cutover.sh --rollback-help
#
# What it does:
#   Step 1  Sets the GitHub Pages custom domain to www.connectomelab.com
#           (runs as YOU via `gh`; fully automatic)
#   Step 2  DNS at Namecheap: prints the exact one-record change to make.
#           If NAMECHEAP_API_USER / NAMECHEAP_API_KEY / NAMECHEAP_CLIENT_IP are
#           all set (API access pre-enabled on your Namecheap account), it can
#           apply the change automatically — after backing up current records.
#   Step 3  Verifies everything end-to-end: DNS propagation, GitHub domain
#           check, HTTPS certificate, then enforces HTTPS and confirms the new
#           site is actually being served.
#
# Rollback = one DNS change back (see --rollback-help). The old Google Site
# keeps serving until the instant DNS flips; there is no downtime window.
# =============================================================================
set -euo pipefail

REPO="Transconnectome/lab-homepage"
DOMAIN="www.connectomelab.com"
PAGES_HOST="snuconnectome.github.io"
MARKER="Six networks, one lab"   # unique to the NEW site (the da Vinci quote also existed on the old Google Site)

say()  { printf '\n\033[1;36m▸ %s\033[0m\n' "$*"; }
ok()   { printf '\033[1;32m  ✓ %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m  ! %s\033[0m\n' "$*"; }
die()  { printf '\033[1;31m  ✗ %s\033[0m\n' "$*"; exit 1; }

current_cname() { dig +short CNAME "$DOMAIN" | sed 's/\.$//' | head -1; }

pages_json() { gh api "repos/$REPO/pages" 2>/dev/null || echo '{}'; }

show_status() {
  say "Current status"
  echo "  DNS  $DOMAIN CNAME -> $(current_cname || echo '(none)')"
  local pj; pj=$(pages_json)
  echo "  GitHub Pages custom domain: $(echo "$pj" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d.get("cname") or "(not set)")')"
  echo "  HTTPS enforced:             $(echo "$pj" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("https_enforced"))')"
  if curl -sfm 10 "https://$DOMAIN" 2>/dev/null | grep -q "$MARKER"; then
    ok "https://$DOMAIN is serving the NEW site"
  else
    warn "https://$DOMAIN is still the old site (or unreachable over HTTPS)"
  fi
}

rollback_help() {
  cat <<EOF

ROLLBACK (restores the old Google Site immediately):
  Namecheap → Domain List → connectomelab.com → Advanced DNS →
  edit the 'www' CNAME record back to:  ghs.googlehosted.com
  (Optionally also clear the GitHub Pages custom domain:
   gh api repos/$REPO/pages -X PUT -F cname=)

EOF
}

case "${1:-}" in
  --status)        show_status; exit 0 ;;
  --rollback-help) rollback_help; exit 0 ;;
esac

# ---------------------------------------------------------------- preflight --
say "Preflight"
command -v gh  >/dev/null || die "gh CLI not found"
command -v dig >/dev/null || die "dig not found (apt install dnsutils)"
gh auth status >/dev/null 2>&1 || die "gh is not authenticated (run: gh auth login)"
ok "gh authenticated as $(gh api user -q .login)"
echo "  DNS today: $DOMAIN -> $(current_cname || echo '(none)')"

# ------------------------------------------------- Step 1: Pages custom domain
say "Step 1/3 — Set GitHub Pages custom domain to $DOMAIN"
CUR_CNAME_CFG=$(pages_json | python3 -c 'import json,sys;print(json.load(sys.stdin).get("cname") or "")')
if [ "$CUR_CNAME_CFG" = "$DOMAIN" ]; then
  ok "already set"
else
  gh api "repos/$REPO/pages" -X PUT -f "cname=$DOMAIN" >/dev/null
  ok "custom domain set on $REPO"
fi

# --------------------------------------------------------- Step 2: DNS switch
say "Step 2/3 — Point DNS at GitHub Pages"
if [ "$(current_cname)" = "$PAGES_HOST" ]; then
  ok "DNS already points to $PAGES_HOST — skipping"
elif [ -n "${NAMECHEAP_API_USER:-}" ] && [ -n "${NAMECHEAP_API_KEY:-}" ] && [ -n "${NAMECHEAP_CLIENT_IP:-}" ]; then
  warn "Namecheap API credentials detected — applying the change automatically."
  warn "A full backup of current DNS records will be written first."
  python3 - "$PAGES_HOST" <<'PYEOF'
import os, sys, urllib.request, urllib.parse, xml.etree.ElementTree as ET, json, datetime

target = sys.argv[1]
sld, tld = "connectomelab", "com"
base = "https://api.namecheap.com/xml.response"
common = {
    "ApiUser": os.environ["NAMECHEAP_API_USER"],
    "ApiKey": os.environ["NAMECHEAP_API_KEY"],
    "UserName": os.environ["NAMECHEAP_API_USER"],
    "ClientIp": os.environ["NAMECHEAP_CLIENT_IP"],
}
NS = {"nc": "http://api.namecheap.com/xml.response"}

def call(params):
    url = base + "?" + urllib.parse.urlencode({**common, **params})
    with urllib.request.urlopen(url, timeout=30) as r:
        root = ET.fromstring(r.read())
    if root.get("Status") != "OK":
        errs = [e.text for e in root.iter() if e.tag.endswith("Error")]
        raise SystemExit(f"Namecheap API error: {errs}")
    return root

# 1) read + back up every existing record
root = call({"Command": "namecheap.domains.dns.getHosts", "SLD": sld, "TLD": tld})
hosts = [dict(h.attrib) for h in root.iter() if h.tag.endswith("host") or h.tag.endswith("Host")]
backup = f"dns-backup-{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
json.dump(hosts, open(backup, "w"), indent=2)
print(f"  backup of {len(hosts)} records -> {backup}")

# 2) rebuild the full host list, swapping only the 'www' record
params = {"Command": "namecheap.domains.dns.setHosts", "SLD": sld, "TLD": tld}
i, swapped = 0, False
for h in hosts:
    name, rtype = h.get("Name"), h.get("Type")
    addr, ttl = h.get("Address"), h.get("TTL", "1800")
    if name == "www":
        rtype, addr, swapped = "CNAME", target, True
    i += 1
    params[f"HostName{i}"] = name
    params[f"RecordType{i}"] = rtype
    params[f"Address{i}"] = addr
    params[f"TTL{i}"] = ttl
    if rtype == "MX":
        params[f"MXPref{i}"] = h.get("MXPref", "10")
if not swapped:
    i += 1
    params[f"HostName{i}"] = "www"
    params[f"RecordType{i}"] = "CNAME"
    params[f"Address{i}"] = target
    params[f"TTL{i}"] = "1800"
if any(h.get("Type") == "MX" for h in hosts):
    params["EmailType"] = "MX"

call(params)
print(f"  www -> CNAME {target} applied ({i} records preserved)")
PYEOF
  ok "Namecheap DNS updated via API"
else
  cat <<EOF

  Make this ONE change in the Namecheap dashboard:

    1. https://ap.www.namecheap.com/ → Domain List → connectomelab.com → [Manage]
    2. Open the "Advanced DNS" tab
    3. Find the record:   CNAME | www | ghs.googlehosted.com
    4. Edit its value to:              $PAGES_HOST
       (keep Type=CNAME, Host=www; TTL Automatic is fine)
    5. Save (green check)

  Nothing else needs to change. The old site keeps serving until this saves.

EOF
  read -rp "  Press Enter AFTER saving the DNS change (Ctrl-C to abort)... " _
fi

# -------------------------------------------------------- Step 3: verification
say "Step 3/3 — Verify (DNS propagation → GitHub check → HTTPS → live site)"

echo "  waiting for DNS to propagate (checks every 30s, up to 30 min)..."
for _ in $(seq 1 60); do
  [ "$(current_cname)" = "$PAGES_HOST" ] && { ok "DNS propagated: $DOMAIN -> $PAGES_HOST"; break; }
  sleep 30
done
[ "$(current_cname)" = "$PAGES_HOST" ] || die "DNS still not propagated — re-run later with: ./scripts/cutover.sh"

echo "  asking GitHub to re-check the domain..."
gh api "repos/$REPO/pages" -X PUT -f "cname=$DOMAIN" >/dev/null 2>&1 || true

echo "  waiting for the HTTPS certificate (checks every 60s, up to 30 min)..."
CERT_OK=false
for _ in $(seq 1 30); do
  STATE=$(pages_json | python3 -c 'import json,sys;print((json.load(sys.stdin).get("https_certificate") or {}).get("state",""))')
  if [ "$STATE" = "approved" ] || [ "$STATE" = "issued" ]; then CERT_OK=true; ok "certificate state: $STATE"; break; fi
  echo "    certificate state: ${STATE:-pending}..."
  sleep 60
done

if $CERT_OK; then
  gh api "repos/$REPO/pages" -X PUT -F https_enforced=true >/dev/null 2>&1 && ok "HTTPS enforcement enabled" || warn "could not enable HTTPS enforcement yet — retry later"
else
  warn "certificate not issued yet (can take up to ~1h). Re-run: ./scripts/cutover.sh --status"
fi

echo "  checking the live site..."
for _ in $(seq 1 10); do
  if curl -sfm 15 "https://$DOMAIN" 2>/dev/null | grep -q "$MARKER"; then
    ok "https://$DOMAIN is serving the NEW site 🎉"
    echo
    echo "  Done. If anything looks wrong: ./scripts/cutover.sh --rollback-help"
    exit 0
  fi
  sleep 30
done

warn "New site not visible over HTTPS yet (cert/CDN can lag). Check again with:"
echo "    ./scripts/cutover.sh --status"
rollback_help
