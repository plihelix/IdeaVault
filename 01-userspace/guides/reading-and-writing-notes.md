---
id: GUIDE-NOTES
type: note
title: Reading and Writing Notes
status: proposed
owner: owner
updated: 2026-10-03
tags: [userspace, guide]
links: [GUIDE-START, GUIDE-CHECKS, CON-VLT-001, ID-SCHEME, STATUS-MODEL, REQ-LANG, VLT-USERSPACE, IDX-01, IDX-01I, IDX-01Q, IDX-01D]
---

# Reading and Writing Notes

Purpose: read a note in this vault without guessing what weight it carries, and put something in without having to know every rule first.

## What a note is

One file, one subject, one ID. The file name is `id-in-kebab-case` for anything in a numbered namespace (`adr-0003-....md`), and a plain descriptive name for a guide or a folder instruction file.

The frontmatter at the top is the part you read first:

| Field | What it tells you |
| --- | --- |
| `id:` | the address; other notes refer to this, never to the file path |
| `type:` | what kind of statement it is - a claim, a constraint, a finding, a decision, a guide, an index |
| `status:` | how much weight it carries: `draft`, `proposed`, `accepted`, `superseded`, `rejected`, `archived` |
| `owner:` | who is responsible for it: `vault` for the mechanism, your name for everything else |
| `updated:` | the date of the last substantive edit |
| `tags:` | how you will find it again |
| `links:` | the notes it depends on or argues against |

Optional fields you will see: `due` on a question, `review` on anything whose evidence ages, `confidence` on a finding, `blocked-by` on a note waiting for an answer, `supersedes` and `superseded-by` on a replaced note.

## Reading the body

The first line after the frontmatter is the title, then `Purpose:` in one sentence. Then sections. Two sections matter most: `## Evidence`, which says what the note rests on, and `## Open issues`, which lists the questions keeping it from being settled. A note with an empty `## Evidence` is either about the vault itself or about your own intention - and it says which.

`[INFERENCE]` in a body means the author knows this part is a guess. `[BLOCKED: OQ-001]` means the note cannot advance until that question is answered. Both are useful: they tell you where the vault is weak instead of leaving you to find out later.

## Status, in practice

`draft` is thinking. `proposed` is coherent and waiting for you. `accepted` is settled and stands until something replaces it. `superseded` and `rejected` are kept, with their reasons, because a reader needs to know what was closed. `archived` is out of scope for now.

Only you set `accepted`. An agent will advance its own notes to `proposed` and ask you to accept them.

## Putting something in without knowing the rules

Write it in `01-userspace/inbox/` as one short file. Name it `inb-<topic>.md`. Say what it is and why you kept it. The agent triages it into the folder that owns it and writes on the entry where it went, so the trail survives.

Three other acts are yours directly:

- Ask a question the vault cannot answer: a new `OQ-###` in `01-userspace/questions/`, with a due date and a line saying what it blocks.
- Record a decision you made: an `ADR-####` in `01-userspace/decisions/`, or tell the agent the decision and let it draft the record for you to accept.
- Ask for a document: name the kind in `01-userspace/outputs/` and the instance lands in `outputs/issued/`.

## Claims, constraints, assumptions

A claim you are taking on is a `REQ-###`. A fact outside your control that binds it is a `CON-###`. Something you are treating as true but would abandon if contradicted is an `ASM-###`. How you would prove a claim is an `AC-###`. The difference matters later: a constraint you wrote as a claim will be renegotiated by someone who does not know it was fixed, and an assumption you wrote as a claim will be defended after it has already failed.

Normative wording - `MUST`, `SHOULD`, `MAY` - belongs in claims, constraints, acceptance criteria, gates, stages, and controls. Everywhere else, write indicatively; the checker enforces this by note type. Details in [requirement-language.md](../../00-vault/requirement-language.md).

## What never happens

An edit to a note you accepted, in place: supersede it instead. A renumbered ID. A deleted decision record. A claim quoted from somewhere else with no source card behind it. A file written into a domain folder that has no `_index.md` yet.
