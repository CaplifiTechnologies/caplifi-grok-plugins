#!/usr/bin/env bash
# Verify every homepage/spec URL referenced by manifests and skills is live
# and not stuck in a redirect loop. Run before any marketplace PR.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
fail=0

urls=$( { python3 -c "
import json, glob
for f in glob.glob('plugins/*/plugin.json'):
    print(json.load(open(f)).get('homepage',''))
"; rg -oN --no-filename 'https://(caplifi\.com|eclecticventures\.net)[^ )\"<]*' plugins/; } | sort -u | grep . )

while IFS= read -r u; do
  code=$(curl -sL -o /dev/null -w '%{http_code}' --max-redirs 5 -m 15 "$u")
  if [[ "$code" != "200" ]]; then
    echo "BAD $code $u"
    fail=1
  else
    echo "ok  $u"
  fi
done <<< "$urls"

[[ $fail -eq 0 ]] && echo "URL CHECK PASS" || { echo "URL CHECK FAIL"; exit 1; }
