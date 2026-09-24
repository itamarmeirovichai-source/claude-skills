#!/bin/bash
# Installs the "minds", "skill-prompt-architect", "live-results" and "prop-fleet" Claude Code skills.
# Usage: curl -fsSL https://raw.githubusercontent.com/itamarmeirovichai-source/claude-skills/main/install.sh | bash
set -euo pipefail

REPO="itamarmeirovichai-source/claude-skills"
SKILLS=(minds skill-prompt-architect live-results prop-fleet)
DEST="$HOME/.claude/skills"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "Downloading skills from github.com/$REPO ..."
curl -fsSL "https://github.com/$REPO/tarball/main" | tar xz -C "$TMP" --strip-components=1

mkdir -p "$DEST"
for s in "${SKILLS[@]}"; do
  if [ -d "$DEST/$s" ]; then
    mv "$DEST/$s" "$DEST/$s.bak.$$"
    echo "  (existing $s backed up to $s.bak.$$)"
  fi
  cp -R "$TMP/skills/$s" "$DEST/$s"
  echo "✓ installed $s"
done

echo ""
echo "Done! Open a NEW Claude Code session and type /minds, /skill-prompt-architect, /live-results or /prop-fleet"
