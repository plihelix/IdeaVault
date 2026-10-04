---
id: IDX-01I
type: index
title: 01-userspace/inbox - Raw Material
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, userspace, inbox]
links: [IDX-01, VLT-USERSPACE, GUIDE-NOTES, OQ-001]
---

# 01-userspace/inbox - Raw Material

Purpose: catch anything the owner wants kept without deciding yet what it is. The inbox is the only place a note may be vague on purpose.

## What belongs here

A link worth keeping, a half-formed thought, a remark made in conversation, a document to be dealt with later, a question that is not yet sharp enough to be an `OQ-###`. One entry per file, short.

## What does not belong here

Anything the owner already knows the home of: a claim goes to `20-claims/`, a decision to `decisions/`, a source to `70-evidence/sources/`. A note that has been triaged does not stay here "for reference".

## Rules for this folder

- Entries are ephemeral. An entry that is still here after two sessions is either triaged, promoted to an `OQ-###`, or deleted, and the reason is written on the entry.
- Entries use descriptive handles (`INB-<TOPIC>`), never a numbered ID from another namespace. No `REQ-*`, `OQ-###`, or `ADR-####` number is allocated in the inbox: allocation happens in the folder that owns the namespace, when the entry is promoted.
- Name entries `inb-<topic>.md`, lowercase kebab-case, no date in the name; the frontmatter `updated:` carries the date.
- Triage is the agent's job and is done before new work is written. The agent writes, on the entry, where the material went and what it became, then the entry is deleted or reduced to a pointer.
- An entry is not evidence. When material from the inbox is quoted as a fact, it first becomes an `S-###` source card or is marked as the owner's own statement.

## Triage record

| Entry | Became | Where |
| --- | --- | --- |
| none yet | - | - |

## Open issues

[OQ-001](../questions/oq-001-what-idea-will-this-vault-hold.md) - until the idea is named, most inbox material will have no obvious domain to land in, which is what the inbox is for.
