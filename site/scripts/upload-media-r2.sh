#!/bin/bash
# Upload public/media/** to the private R2 bucket that functions/media/[[path]].ts serves from
# (needed only for a Git-connected Pages build, where public/media is not in the repo).
# Needs CLOUDFLARE_API_TOKEN (R2 edit) and CLOUDFLARE_ACCOUNT_ID in the environment settings, never in chat or git.
# Usage: bash scripts/upload-media-r2.sh [bucket=studio-media]
set -euo pipefail
cd "$(dirname "$0")/.."
: "${CLOUDFLARE_API_TOKEN:?set CLOUDFLARE_API_TOKEN in the environment settings}"
: "${CLOUDFLARE_ACCOUNT_ID:?set CLOUDFLARE_ACCOUNT_ID in the environment settings}"
BUCKET="${1:-studio-media}"
npm run media:check
find public/media -type f ! -name '*.tmp.mp4' | sort | while read -r f; do
  key="media/${f#public/media/}"
  echo "put $key"
  npx --yes wrangler@4 r2 object put "$BUCKET/$key" --file "$f" --remote >/dev/null
done
