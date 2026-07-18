#!/usr/bin/env bash
# Local self-test for the Caplifi agent plugins monorepo
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
fail=0

echo "== structure =="
for p in brandmd hbi slopmd caplifi-approve; do
  for f in "plugins/$p/plugin.json" "plugins/$p/.grok-plugin/plugin.json" "plugins/$p/.claude-plugin/plugin.json" "plugins/$p/README.md"; do
    if [[ ! -f "$f" ]]; then echo "MISSING $f"; fail=1; fi
  done
  if ! find "plugins/$p/skills" -name SKILL.md | grep -q .; then
    echo "NO SKILLS in $p"; fail=1
  fi
done

echo "== manifests in sync (plugin.json == .grok-plugin == .claude-plugin) =="
for p in brandmd hbi slopmd caplifi-approve; do
  if ! cmp -s "plugins/$p/plugin.json" "plugins/$p/.grok-plugin/plugin.json" || \
     ! cmp -s "plugins/$p/plugin.json" "plugins/$p/.claude-plugin/plugin.json"; then
    echo "MANIFEST DRIFT in $p"; fail=1
  fi
done
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))" || { echo "BAD marketplace.json"; fail=1; }

echo "== no house paths in plugins (tools/ included) =="
if rg -n '~/ALMI|matthewgallegos|/Users/matthew|127\.0\.0\.1:8|localhost:8' plugins/ 2>/dev/null; then
  echo "HOUSE PATH LEAK"
  fail=1
else
  echo "clean"
fi

echo "== hbi validator smoke =="
TMP=$(mktemp -d)
PKG="$TMP/smoke-idea-2026-07"
mkdir -p "$PKG"
cat > "$PKG/MANIFEST.json" <<'JSON'
{
  "id": "smoke-idea-2026-07",
  "title": "Smoke",
  "stage": "packaged",
  "created": "2026-07-17T00:00:00Z",
  "updated": "2026-07-17T00:00:00Z",
  "spec_version": "1.0"
}
JSON
echo '# Smoke idea' > "$PKG/IDEA.md"
printf 'HANDOFF\n\n# discuss smoke\n' > "$PKG/HANDOFF.md"
cat > "$PKG/IP_TRIAGE.json" <<'JSON'
{"status": "untriaged", "notes": "smoke"}
JSON
cat > "$PKG/DISCLOSURE.json" <<'JSON'
{"status": "closed", "approved": false}
JSON
python3 plugins/hbi/tools/hbi_validate.py "$PKG" || true

echo "== plugin.json names =="
for p in brandmd hbi slopmd caplifi-approve; do
  python3 -c "import json; d=json.load(open('plugins/$p/plugin.json')); assert d['name']=='$p', d"
done

if [[ $fail -ne 0 ]]; then
  echo "SELFTEST FAIL"
  exit 1
fi
echo "SELFTEST PASS"
