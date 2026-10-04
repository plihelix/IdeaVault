---
id: VLT-SHAPE
type: note
title: Reshaping the Vault Around the Idea
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, shape]
links: [CON-VLT-001, ID-SCHEME, VLT-USERSPACE, ADR-0001, ADR-0003, IDX-01G]
---

# Reshaping the Vault Around the Idea

Purpose: give the exact procedure for changing the vault's shape - a domain added, renamed, merged, or retired - so that a shape change is a recorded decision with a mechanical follow-through, and not a folder quietly renamed until the checker starts complaining.

## What may be reshaped

- **Domains.** The numbered folders, their names, and what each one is for.
- **Namespaces and blocks.** The prefixes in `this-vault.json`, their numeric blocks, and which folder may allocate from them.
- **Output kinds.** The shapes the vault generates, their sections, and their word budgets.
- **Templates.** The skeletons in `_templates/`.
- **The mechanism files themselves** in `00-vault/`.

What is not reshaped on impulse: the frontmatter contract, the status model, the ownership split, and the ID allocation rules. Those are what make two notes comparable; changing one is a decision about the vault itself, recorded as such.

## The procedure

1. **Decide it.** Write or amend an `ADR-####` in `01-userspace/decisions/` naming the change, why the idea needs it, and what it costs. This is the human's act.
2. **Edit `00-vault/this-vault.json`.** Add or remove the namespace entries and their blocks, the `folder_blocks` entry for the folder, and the folder's name in `spec_index_folders` if it will carry claims.
3. **Create the folder and its `_index.md`** before anything is filed in it. The index states what belongs there, what does not, the ID range in use, the rules, and - for a claim-bearing domain - `## Evidence` and `## Open issues`.
4. **Give it room to number.** A domain that owns namespaces gets a block in `this-vault.json` and the same range written in its `_index.md`. A domain that only holds descriptive notes needs no block.
5. **Update the pointers.** `HOME.md`, the affected indexes, and any guide that routes to the changed folder. Cross-references use IDs, so renaming a folder changes no ID.
6. **Check it.** `python3 _tools/vault.py check`, then `ids`, then `links`. A shape change that leaves `PROBLEMS: 0` is finished; anything else is unfinished work.
7. **Commit it** with the folders and IDs the change touched, through `commitmsg`.

## Adding a namespace

- The prefix is uppercase, short, and unambiguous: `RSK`, `GATE`, `MET`. It must not collide with an existing prefix or a handle form.
- Give it a block that leaves room: 30 to 100 numbers for a namespace a real idea will fill, 20 for one it will not.
- Give it a `width` if it is not three digits. Decision records use four (`ADR-####`) so that a four-digit ledger sorts beside a three-digit one without renumbering.
- Add a row to the namespaces table in [id-scheme.md](id-scheme.md), and to the `_index.md` of the folder allowed to allocate from it.
- If the type of note that uses it carries obligations, add its `type` value to the licensed set in [requirement-language.md](requirement-language.md) and to `LICENSED_TYPES` in `_tools/vault_scan.py`. The two must agree; a mismatch is a defect in the script.

## Renaming or merging domains

- Renaming a folder never changes an ID, a status, or an `updated:` date. It changes paths, and every relative link that pointed at the old path.
- Merging two domains means one folder's content moves, its index is retired as `archived` with `superseded-by` pointing at the surviving index, and its block is folded into the survivor's block or retired.
- Splitting a domain keeps the original IDs with the notes that already held them. Nothing is renumbered.

## Retiring a domain or a namespace

- Set the retired notes to `archived`, move bodies to `99-archive/` when leaving them in place would mislead, and keep the retired index as an `archived` note pointing at what replaced it.
- A retired block is retired for good. Its numbers are never handed out again, in this vault or in a copy of it.
- `this-vault.json` keeps no entry for a retired namespace, and `check` then reports any surviving reference to it as an out-of-block ID.

## Gaps are part of the design

The shipped numbering leaves `80-` empty on purpose. A domain the idea needs that the shipped seven do not cover takes the next free number, and gaps inside a block are reported by `ids` because a gap is usually a deleted note that was never superseded.

## What a shape change looks like in the reports

| Symptom | Report |
| --- | --- |
| A note filed in a folder with no `_index.md` | `check`: `NN-folder/_index.md: missing folder instruction file` |
| An ID outside its folder's block | `check`: `id ... outside the block for ...` |
| A namespace nobody was allowed to allocate | `ids`: `cross-listed` against the owning folder |
| A block with no free number left | `metrics`: `numbering_exhausted=PREFIX`, and `next PREFIX` reporting no free number |
| A claim-bearing domain index missing its evidence or open-issues section | `check`: the missing section |
| A mechanism file changed with no decision record | not a checker problem; it is what `adr` and the commit history make visible |
