---
name: hbi-validate
description: >
  Validate an HBI package for structural conformance using the reference
  validator. Use when the user says hbi validate, check HBI package, or
  conformance test.
---

# Validate HBI package

## Command

From the plugin root (or any path to the script):

```bash
python3 tools/hbi_validate.py /path/to/{package-id}
```

If the plugin install path is unknown, search for `hbi_validate.py` under the plugin directory or ask the user for the package path and run the script from this plugin's `tools/`.

## Pass criteria

- All required files present  
- `MANIFEST.json` id/stage fields valid  
- HANDOFF first token is `HANDOFF` or `INSTIGATE`  
- `shipped` only with valid disclosure approval  

## Report

Paste validator JSON/stdout. Summarize errors and warnings. Fix structure, then re-run. Do not “fix” disclosure closed → shipped.
