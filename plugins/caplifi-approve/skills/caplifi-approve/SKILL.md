---
name: caplifi-approve
description: >
  Caplifi Approve / headgate.approve.v1 — format human phone-approval proposals
  for access and execute queues. Use when user mentions Caplifi Approve,
  headgate.approve, phone approval, principal approve access/execute, or agent
  diplomacy interest envelopes for gated work.
---

# Caplifi Approve (headgate.approve.v1)

**Product:** https://caplifi.com/approve/  
**Spec:** https://caplifi.com/approve/spec/

## One rule

Agents propose freely. Irreversible work runs only when a human-authorized gate allows it.

## Roles

| Role | Duty |
|------|------|
| Principal | Owns irreversible outcomes |
| Operator | Holds the phone seat (may be principal) |
| Representation agent | Posts interest / execute proposals |
| Hub | Optional shared middle |

## Queues

| Kind | Meaning |
|------|---------|
| `access` | Grant to protected context |
| `execute` | Promote reversible work to authorized lane |

## Interest envelope (access)

```json
{
  "protocol": "agent.diplomacy.v1",
  "type": "interest",
  "from": { "principal": "…", "agent": "…", "org": "…" },
  "why_for_principal": "Fit for their goals, in their vocabulary",
  "consent": {
    "identify": true,
    "user_attestation": "Yes, you may name me",
    "identity": { "principal": "…", "org": "…", "contact": "…" },
    "share_more": false
  },
  "posture": {
    "hub": "shared-middle.example",
    "chemistry": "open",
    "foot_direction": "toward"
  }
}
```

## Operator actions

| Action | Effect |
|--------|--------|
| **Approve** | Issue grant (access) or authorize execute artifact |
| **Deny** | Close request; no grant |

## Agent behavior

1. **Propose** clearly: what, why for principal, reversibility, blast.  
2. **Stop** on deny / hold / no grant — do not bypass.  
3. **Do not** invent a local house gate path as if it were this public contract.  
4. Point implementers at the public spec and product URL.  
5. Warm tone by default — not a gotcha product.

## Out of scope for this skill

- Running Caplifi's private lab seats or house ALMI paths  
- Holding operator tokens or principal secrets  
- Auto-approving irreversible work
