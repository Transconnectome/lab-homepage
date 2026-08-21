#!/bin/bash
# ==============================================================================
# Connectome Lab - DGX-Spark Local Automation Runner
# Can be scheduled via crontab on dgx-spark or executed via Claude Code CLI.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== [Connectome Lab] Starting Local Intelligence Sync ==="
cd "$REPO_DIR"

# 1. Run OpenAlex / Scholar crawler
python3 "$SCRIPT_DIR/sync_scholar.py"

# 2. Run SOTA Research Radar (calls OpenRouter / Gemini API if key is present)
python3 "$SCRIPT_DIR/update_research_radar.py"

# 3. Refresh Featured Projects repo metadata (GitHub API, unauthenticated is fine locally)
python3 "$SCRIPT_DIR/sync_project_metadata.py"

# 4. Generate AI research ideas via the local codex CLI (ChatGPT login auth, no API key).
#    CODEX_MODEL must match the model configured in codex so generatedBy stays honest.
IDEAS_BACKEND=codex CODEX_MODEL="${CODEX_MODEL:-gpt-5.6-sol}" \
  python3 "$SCRIPT_DIR/generate_research_ideas.py"

# 5. Render idea infographics via codex imagegen (DGX-only; skips gracefully elsewhere).
#    Review the images before pushing — this runner does not commit.
python3 "$SCRIPT_DIR/generate_idea_infographics.py"

# 6. Test local build
npm run build

echo "=== [✓] Local Sync and Build Completed Successfully ==="
