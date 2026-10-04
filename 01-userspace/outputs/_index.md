---
id: IDX-01O
type: index
title: 01-userspace/outputs - Documents the Vault Generates
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, userspace, outputs]
links: [IDX-01, IDX-01OI, OUT-ELEVATOR, OUT-BRIEF, OUT-EXPLAINER, ADR-0004, OQ-003]
---

# 01-userspace/outputs - Documents the Vault Generates

Purpose: hold the declared shapes the vault can generate from its own notes, and the instances it has issued in those shapes. A generated document is a reading surface: someone outside the vault reads it, and the vault's claims are what it asserts.

## Two levels

| Level | Handle | What it is |
| --- | --- | --- |
| Kind | `OUT-<KIND>` | a declaration: sections, length budget, what may be claimed, what must be cited |
| Instance | `ISS-<KIND>` | one generated document in that kind, generated on a date, from a stated set of notes |

A kind is a rule about generation. An instance is a product of it. Neither is evidence for anything: a generated document restates claims, and the claims carry the evidence.

## What belongs here

Kinds, in this folder, one note each: [elevator-pitch.md](elevator-pitch.md), [one-page-brief.md](one-page-brief.md), [long-form-explainer.md](long-form-explainer.md). Instances, in [issued/](issued/_index.md), one file each.

## What does not belong here

Working notes, drafts of the idea itself, or a document the owner wrote by hand. A document that is not generated from the vault's notes has no `ISS-` handle and no place here.

## Rules for this folder

- A kind is added by decision record, not by writing a document in an improvised shape. Add the kind note, its budget, and its `OUT-<KIND>` handle, then generate into it.
- Kinds are declared with a word budget written as `<min> to <max> words`, which `words` and `audit` read as the budget. A budget is a length limit, not a target to pad toward.
- An instance links to its kind, to the notes it drew from, and to nothing it cannot cite.
- An instance is generated from `accepted` and `proposed` notes, and says which ones it drew from. An instance that rests on a `draft` note marks it as such.
- `python3 _tools/vault.py words` checks every issued instance against its kind's budget; `audit` checks budget, banned content terms, and registration in the issued index; `noise` reports banned terms in the bodies.
- A shipped instance is never quietly rewritten. A new version is a new instance with a new date.

## Open issues

[OQ-003](../questions/oq-003-which-output-kinds-are-worth-generating.md) - the three shipped kinds are a starting guess about what this vault will need to say out loud.
