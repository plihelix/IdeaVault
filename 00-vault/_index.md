---
id: IDX-00
type: index
title: 00-vault - How This Vault Works
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta]
links: [ADR-0001, ADR-0002, ADR-0003, ADR-0005, ADR-0006, HOME, AGENTS]
---

# 00-vault - How This Vault Works

Purpose: hold the mechanism of the vault - the rules that make a pile of notes into a record that can be checked, traced, and handed to someone else - and the one file that says which vault this one is.

## What belongs here

Rules about writing and about the shape of the vault: note frontmatter, the ID scheme, the status model, normative language, the boundary between the human's folder and the agent's folders, and the rules for changing the shape of the vault. Plus `this-vault.json`, the instantiation file that names this vault, its owner, and the ID blocks in use.

## What does not belong here

The idea itself, in any form. Nothing here states what the vault is about, what it aims at, or what has been decided about it: those live in `10-idea/`, `20-claims/`, and `01-userspace/`. Rules that only one domain follows live in that domain's `_index.md`.

## Files

| File | ID | Role |
| --- | --- | --- |
| [conventions.md](conventions.md) | CON-VLT-001 | note shape, frontmatter fields, naming, linking, citation and commit rules |
| [id-scheme.md](id-scheme.md) | ID-SCHEME | namespaces, handles, allocation, traceability |
| [status-model.md](status-model.md) | STATUS-MODEL | what each status means and who may set it |
| [requirement-language.md](requirement-language.md) | REQ-LANG | where `MUST`-style wording is allowed and what a well-formed obligation looks like |
| [userspace.md](userspace.md) | VLT-USERSPACE | the boundary between what the human writes and what the agent manages |
| [reshaping.md](reshaping.md) | VLT-SHAPE | how a domain, a namespace, or an ID block is added, renamed, or retired |
| `this-vault.json` | - | the instantiation file: vault name, owner name, namespaces and blocks, spec folders |

## Rules for this folder

- Every file here is mechanism: `owner: vault`, and no note in this folder is ever cited as evidence for a claim about the idea.
- A change to any file here needs a decision record in [01-userspace/decisions/](../01-userspace/decisions/_index.md). These rules affect every other note, so they are not edited quietly.
- The shipped mechanism is `proposed` until the owner accepts it. Accepting it is the first act in [01-userspace/guides/start-here.md](../01-userspace/guides/start-here.md).
- Keep each file under about 120 lines. Split rather than grow.
