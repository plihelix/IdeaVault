---
id: STATUS-MODEL
type: note
title: Status Model
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta]
links: [CON-VLT-001, ID-SCHEME, VLT-USERSPACE, ADR-0002]
---

# Status Model

Purpose: make explicit how much weight a note carries, so that a half-formed intention is never mistaken for a commitment.

## Values

| Status | Meaning | May be cited as |
| --- | --- | --- |
| `draft` | the author's thinking, unreviewed, may be wrong | context only |
| `proposed` | internally coherent, waiting on the owner's decision | input to a decision |
| `accepted` | the owner has signed off; it stands; changing it means superseding it | the basis for further work |
| `superseded` | replaced by a newer note; kept for provenance | history only |
| `rejected` | deliberately not adopted; kept with the reason | precedent, guardrail |
| `archived` | out of scope for now; kept for whatever comes next | history only |

Two auxiliary markers are not statuses and appear inline, never in frontmatter:

- `[BLOCKED: OQ-###]` - this note cannot advance until the named question is answered.
- `[INFERENCE]` - an unverified assumption. Allowed in `draft` and `proposed`, never in an `accepted` note.

## Transitions

```
draft ──(self-review complete, evidence listed)──▶ proposed
proposed ──(owner decides, ADR if it closes an option)──▶ accepted
accepted ──(new evidence or a new decision)──▶ superseded  +  a new note accepted
proposed ──(owner declines)──▶ rejected
any ──(out of scope for now)──▶ archived
```

## Rules

- Only the human owner sets `accepted`, on mechanism notes as on content notes: the vault does not sign off its own mechanism, and an agent never signs off the idea. See [userspace.md](userspace.md).
- Advancing to `proposed` requires: complete frontmatter, a non-empty `## Evidence` for anything grounded outside the vault, and no unlinked `[INFERENCE]`.
- Advancing to `accepted` requires: no `blocked-by`, and for a `REQ-*` a matching `AC-*`.
- A decision record is required whenever a transition closes an option a reader would otherwise consider open.
- `superseded` and `rejected` notes keep their IDs and gain `superseded-by` or a `## Rejected because` section. Move the body to `99-archive/` only when leaving it where it is would mislead a reader.
- An idea that is still half-stated is not a defect. It is a `draft` note in `10-idea/` with the open parts listed as `OQ-###`.

## Freshness

Notes whose evidence goes out of date (measurements, published capability, licence terms, market facts) carry `review: YYYY-MM-DD`. A note past its review date is treated as `draft` whatever its recorded status, until it is re-checked. Set `review` six months out for anything measured, twelve months out for anything quoted from a document.
