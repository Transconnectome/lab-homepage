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

# 3. Test local build
npm run build

echo "=== [✓] Local Sync and Build Completed Successfully ==="
