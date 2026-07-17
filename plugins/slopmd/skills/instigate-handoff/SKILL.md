---
name: instigate-handoff
description: >
  Write INSTIGATE (execute on receipt) or HANDOFF (absorb then discuss) documents
  correctly. Use when the user says INSTIGATE, HANDOFF, handoff doc, work order,
  or agent briefing.
---

# INSTIGATE & HANDOFF

Two document types. The **first word** is the contract.

| Title word | Posture |
|------------|---------|
| **INSTIGATE** | Act — execute on receipt |
| **HANDOFF** | Absorb — load context; next move is conversation, not action |

An INSTIGATE that opens with discussion is malformed.  
A HANDOFF that opens with a command is malformed.

## INSTIGATE template

```markdown
INSTIGATE

From:          [you or agent]
To:            [agent]
Date:          [date]
Subject:       [one line — the action]
Reversibility: [reversible | irreversible, gate before executing]

## Action
[Imperative directive]

## Done when
[Concrete acceptance criteria]

## Boundaries
[In / out of scope]

## Constraints
[Invariants — keys, audit, gates]

## Inputs
[Links and paths, not retelling]
```

If irreversible: gate behind human confirmation before running.

## HANDOFF template

```markdown
HANDOFF

From:    [you or agent]
To:      [agent]
Date:    [date]
Subject: [what this briefing is about]

## Context
[What they need to know]

## State
[Current status, artifacts, links]

## Open questions
[Decisions still needed]

## Suggested next discuss
[Topics — not commands]
```

## Agent behavior

- Receiving **INSTIGATE** → execute toward Done when.  
- Receiving **HANDOFF** → summarize and discuss; do not freestyle a ship.  
- When writing for another agent, pick the type deliberately.
