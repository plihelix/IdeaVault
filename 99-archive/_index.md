---
id: IDX-99
type: index
title: 99-archive - Superseded and Rejected Notes
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, archive]
links: [HOME, CON-VLT-001, STATUS-MODEL, ID-SCHEME, OQ-002]
---

# 99-archive - Superseded and Rejected Notes

Purpose: keep the notes that no longer stand, with their IDs and their reasons, so that a reader can see what was tried, what was refused, and what the current claims were written against.

## What belongs here

A note whose status is `superseded`, `rejected`, or `archived`, moved here when leaving it in its original folder would mislead a reader about what currently stands. A retired folder index, kept as an `archived` note pointing at what replaced it.

## What does not belong here

A note that is merely old: age is not a reason to archive, and `review:` dates do that work where it matters. A note that is out of date but still standing. Anything still cited by a live claim, unless the citing note is updated in the same commit.

## Rules for this folder

- Nothing is deleted from this vault. A note that closes an option keeps its ID here, or stays where it was with a status that says so.
- A moved note keeps its ID and its `updated:` history; the move is recorded in the commit, and the note gains a line saying where it came from.
- Every archived note names what replaced it (`superseded-by`) or why it was refused (`## Rejected because`). An archive entry with no reason is a rumour with a date.
- An archived note is never cited as evidence for a live claim. A reader who needs the old conclusion cites the new note that records it.
- Nobody writes new content here. A new note belongs in the domain that owns its subject.

## Contents

| ID | Was | Why it is here |
| --- | --- | --- |
| none yet | - | - |

## Evidence

None: an archive records the vault's own history, and the history is in the git log and in the notes themselves.

## Open issues

None. An empty archive in a fresh vault is the correct state, and it will fill on its own as the idea changes shape.
