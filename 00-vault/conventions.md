---
id: CON-VLT-001
type: note
title: Note and Vault Conventions
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta]
links: [IDX-00, ID-SCHEME, STATUS-MODEL, REQ-LANG, VLT-USERSPACE, ADR-0001, ADR-0002, ADR-0003, ADR-0005, ADR-0006]
---

# Note and Vault Conventions

Purpose: every note is addressable, dated, attributable, and traceable to evidence, whatever the idea it records happens to be.

## Instantiation

`this-vault.json` in this folder is the only place that says which vault this is: the vault's name, the owner's name, the ID namespaces with their numeric blocks, and which folders carry claims. The scripts in `_tools/` read it instead of carrying these facts in their source. Changing the shape of the vault means changing that file, under the rules in [reshaping.md](reshaping.md) - not editing a script.

## Filesystem rules

- Domain folders are named `NN-kebab-case` (`40-plan/`). The number is reading order, not hierarchy, and gaps are deliberate room for a domain added later.
- The unprefixed folders are `_templates/` (note skeletons) and `_tools/` (the scripts that check and maintain the vault). Neither belongs to a domain ([ADR-0005](../01-userspace/decisions/adr-0005-tooling-and-the-health-demo-travel-with-the-vault.md)).
- Every folder holds an `_index.md`: its instruction file, always first in that folder's reading order, always `type: index`. Folder content obeys it.
- File names are lowercase kebab-case. Register and namespace entries are ID-prefixed (`adr-0003-....md`, `oq-001-....md`). No spaces, no dates in names, except inbox entries, which are ephemeral.
- One note per file. A file that has become two topics becomes two notes plus a link.
- Attachments (diagrams, exports, PDFs, data files) go in the owning folder's `assets/` and are linked relatively.
- A clone may also carry the repository's own front page for a code forge: `README.md` at the vault root, and the images that page shows, kept in an `assets/` folder at the vault root. Neither is a note, nothing in the vault links to them, and `instantiate` removes both when the vault is named. Until it has, `check` reports the front page as a problem: a vault is self-describing only when every file inside it is a note. The root `assets/` belongs to the front page; a note's attachments still go in the owning folder's `assets/`.
- `LICENCE` at the repository root is the repository's own file: plain text, no frontmatter, no ID, no owner, no status. The checker governs markdown notes and does not report it, and `instantiate` leaves it in place, because the terms the template travels under do not change when the vault is named ([ADR-0006](../01-userspace/decisions/adr-0006-the-repository-ships-a-licence-that-survives-instantiation.md)).
- Internal links are relative markdown links so the vault stays readable outside any particular note-taking app. Never write an example link that points nowhere: a broken link is a defect, and the checker reports it as one.

## Frontmatter

Every note begins with YAML frontmatter. Required fields:

```yaml
---
id: REQ-###            # the shape; the real number comes from `next REQ` in _tools/vault.py
type: requirement      # index|note|requirement|constraint|assumption|acceptance-criteria|
                       # component|interface|risk|control|stage|role|gate|finding|source|
                       # decision|open-question|metric|template|glossary
title: A title a reader can recognise from the folder listing
status: draft          # draft|proposed|accepted|superseded|rejected|archived
owner: owner           # `vault` in a mechanism note, the owner's name in every other note
updated: 2026-10-03    # ISO date of the last substantive edit
tags: [meta]
links: [S-###, FND-###, OQ-###]   # IDs of the notes this one depends on or argues against
---
```

Optional fields: `supersedes`, `superseded-by`, `blocked-by`, `due` (ISO date, open questions), `review` (ISO date, when the note is due to be re-checked), `confidence` (`high|medium|low`, findings).

`owner` carries the split between the mechanism and the idea ([ADR-0002](../01-userspace/decisions/adr-0002-userspace-is-where-the-human-writes.md)). It takes exactly two values: `vault` in the core notes - the root entry files `HOME.md` and `AGENTS.md`, everything under `00-vault/`, `_templates/` and `_tools/`, and every folder `_index.md` - and the owner's name from `this-vault.json` in every other note. The expected value follows from the note's path, and `check` derives it from the path, so a note cannot pick its own side of the split. `accepted` is set only by the human owner, on mechanism notes as on content notes.

A register file - one file holding many entries of one namespace - takes `id: <PREFIX>-REG` or a descriptive handle, and carries the `type` of the entries it registers (`requirement`, `constraint`, `assumption`, `acceptance-criteria`, `component`, `interface`, `risk`, `control`, `stage`, `role`, `gate`, `metric`), so that [requirement-language.md](requirement-language.md) licenses normative wording exactly where the register's entries sit. A register that is a pure catalogue with no obligations uses `type: index`. Folder and sub-folder instruction files always use `type: index` and hold no obligations. A register's own ID is never cited as one of its entries. Descriptive notes that are not members of a numbered namespace use `id: <TAG>-<TOPIC>` (`GUIDE-SHAPE`, `VLT-USERSPACE`).

## Body shape

1. `# Title` matching `title`.
2. `Purpose:` one sentence saying what the note is for.
3. Body in `##` sections. Registers use a table or one `###` block per entry, each with its stable ID.
4. `## Evidence` listing the source and finding IDs the note relies on. Required for any claim grounded outside the vault.
5. `## Open issues` listing the `OQ-###` IDs that keep this note from reaching `accepted`.

## Citation discipline

- A claim taken from outside the vault cites an `S-###` source card. The card holds the URL, publisher, publication date, access date, and a short verbatim or near-verbatim excerpt.
- A synthesis across sources is an `FND-###` finding. Claim-bearing notes cite findings, not raw URLs.
- A source written by the party that benefits from the claim is marked `confidence: low` and never carries a number on its own. Two independent sources, or a measurement taken here, is required.
- A claim with no source and no measurement is marked `[INFERENCE]` in place, and cannot appear in an `accepted` note.
- When the idea is something nobody published - an intention, a plan, a position being formed - the evidence line says so plainly and names the owner's own statement or measurement instead. Absence of outside evidence is recorded, not hidden.

## Style

- Terse, declarative, no marketing, no emoji, no rhetorical questions in claim-bearing folders.
- Present tense for facts; normative wording only where [requirement-language.md](requirement-language.md) licenses it.
- Numbers carry units and the method that produced them: `p95 response 1.5 s measured at the gateway, warm cache`.
- Diagrams: mermaid, only where the structure is real, with every node labelled by its component ID (`CMP-###`).
- Fill-ins and unfinished-work markers belong only inside `_templates/`. Where something is unknown outside a template, name an `OQ-###` instead of leaving a hole in the prose.

## Versioning

The vault is a git repository. Commit per note-set. Message format: `<folder> + <folder>: <what changed> (<ID list>)`, built by `python3 _tools/vault.py commitmsg "<subject>"` after staging, so the folder list and the ID list come from the staged files rather than from memory. Never rewrite the history of an `accepted` note: supersede it.
