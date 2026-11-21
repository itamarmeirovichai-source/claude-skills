#!/bin/bash
# Deploy the VXO site (code + local media) to a separate Cloudflare Pages project.
# Needs CLOUDFLARE_API_TOKEN (Pages:Edit) and CLOUDFLARE_ACCOUNT_ID in the environment settings — never in chat or git.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${CLOUDFLARE_API_TOKEN:?set CLOUDFLARE_API_TOKEN in the environment settings}"
: "${CLOUDFLARE_ACCOUNT_ID:?set CLOUDFLARE_ACCOUNT_ID in the environment settings}"
PROJECT="${PAGES_PROJECT:-studio-site}"
npm run media:check
npm run build
npx --yes wrangler@4 pages project create "$PROJECT" --production-branch main 2>/dev/null || true
npx --yes wrangler@4 pages deploy dist --project-name "$PROJECT" --branch main --commit-dirty=true
