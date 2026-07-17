---
name: slop-envelope
description: >
  Author or parse SLOP.md agent handoff envelopes (slop.v1). Use for multi-agent
  inbox/outbox drops, instigate vs handoff types, acks, results. Triggers: SLOP,
  slopmd, agent handoff envelope, slop.v1, inbox drop.
---

# SLOP.md envelopes

**Spec:** https://eclecticventures.net/slopmd/

## Invariant

Fuzzy layers inform. Deterministic code gates anything irreversible.  
Agents never write the human-only `authorized/` lane.

## Envelope (markdown + YAML front-matter)

```yaml
---
protocol: slop.v1
id: 20260717T120000Z-short-slug
type: instigate | handoff | ack | result | error | query | handshake | note
from: <agent-id>
to: <recipient>
in_reply_to: null
created_at: 2026-07-17T12:00:00Z
auth: none
---

# Body
```

## Type vs mode

| Signal | Mode |
|--------|------|
| `type: instigate` (default) | **execute** |
| `type: handoff` | **discuss** |
| `mode: discuss` on any type | **discuss** (overrides) |
| Body "discuss only" | **discuss** |
| `authorized/` + valid signature | **execute** for irreversible |

Never let discuss-mode trigger irreversible actions.

## Lanes (file transport)

| Lane | Who writes |
|------|------------|
| inbox/ | any |
| outbox/ | watcher/orchestrator |
| authorized/ | **human only** |
| archive/ | watcher |
| assets/ | anyone (large blobs) |

## Rules

1. Never overwrite a prior drop — new `id`, use `in_reply_to`.  
2. One seat per drop (`from` is a specific agent surface).  
3. Transport-agnostic: same envelope over files, HTTP, or cloud folders.  
4. Replies: classify (ack vs result), don't dump novels into push notifications.
