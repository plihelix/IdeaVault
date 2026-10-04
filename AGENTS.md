---
id: AGENTS
type: index
title: AGENTS.md - Working Inside a Vault of This Shape
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, agents]
links: [HOME, IDX-00, CON-VLT-001, ID-SCHEME, STATUS-MODEL, REQ-LANG, VLT-USERSPACE, VLT-SHAPE, IDX-01, IDX-TOOLS, ADR-0002, ADR-0003, ADR-0005]
---

# AGENTS.md - Working Inside a Vault of This Shape

Purpose: onboard an agent to any vault built on this mechanism, without telling it what the idea is. Everything here is about how the vault works; the idea lives in the domain folders and is not described in this file.

## What you are working in

A vault is a git repository of short, dated, ID-addressable notes divided into domains. Each note declares what kind of thing it is and how much weight it carries. Claims are traceable to evidence, unknowns are named as open questions with due dates, and decisions are recorded so a later reader can see what was closed and why. The rules are not advisory: `_tools/vault.py` checks them and reports `PROBLEMS: <n>`, where 0 means the vault is consistent with its own stated rules. A clone of the template also carries the repository's front page - `README.md` and the images in `assets/` - which are not notes, are removed by `instantiate`, and are reported by `check` until they are gone.

## Read before you write

1. [HOME.md](HOME.md) - what this vault holds and its current state.
2. [00-vault/conventions.md](00-vault/conventions.md) - frontmatter, naming, linking, commits.
3. [00-vault/id-scheme.md](00-vault/id-scheme.md) - namespaces, handles, allocation.
4. [00-vault/status-model.md](00-vault/status-model.md) - what each status means and who may set it.
5. [00-vault/userspace.md](00-vault/userspace.md) - which folders you write in and which you do not.
6. The `_index.md` of every folder you are about to touch. The index is that folder's law; folder content obeys it.

## Where you write

You write in `10-idea/`, `20-claims/`, `30-structure/`, `40-plan/`, `50-risk/`, `60-quality/`, `70-evidence/`, `90-glossary/`, `99-archive/`, `00-vault/`, `_templates/`, and `_tools/`.

In `01-userspace/` you write only four things: a new `OQ-###` for a question the vault cannot answer, a `proposed` `ADR-####` recording a choice the owner has made or has been offered, a generated instance under `01-userspace/outputs/issued/`, and triage notes on inbox entries. You do not decide on the owner's behalf, and you do not answer the owner's questions for them.

The owner's name and `vault` are the only legal `owner:` values, and which one a note takes follows from its path. `check` derives it. A note filed on the wrong side of the boundary is reported as a defect, so file it on the right side instead of arguing about it later.

## The note contract

- Frontmatter, in order: `id`, `type`, `title`, `status`, `owner`, `updated`, `tags`, `links`. Optional: `supersedes`, `superseded-by`, `blocked-by`, `due`, `review`, `confidence`.
- Body: `# Title`, then `Purpose:`, then `##` sections, then `## Evidence`, then `## Open issues`.
- One note per file. A file that has become two topics becomes two notes plus a link.
- `updated:` is the date of the last substantive edit. `_tools/vault.py stamp --changed` sets it for the notes git reports as changed, before the commit.
- Skeletons come from `_templates/` through `scaffold`. Fill in every placeholder before the note is saved anywhere; a placeholder outside `_templates/` is a defect.

## IDs

- Allocate with `python3 _tools/vault.py next PREFIX [FOLDER]`. Never invent a number, never reuse one, never renumber one.
- Stay inside the block recorded for your folder in `00-vault/this-vault.json`.
- Refer to another note by its ID, never by a file path.
- In prose, write an ID as a shape (`REQ-###`) when no specific note is meant. A concrete ID that no note defines shows up in the reports as an undefined reference.

## Status

You may set `draft` and `proposed`. You never set `accepted`, `superseded`, `rejected`, or `archived` on the owner's behalf: `accepted` is the owner's signature, and the other three close or reverse something the owner may still want open. Advancing your own note to `proposed` requires complete frontmatter, a non-empty `## Evidence` for anything grounded outside the vault, and no unlinked `[INFERENCE]`.

## Evidence

- Outside claim → an `S-###` source card with URL, publisher, publication date, access date, and a short excerpt.
- Synthesis across sources → an `FND-###` finding citing the cards.
- Claim-bearing notes cite findings, not raw URLs.
- A source that benefits from the claim it reports is `confidence: low` and never carries a number alone.
- No source and no measurement → mark it `[INFERENCE]` in place. An `[INFERENCE]` cannot sit in an `accepted` note.
- When the idea has no outside evidence - an intention, a plan, a position being formed - write that plainly in `## Evidence` and name the owner's statement or measurement instead.

## Normative wording

`MUST`, `SHOULD`, `MAY`, `NEVER`, `AVOID` and their relatives belong only in a `REQ-*`, `CON-*`, `AC-*`, `GATE-*`, `STG-*`, or the Control line of a `CTL-*`. Everywhere else, write indicatively. The checker enforces this by note type. When mentioning a keyword as a word rather than using it normatively, put it in backticks.

## Commands

```
python3 _tools/vault.py check                  # every rule the scanner enforces
python3 _tools/vault.py status                 # counts, statuses, types, headroom
python3 _tools/vault.py metrics                # the same facts as key=value lines
python3 _tools/vault.py ids [PREFIX|ID]        # the ID ledger, gaps, headroom
python3 _tools/vault.py next PREFIX [FOLDER]   # the next free ID
python3 _tools/vault.py find PATTERN           # titles, frontmatter, bodies
python3 _tools/vault.py links [PATH|ID]        # broken links, orphans, referrers
python3 _tools/vault.py oq                     # open questions with due dates
python3 _tools/vault.py adr                    # decision ledger and supersession chains
python3 _tools/vault.py due [DATE]             # due and review dates; --stale DAYS
python3 _tools/vault.py changed [DATE]         # notes git reports changed
python3 _tools/vault.py stamp --changed        # set updated: to today
python3 _tools/vault.py scaffold TYPE TITLE [FOLDER]   # a skeleton with the next free ID
python3 _tools/vault.py instantiate NAME [TITLE]    # name the vault and drop the front page
python3 _tools/vault.py words [FILE...]        # generated instances against their budgets
python3 _tools/vault.py noise [FILE...]        # banned content terms in generated bodies
python3 _tools/vault.py audit [FILE...]        # generated instances: budget, policy, registration
python3 _tools/vault.py commitmsg "SUBJECT"    # the commit message for the staged files
```

`--root PATH` points any command at another vault. Every report ends with `PROBLEMS: <n>`; exit 0 means the report found nothing.

## The working loop

1. Read the folder's `_index.md` and the notes already in it. Do not write a second note for something one already holds: edit it, or supersede it.
2. Triage `01-userspace/inbox/` first. Every entry is promoted to the folder that owns it, turned into an open question, or proposed for deletion.
3. Write or amend notes in the folder that owns the subject. New claims start `draft`.
4. Name what you do not know as an `OQ-###` with a due date, and put `[BLOCKED: OQ-###]` in the note that waits on it.
5. When a decision has been made, write its `ADR-####` in `01-userspace/decisions/` as `proposed`, and record it in the ledger: `supersedes` the note it replaces, and update the replaced note's `superseded-by`.
6. Run `check`, `links`, and `adr`. Fix what they name. A report with problems is unfinished work, not a note to mention in your summary.
7. `stamp --changed`, stage the exact paths, generate the message with `commitmsg` after staging, commit, and require `git status --short` to be empty.

## Commit format

`<folder> + <folder>: <what changed> (<ID list>)`, built by `commitmsg` from the staged files. Stage with explicit paths. `git add` and `git commit` are separate commands, and the message comes from the first line `commitmsg` prints.

## What stays with the owner

Accepting any note. Answering an `OQ-###`. Deciding, declining, and closing options. Choosing which documents the vault generates and what the kinds mean. Changing the shape of the vault - a domain, a namespace, an ID block - which is a decision record first and an edit second ([reshaping.md](00-vault/reshaping.md)). Anything that costs money, deletes work, or reaches outside the machine.

## What breaks the vault

- A concrete ID that no note defines, or an ID invented instead of allocated.
- A relative link that points nowhere, including an example link written to illustrate a rule.
- A placeholder or an unfinished-work marker left outside `_templates/`.
- Normative wording in a note that only describes.
- An `accepted` note written by an agent, or an `accepted` note edited in place instead of superseded.
- Two notes defining the same ID, or one note defined in two files.
- A claim in a spec folder with no evidence line behind it, or an unmarked guess.
- A file that is not a note left sitting in the vault, including the repository's front page once the vault has been named.
- A mechanism file changed with no decision record behind the change.
