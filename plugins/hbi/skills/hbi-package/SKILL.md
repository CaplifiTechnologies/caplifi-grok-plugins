---
name: hbi-package
description: >
  Create or shape a Half-Baked Idea (HBI) package: MANIFEST, IDEA, HANDOFF,
  IP_TRIAGE, DISCLOSURE. Use when the user says HBI, half-baked idea, package
  this idea, IP triage, disclosure gate, or hbi package.
---

# HBI package workflow

**Spec:** https://eclecticventures.net/hbi/ · GitHub: CaplifiTechnologies/hbi-standard  
**Invariant:** Triage is advisory. Only the disclosure gate authorizes distribution outside the owner's control.

## Package layout

```
{package-id}/
  MANIFEST.json
  IDEA.md
  HANDOFF.md
  IP_TRIAGE.json
  DISCLOSURE.json
  CHANGELOG.md          # recommended
  ATTACHMENTS/          # optional
```

## ID format

`^[a-z0-9]+(-[a-z0-9]+)*-\d{4}-\d{2}$`  
Example: `acequia-attestation-2026-07`

## Stages

| Stage | Meaning |
|-------|---------|
| `inbox` | Raw capture |
| `half-baked` | Actively shaping |
| `packaged` | Structurally complete |
| `shipped` | Approved for distribution **outside** private boundary |
| `parked` | Shelved intentionally |

**Never** set `stage: shipped` unless `DISCLOSURE.json` has explicit approval per the open standard.

## HANDOFF.md first line

| First word | Mode |
|------------|------|
| `HANDOFF` | discuss |
| `INSTIGATE` | execute |

## IP_TRIAGE.json (advisory only)

Status examples: `untriaged`, `not-patentable`, `defensive-publication`, `consider-provisional`.  
Classifier output **MUST NOT** be treated as permission to publish.

## DISCLOSURE.json (gate)

Record whether disclosure is `closed` or approved, who approved, when.  
If closed: do not put package contents on public remotes, marketplaces, or stranger-facing plugins.

## Agent rules

1. Prefer creating packages in a path the **user names** (their workspace).  
2. Do not open-source closed packages.  
3. After structural edits, run `hbi-validate` skill / `tools/hbi_validate.py`.  
4. Do not invent legal advice; triage is fuzzy classification, not counsel.
