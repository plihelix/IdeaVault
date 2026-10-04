---
id: IDX-01Q
type: index
title: 01-userspace/questions - Open Questions
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, userspace, questions]
links: [IDX-01, VLT-USERSPACE, STATUS-MODEL, ID-SCHEME, GUIDE-NOTES, OQ-001, OQ-002, OQ-003]
---

# 01-userspace/questions - Open Questions

Purpose: hold every question the vault cannot yet answer, each with a due date, so that an unknown is a dated obligation instead of a hole in the prose.

## What belongs here

An `OQ-###` for anything that blocks a note, a decision, or a generated document: a fact that has to be looked up, a choice only the owner can make, a measurement that has not been taken, a term that is not yet settled. A question the owner asks the agent and a question the agent must ask the owner are the same kind of note.

## What does not belong here

A question answerable from a source card already in the vault: answer it and cite the card. A worry with no consequence: that is a `RSK-###` in `50-risk/`. An obligation: that is a `REQ-###`.

## Rules for this folder

- Block in use: numbers 1 to 40, allocated with `python3 _tools/vault.py next OQ 01-userspace`. Never invented, never reused.
- One question per note, phrased so an answer would be recognisable as an answer. "Is it worth doing?" is not a question; "Will the owner pay for X at price Y?" is.
- Every note carries `due:`. A question with no due date is a wish. `python3 _tools/vault.py due --stale 14` lists the ones nobody has touched.
- Every note lists what it blocks, in `blocked-by` or in the body. A question that blocks nothing is not worth its due date.
- The owner answers; the agent records the answer in the note, unblocks the notes that were waiting, and sets the question's `status:` to `accepted` only after the owner has given the answer.
- When a question dissolves because the idea changed shape, it becomes `superseded` with a line saying what replaced it. It is not deleted.
- File names: `oq-NNN-<topic>.md`.

## Open now

| ID | Question | Due | Blocks |
| --- | --- | --- | --- |
| `OQ-001` | what idea will this vault hold | 2026-10-17 | the whole vault |
| `OQ-002` | which domains this idea needs | 2026-10-31 | the folder shape |
| `OQ-003` | which output kinds are worth generating | 2026-11-14 | `outputs/` |

## Evidence

None yet: these are questions, not claims. When an answer comes from outside the vault, the answer cites the `S-###` card that carries it.

## Open issues

The three questions in the table above are this folder's content, and each is this folder's open issue until it is answered.
