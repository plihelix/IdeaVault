---
id: IDX-TPL
type: index
title: Templates
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, templates]
links: [CON-VLT-001, ID-SCHEME, STATUS-MODEL, REQ-LANG, IDX-TOOLS]
---

# Templates

Purpose: copyable note skeletons so that notes written by the owner or by an agent come out shaped the same way, whatever the idea is.

## What belongs here

One skeleton per note type that recurs. A template is a fill-in scaffold, not a note: this is the only place in the vault where a `<<...>>` fill-in or a `-000` placeholder ID is legal. A note created from a template `MUST` have every fill-in resolved, its `id` allocated through `next` in [id-scheme.md](../00-vault/id-scheme.md), and its `links` pointing at real IDs before it is committed as anything other than `draft`.

Templates carry no status beyond `proposed` and `archived`, and are never cited as evidence.

## Templates

| File | Produces | Type value | ID shape |
| --- | --- | --- | --- |
| [requirement.md](requirement.md) | an obligation the idea takes on | `requirement` | `REQ-###` |
| [constraint.md](constraint.md) | a limit fixed outside the idea | `constraint` | `CON-###` |
| [assumption.md](assumption.md) | a claim treated as true and named falsifiable | `assumption` | `ASM-###` |
| [acceptance-criteria.md](acceptance-criteria.md) | the observable test of one requirement | `acceptance-criteria` | `AC-###` |
| [component.md](component.md) | a part of the idea | `component` | `CMP-###` |
| [interface.md](interface.md) | a boundary between two parts | `interface` | `IF-###` |
| [stage.md](stage.md) | a stage of the work | `stage` | `STG-###` |
| [role.md](role.md) | a responsibility that decides something | `role` | `ROLE-###` |
| [risk.md](risk.md) | a way the idea could fail | `risk` | `RSK-###` |
| [control.md](control.md) | a limit placed on a named risk | `control` | `CTL-###` |
| [gate.md](gate.md) | a point where the idea can be refused | `gate` | `GATE-###` |
| [metric.md](metric.md) | a number with a method | `metric` | `MET-###` |
| [finding.md](finding.md) | a synthesis across sources | `finding` | `FND-###` |
| [source.md](source.md) | one external source | `source` | `S-###` |
| [decision.md](decision.md) | a choice that closes an option | `decision` | `ADR-####` |
| [open-question.md](open-question.md) | a question with a due date | `open-question` | `OQ-###` |
| [note.md](note.md) | a descriptive note outside a numbered namespace | `note` | `<TAG>-<TOPIC>` |

## Rules

- Frontmatter fields match [conventions.md](../00-vault/conventions.md); a new field is added to conventions first, not to a template.
- Generate through the command, which allocates the ID and fills `owner` and `updated` from the target folder: `python3 _tools/vault.py scaffold <type> "<title>" <folder>`.
- Normative wording rules from [requirement-language.md](../00-vault/requirement-language.md) apply to whatever obligation a template carries; a descriptive skeleton stays indicative.
- A template that no note uses for six months is archived rather than maintained.
