#!/usr/bin/env bash
# ==============================================================================
# Double-clickable macOS launcher for 0$ University LinkedIn Growth Engine
# ==============================================================================
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "======================================================================"
echo "🎓 Launching 0$ University LinkedIn Growth Engine"
echo "======================================================================"

if [ -f "run_pipeline.sh" ]; then
    bash run_pipeline.sh "$@"
else
    python3 scripts/zero_dollar_uni_runner.py "$@"
fi

echo ""
echo "Press any key to close this terminal..."
read -n 1 -s
