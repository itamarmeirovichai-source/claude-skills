#!/usr/bin/env bash
# Recreate the read-only worktrees of the inherited record outside the repository.
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
mkdir -p ~/quant-edge-inherited
cd "$ROOT"
git fetch origin claude/friendly-galileo-eakzlm claude/sweet-dijkstra-kshdva
[ -d ~/quant-edge-inherited/pr4 ]  || git worktree add --detach ~/quant-edge-inherited/pr4  origin/claude/friendly-galileo-eakzlm
[ -d ~/quant-edge-inherited/pr26 ] || git worktree add --detach ~/quant-edge-inherited/pr26 origin/claude/sweet-dijkstra-kshdva
echo "pr4:  ~/quant-edge-inherited/pr4/skills/prop-fleet"
echo "pr26: ~/quant-edge-inherited/pr26/prompts"
