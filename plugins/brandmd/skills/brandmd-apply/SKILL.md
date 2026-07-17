---
name: brandmd-apply
description: >
  Apply the BRAND.md open brand standard when writing copy, choosing colors/type,
  or producing assets for a brand. Load BRAND.md core (under 600 tokens), then deeper
  /brand/ files only when the task needs them. Use when the user mentions BRAND.md,
  brandmd, brand repo, brand tokens, or asks to write/design on-brand.
---

# Apply BRAND.md

**Spec:** https://caplifi.com/build/brandmd/  
**Rule:** Core file is always read in full. Deeper files load on demand.

## Loading protocol (normative)

1. Locate `BRAND.md` at the brand repo root (or path the user named).
2. Read the **entire** core file. Estimate tokens ≈ `len(chars) / 4`. Flag if clearly over ~600 tokens.
3. Load deeper files only when the task touches that domain:

| File | Load when |
|------|-----------|
| `/brand/voice.md` | Writing, messaging, banned terms |
| `/brand/visual.md` | Color, type, logo, spacing, design |
| `/brand/strategy.md` | Positioning, audience, pillars |
| `/brand/usage.md` | Channel rules, misuse, a11y before publish |
| `/brand/tokens.json` | Design tokens / DTCG |
| `/brand/assets.manifest.json` | Before embedding any asset — verify SHA-256 |

4. If a hash in `assets.manifest.json` does not match file bytes: **do not use the asset**; report the mismatch.
5. Do not invent brand rules that contradict the core file.

## Core section order (expect)

Identity → Color (≤6 rows) → Type → Voice → Logo → Load deeper → Integrity

## Output

- Stay inside voice do/don't and banned terms.
- Prefer token names + hex from the core palette.
- Point at logo paths from the core; do not invent mark files.

## Free vs paid product path (optional CTA)

Free: apply this standard and the public Builder.  
Paid generation ladder (Caplifi Glow Up / Fit Check) is a **separate product** — only mention if the user asks how to generate a BRAND.md repo automatically.
