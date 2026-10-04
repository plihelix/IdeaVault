---
id: TERMS-REG
type: glossary
title: Mechanism Vocabulary
status: proposed
owner: owner
updated: 2026-10-03
tags: [meta, glossary]
links: [IDX-90, CON-VLT-001, ID-SCHEME, STATUS-MODEL, REQ-LANG, VLT-USERSPACE, VLT-SHAPE, IDX-20, IDX-01O, IDX-TOOLS]
---

# Mechanism Vocabulary

Purpose: define the words this vault's mechanism uses, so that a note written next month means the same thing as one written today. Each entry points at the note that defines the thing in full; a definition is not maintained twice.

## The vault and its parts

| Term | Meaning | Defined in |
| --- | --- | --- |
| vault | this repository: notes, rules, scripts, and history, treated as one record | [conventions.md](../00-vault/conventions.md) |
| mechanism | the rules and tooling, independent of any idea | [00-vault/](../00-vault/_index.md) |
| mechanism note | a note the vault owns: `owner: vault`, and never cited as evidence about the idea | [conventions.md](../00-vault/conventions.md) |
| content note | a note about the idea: `owner:` is the owner's name | [conventions.md](../00-vault/conventions.md) |
| owner | the frontmatter field carrying that split, derived from the note's path | [userspace.md](../00-vault/userspace.md) |
| userspace | `01-userspace/`: the folders the owner writes in and reads directly | [userspace.md](../00-vault/userspace.md) |
| domain | a top-level numbered folder with its own index and rules | [conventions.md](../00-vault/conventions.md) |
| index file | a folder's `_index.md`: its instruction file, `type: index`, holding no obligations | [conventions.md](../00-vault/conventions.md) |
| spec folder | a domain that carries claims, whose index must state evidence and open issues | [reshaping.md](../00-vault/reshaping.md) |

## Naming and address

| Term | Meaning | Defined in |
| --- | --- | --- |
| ID | a note's permanent address, written `<PREFIX>-<number>` and never reused | [id-scheme.md](../00-vault/id-scheme.md) |
| handle | a named ID for a note outside a numbered namespace (`GUIDE-SHAPE`, `TERMS-REG`) | [id-scheme.md](../00-vault/id-scheme.md) |
| namespace | a prefix whose numbers are allocated in order from one block | [id-scheme.md](../00-vault/id-scheme.md) |
| ID block | the range of numbers a folder may allocate from, recorded in `this-vault.json` | [id-scheme.md](../00-vault/id-scheme.md) |
| allocation | taking the next free number by command, never by hand | [id-scheme.md](../00-vault/id-scheme.md) |
| register | one file holding many entries of one namespace, each entry keeping its own ID | [conventions.md](../00-vault/conventions.md) |
| instantiation | setting this vault's title, owner name, and blocks in `this-vault.json` | [ADR-0003](../01-userspace/decisions/adr-0003-one-instantiation-file-names-the-owner-and-the-id-blocks.md) |

## Weight and standing

| Term | Meaning | Defined in |
| --- | --- | --- |
| status | how much weight a note carries: `draft`, `proposed`, `accepted`, `superseded`, `rejected`, `archived` | [status-model.md](../00-vault/status-model.md) |
| accepted | settled by the human owner; changing it means superseding it | [status-model.md](../00-vault/status-model.md) |
| supersede | replace a standing note with a new one, keeping both readable | [status-model.md](../00-vault/status-model.md) |
| blocked | a note cannot advance until a named question is answered, written as `[BLOCKED: OQ-###]` | [status-model.md](../00-vault/status-model.md) |
| inference | an unverified assumption, marked in place and barred from an accepted note | [conventions.md](../00-vault/conventions.md) |
| normative wording | `MUST`-style obligation, licensed only in claim-bearing note types | [requirement-language.md](../00-vault/requirement-language.md) |

## Claims and their grounds

| Term | Meaning | Defined in |
| --- | --- | --- |
| claim | a statement the idea takes as binding, in any of four kinds | [20-claims/](../20-claims/_index.md) |
| constraint | fixed outside the idea and not negotiable while it stands as it is | [requirement-language.md](../00-vault/requirement-language.md) |
| assumption | taken as true, named as falsifiable | [requirement-language.md](../00-vault/requirement-language.md) |
| acceptance criterion | the observable test of a claim | [id-scheme.md](../00-vault/id-scheme.md) |
| evidence chain | claim to criterion to gate to part to control to finding to source card | [id-scheme.md](../00-vault/id-scheme.md) |
| source card | one external source, with citation, dates, excerpt, and confidence | [sources/](../70-evidence/sources/_index.md) |
| finding | a synthesis across cards, with a confidence level | [findings/](../70-evidence/findings/_index.md) |
| gate | a point where the idea is checked against criteria and can be refused | [60-quality/](../60-quality/_index.md) |
| metric | a number with a method, a unit, and a reason it was chosen | [60-quality/](../60-quality/_index.md) |
| control | a limit placed on a named risk | [50-risk/](../50-risk/_index.md) |
| stage | a state of the work, with an entry and an exit condition | [40-plan/](../40-plan/_index.md) |
| role | a named responsibility that decides something | [40-plan/](../40-plan/_index.md) |
| decision record | an act that closes an option, with context, decision, and consequences | [decisions/](../01-userspace/decisions/_index.md) |
| open question | a question with a due date and a named consequence | [questions/](../01-userspace/questions/_index.md) |

## Generation and upkeep

| Term | Meaning | Defined in |
| --- | --- | --- |
| output kind | a declared shape the vault can generate, with sections and a word budget | [outputs/](../01-userspace/outputs/_index.md) |
| issued instance | one generated document in a kind, dated, drawn from named notes | [outputs/issued/](../01-userspace/outputs/issued/_index.md) |
| word budget | the length limits a kind sets, read by `words` and `audit` | [outputs/](../01-userspace/outputs/_index.md) |
| triage | turning inbox material into a note in the folder that owns it, a question, or a proposal to delete | [inbox/](../01-userspace/inbox/_index.md) |
| scaffold | generating a skeleton note from `_templates/` with the next free ID | [_tools/](../_tools/_index.md) |
| stamp | setting `updated:` on the notes git reports as changed | [_tools/](../_tools/_index.md) |
| report line | a checker's statement of file, line, and rule | [checking-the-vault.md](../01-userspace/guides/checking-the-vault.md) |
| `PROBLEMS: n` | the closing line of every report; 0 means the vault matches its own rules | [_tools/](../_tools/_index.md) |

## Evidence

None: these entries restate the mechanism notes they point at. Where an entry and its note disagree, the note is authoritative and the entry is a defect.

## Open issues

[OQ-002](../01-userspace/questions/oq-002-which-domains-does-this-idea-need.md) - the idea's own vocabulary joins this register as the writing produces it, and some of these definitions will be narrowed by a real subject.
