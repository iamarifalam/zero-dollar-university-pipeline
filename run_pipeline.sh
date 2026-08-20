#!/usr/bin/env bash
# ==============================================================================
# 0$ University - Dedicated Daily LinkedIn Growth Pipeline Execution Wrapper
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo "🎓 0$ UNIVERSITY - LINKEDIN DAILY GROWTH ENGINE"
echo "⏰ Triggered at: $(date)"
echo "======================================================================"

# Check Python environment
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run QA Dedup Auditor first
python3 scripts/qa_dedup_auditor.py

# Run Main 0$ University Engine
python3 scripts/zero_dollar_uni_runner.py "$@"

echo "======================================================================"
echo "✅ Execution Completed Successfully!"
echo "======================================================================"
