---
id: VLT-USERSPACE
type: note
title: Userspace - The Boundary Between the Human and the Agent
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, userspace]
links: [CON-VLT-001, STATUS-MODEL, ID-SCHEME, VLT-SHAPE, ADR-0002, ADR-0004, IDX-01]
---

# Userspace - The Boundary Between the Human and the Agent

Purpose: say exactly where the person who owns the vault writes, where the agent working on the idea writes, and what each side may not do, so that nobody has to guess which folder a given act belongs in.

## The boundary

`01-userspace/` is the human's folder. It is the input surface and the reading surface: what the owner drops in, what the owner is asked to answer, what the owner has decided, and what the vault produces for the owner to read. Every other domain folder - `10-idea/` through `70-evidence/`, `90-glossary/`, `99-archive/` - is the agent's working ground: the agent writes there, the human reads there.

The split is not decoration. It is recorded in every note's `owner` field, derived from the note's path by the checker ([conventions.md](conventions.md)), and it is the rule an agent obeys when it decides where to put something.

## What the human does

| Act | Where it lands |
| --- | --- |
| Drop raw material: a link, a half-formed thought, a remark, a document to be dealt with | `01-userspace/inbox/` |
| Answer a question the vault could not answer | the `OQ-###` note in `01-userspace/questions/` |
| Decide, decline, or close an option | an `ADR-####` in `01-userspace/decisions/` |
| Accept or decline a note the agent wrote | that note's `status:`, set by the human alone |
| Ask for a document to be generated from the vault | a request; the instance lands in `01-userspace/outputs/issued/` |
| Change the shape of the vault | an `ADR-####`, then the agent carries it out ([reshaping.md](reshaping.md)) |
| Write an instruction the vault must follow | a decision record, not a stray file |

## What the agent does

| Act | Where it lands |
| --- | --- |
| Classify inbox material into the domain that owns it | the domain folder, plus a note in the inbox entry saying where it went |
| Write and revise claims, structure, plan, risks, quality, and evidence | `20-claims/`, `30-structure/`, `40-plan/`, `50-risk/`, `60-quality/`, `70-evidence/` |
| State what the idea currently is, as far as it is understood | `10-idea/` |
| Raise a question the vault cannot yet answer | a new `OQ-###` in `01-userspace/questions/`, with a due date |
| Draft a decision record for a choice the human has made or been offered | a `proposed` `ADR-####` in `01-userspace/decisions/` |
| Generate a document in a declared output kind | an instance in `01-userspace/outputs/issued/` |
| Maintain the mechanism: the rules, the templates, the scripts, the shape | `00-vault/`, `_templates/`, `_tools/`, after a decision record authorises it |

## What neither side does

- An agent never sets `accepted` on any note. Only the owner does, on mechanism notes as on content notes ([status-model.md](status-model.md)).
- An agent never writes a claim into `01-userspace/decisions/` that the human has not made. It records the human's decision, or drafts one for the human to accept.
- The human never edits a domain folder to fix wording. A correction is a note to the agent or a decision record; the agent makes the edit, and the change is attributed to the human's decision.
- Nobody writes into `99-archive/` except to move a superseded or rejected note there.
- Guides in `01-userspace/guides/` route the reader to the mechanism. They do not restate it, because a restatement is a second rule that can drift from the first.

## Ownership inside userspace

Notes in `01-userspace/` carry the owner's name in `owner:`, including the guides: a guide you have edited is your instruction. The `_index.md` file of each userspace folder carries `owner: vault`, because an instruction file is mechanism wherever it sits. This is the same rule as everywhere else, so `check` needs no special case for the human's folder.

## Why the boundary is enforced rather than polite

A vault that only *says* where each side writes drifts: an agent files a decision in a domain folder, a human drops a claim into the inbox and it is never triaged, and the record stops matching the acts that produced it. The checker knows the expected `owner` value for every path, so a note filed on the wrong side of the boundary is reported as a problem instead of being quietly wrong.
