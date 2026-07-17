---
name: brandmd-audit
description: >
  Audit a repository for BRAND.md conformance and completeness score. Use when the
  user says brandmd audit, check brand repo, BRAND.md score, or brand conformance.
---

# Audit BRAND.md repo

**Spec:** https://caplifi.com/build/brandmd/

## Checklist

### Required

- [ ] `BRAND.md` at repo root
- [ ] Title line: brand name + semver
- [ ] Sections in order: Identity, Color, Type, Voice, Logo, Load deeper, Integrity
- [ ] Color ≤ 6 rows in core
- [ ] Type entries include web-safe fallback stacks
- [ ] Core size roughly ≤ 600 tokens (`chars/4`)

### Recommended

- [ ] `/brand/voice.md`, `visual.md`, `strategy.md`, `usage.md`
- [ ] `/brand/tokens.json` (DTCG)
- [ ] `/brand/assets.manifest.json` with `version`, `generated`, `canonical`, `assets[]`
- [ ] Each asset: `file`, `sha256` (lowercase hex), `role`, `formats`
- [ ] `CHANGELOG.md`
- [ ] No broken pointers from core → missing files

### Integrity spot-check

For 1–3 assets: recompute SHA-256 and compare to manifest.

## Report format

```markdown
# BRAND.md audit — {path}
**Conformant core:** yes/no
**Estimated core tokens:** N
**Score (honest):** X/10 — gaps listed
## Errors
## Warnings
## Suggested next edits
```

Gaps are welcome. Completeness score is a starting point, not a gate for shipping the standard itself.
