# hbi — Grok Build plugin

[HBI](https://eclecticventures.net/hbi/) (Half-Baked Idea) v1.0 — open package format for ideas **before** they ship.

## Design invariant

- **IP triage is advisory** — never authorization to distribute  
- **Disclosure gate is deterministic** — only explicit approval authorizes `shipped`  
- **Container ≠ content leak** — closed packages stay closed  

## Skills

| Skill | When |
|-------|------|
| `hbi-package` | Create or shape an HBI package |
| `hbi-validate` | Run conformance validation |

## Tools

`tools/hbi_validate.py` — pure Python reference validator (no network).

```bash
python3 tools/hbi_validate.py /path/to/package-id-2026-07
```

## Install

```bash
grok plugin install ./plugins/hbi --trust
```
