#!/usr/bin/env bash
# Tag-driven release: pin marketplace entries to an existing tag's SHA,
# build per-plugin zips + checksums into dist/.
#
# Usage: scripts/release.sh v0.1.1
#
# Process (fixes the pin-chases-HEAD loop):
#   1. Land all content changes on main.
#   2. git tag vX.Y.Z && git push --tags
#   3. scripts/release.sh vX.Y.Z   → rewrites docs/marketplace-entries.json pins
#      to the TAG's SHA (which never moves) and builds dist/ artifacts.
#   4. Commit the pin change ("docs: pin marketplace to vX.Y.Z"). This commit
#      lands AFTER the tag and never invalidates it.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TAG="${1:?usage: release.sh <tag>}"
SHA="$(git rev-parse "${TAG}^{commit}")"
echo "pinning to $TAG = $SHA"

python3 - "$SHA" <<'EOF'
import json, sys
sha = sys.argv[1]
path = "docs/marketplace-entries.json"
entries = json.load(open(path))
for e in entries:
    e["source"]["sha"] = sha
json.dump(entries, open(path, "w"), indent=2)
print(f"updated {path}: {len(entries)} entries")
EOF

bash scripts/selftest.sh

mkdir -p dist
rm -f dist/*.zip dist/SHA256SUMS
for p in brandmd hbi slopmd caplifi-approve; do
  (cd plugins && zip -qr "../dist/${p}-${TAG}.zip" "$p" -x '*.DS_Store')
done
(cd dist && shasum -a 256 ./*.zip > SHA256SUMS && cat SHA256SUMS)
echo "release artifacts in dist/ — attach to the GitHub Release for $TAG"
