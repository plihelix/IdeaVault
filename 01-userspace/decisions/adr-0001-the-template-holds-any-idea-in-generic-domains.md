---
id: ADR-0001
type: decision
title: The template holds any idea in generic domains
status: proposed
owner: owner
updated: 2026-10-03
tags: [decision, shape]
links: [IDX-00, IDX-20, IDX-30, IDX-40, IDX-50, IDX-60, IDX-70, VLT-SHAPE, OQ-002]
---

# ADR-0001: The template holds any idea in generic domains

Status: proposed, 2026-10-03.

## Context

A vault is only useful if the person using it can file what they are thinking without first translating it into someone else's categories. The working reference this template was modelled on had folders and namespaces shaped for one particular software system: requirements split into functional and non-functional, an architecture split into two halves, a factory domain, a security domain with threats, an operations domain. That shape is excellent for that idea and wrong for almost every other one: a research position has no factory, a plan has no architecture, a body of knowledge has no threats, and a half-stated intention has none of them.

The decision this vault needs before any content goes in is what its domains are, and whether they name kinds of statement or kinds of subject.

## Decision

1. Domains name **kinds of statement**, not kinds of subject: `10-idea/` what the idea is, `20-claims/` what it depends on being true, `30-structure/` what it is made of, `40-plan/` how it gets realised, `50-risk/` how it could fail, `60-quality/` how it is judged, `70-evidence/` what grounds it outside the vault.
2. The shipped namespaces are generic: `REQ`, `CON`, `ASM`, `AC`, `CMP`, `IF`, `STG`, `ROLE`, `RSK`, `CTL`, `GATE`, `MET`, `S`, `FND`, `ADR`, `OQ`. The reference vault's `REQ-F`/`REQ-N` split becomes one `REQ` block; `THR` becomes `RSK`; `R-F` becomes `FND`.
3. A domain may be empty for an idea that does not need it, and an empty domain records that fact rather than being padded.
4. `80-` is left free as the next number, so a domain this idea needs can be added without renumbering anything.
5. The mechanism carries no vocabulary from any single field: no product, no technology, no framework, no organisation.

## Consequences

- A new subject fits by filing, not by reshaping: most ideas will never need a domain change.
- Splitting a claim type that the reference vault split (functional versus non-functional requirements) loses that distinction. An idea that needs it adds a second `REQ` register or a new namespace, by decision record.
- Generic names are slightly less suggestive than specific ones: `50-risk/` invites less immediate thinking than a domain named for a specific class of threat. The cost is accepted, because the alternative is a template that fits one idea.
- Empty folders look unfinished. They are not: each one says what it would hold and why it holds nothing yet.

## Alternatives considered

- **Keep the reference vault's domains and rename only the obvious ones.** Refused: the shape would still assume a built system with an architecture, a factory, and an operations layer.
- **Ship only `10-idea/`, `20-claims/`, `70-evidence/` and let everything else be added later.** Refused: a vault with no room for structure, plan, risk, or judgement gets those written into `10-idea/` as one growing note, which is the failure mode this mechanism exists to prevent.
- **Let the owner choose the folder names before anything is written.** Refused as a first step: choosing names before there is an idea produces a taxonomy invented for its own sake. The shipped set is a working default, and [reshaping.md](../../00-vault/reshaping.md) is how it changes once the idea is known.

## Affects

Sets the folder tree in [HOME.md](../../HOME.md), the namespace table in [id-scheme.md](../../00-vault/id-scheme.md), and the blocks in `00-vault/this-vault.json`. Kept open by [OQ-002](../questions/oq-002-which-domains-does-this-idea-need.md), which may reopen points 1 and 2 once the idea is named.

## Evidence

The reference vault this mechanism was modelled on, and the mechanism notes it authorises. No outside source is cited: this is a decision about the shape of the record, not a claim about the world.

## Revisit when

The idea is named and the first dozen claims are written. If material keeps landing in a folder whose index says it does not belong, or a folder's index grows exceptions, this decision is reopened by a new record here.
