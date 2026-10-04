#!/usr/bin/env python3
"""Vault integrity scan for an ideation vault.

Tooling, not a note: no frontmatter, no ID, never cited as evidence (ADR-0005).
The rules enforced here are stated in 00-vault/conventions.md, 00-vault/id-scheme.md,
00-vault/status-model.md, 00-vault/requirement-language.md, 00-vault/userspace.md, and
00-vault/_index.md. A disagreement between this script and those notes is a defect in
this script.

The namespaces, ID blocks, spec folders, and owner name are read from
00-vault/this-vault.json (ADR-0003): this script ships no vault-specific constants.

Run: python3 _tools/vault_scan.py [vault-root]
Import: vault_scan.scan(root) returns the result containers, so _tools/vault.py
reports on the same rule set instead of restating it.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".obsidian", "assets", ".trash"}

TYPES = {
    "index", "note", "requirement", "constraint", "assumption", "acceptance-criteria",
    "component", "interface", "stage", "role", "risk", "control", "gate", "finding",
    "source", "decision", "open-question", "metric", "template", "glossary",
}
STATUSES = {"draft", "proposed", "accepted", "superseded", "rejected", "archived"}
REQUIRED_FIELDS = ["id", "type", "title", "status", "owner", "updated", "tags", "links"]

# ADR-0002: `owner` carries the mechanism/content split so a vault can be lifted out as a
# template without inventing a second metadata field. Core notes are the vault's own machinery
# and travel with it; every other note carries the human's idea and stays with the human.
# The human's name is read from 00-vault/this-vault.json by configure(), never hardcoded here.
HUMAN_OWNER = "owner"
CORE_OWNER = "vault"
CORE_DIRS = {"00-vault", "_templates", "_tools"}
CORE_FILES = {"HOME.md", "AGENTS.md"}

# A clone of the template carries the repository's front page for a code forge, plus the
# images that page shows. Neither is a note: no frontmatter, no ID, no owner, no status. The
# vault is self-describing only when every file inside it is a note, so their presence is
# reported until `instantiate` removes them (00-vault/conventions.md, ADR-0003).
CLONE_FILES = {"README.md"}
CLONE_DIRS = {"assets"}
CLONE_REPORT = ("not a vault note: the repository front page lives outside the vault; "
                "run `instantiate <owner> \"<title>\"` to remove it and its images")


def core_note(rel_str):
    parts = rel_str.split("/")
    return rel_str in CORE_FILES or parts[0] in CORE_DIRS or parts[-1] == "_index.md"


def expected_owner(rel_str):
    return CORE_OWNER if core_note(rel_str) else HUMAN_OWNER

# requirement-language.md licenses RFC 2119 keywords only in these note types.
LICENSED_TYPES = {"requirement", "constraint", "acceptance-criteria", "control", "gate", "stage"}
RFC_KEYWORDS = ["MUST NOT", "SHOULD NOT", "SHALL", "MUST", "SHOULD", "NEVER", "AVOID", "MAY"]

# Namespaces, ID widths, blocks, per-folder allocations, and spec folders are read from
# 00-vault/this-vault.json by configure() (00-vault/id-scheme.md, ADR-0003). They are declared
# here only so the module imports cleanly: a vault whose instantiation file is missing or
# malformed is reported by scan(), never checked against built-in defaults. Declaration order
# in the file is preserved, because register order and the ids ledger depend on it.
PREFIXES = ()
ID_WIDTH = {}
BLOCKS = {}
FOLDER_BLOCKS = {}
SPEC_INDEX_FOLDERS = set()

ID_BODY = "UNDEFINED"
ID_RE = re.compile(rf"\b(?:{ID_BODY})-\d{{1,4}}\b")
HEADING_ID_RE = re.compile(rf"^#{{2,4}}\s+((?:{ID_BODY})-\d{{1,4}})\b")
ROW_ID_RE = re.compile(rf"^\|\s*((?:{ID_BODY})-\d{{2,4}})\s*\|")
LINK_RE = re.compile(r"\]\(([^)\s]+)")
FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")

CONFIG_FILE = "00-vault/this-vault.json"
CONFIG_ERROR = None


def id_patterns(body):
    """The three ID-matching patterns, rebuilt whenever the namespace set changes."""
    return (re.compile(rf"\b(?:{body})-\d{{1,4}}\b"),
            re.compile(rf"^#{{2,4}}\s+((?:{body})-\d{{1,4}})\b"),
            re.compile(rf"^\|\s*((?:{body})-\d{{2,4}})\s*\|"))


def configure(root):
    """Load the vault's own instantiation file: owner name, namespaces, blocks, digit widths,
    folder allocations, spec folders. A missing or malformed file sets CONFIG_ERROR, which
    scan() reports as a problem instead of falling back to constants."""
    global HUMAN_OWNER, PREFIXES, ID_WIDTH, ID_BODY, ID_RE, HEADING_ID_RE, ROW_ID_RE
    global BLOCKS, FOLDER_BLOCKS, SPEC_INDEX_FOLDERS, CONFIG_ERROR
    path = Path(root) / CONFIG_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        CONFIG_ERROR = f"{CONFIG_FILE}: missing; namespaces, ID blocks, and the owner name are undefined"
        return
    except (OSError, ValueError) as exc:
        CONFIG_ERROR = f"{CONFIG_FILE}: unreadable ({exc})"
        return
    namespaces = data.get("namespaces") or {}
    if not namespaces:
        CONFIG_ERROR = f"{CONFIG_FILE}: defines no namespaces"
        return
    CONFIG_ERROR = None
    HUMAN_OWNER = data.get("owner") or "owner"
    PREFIXES = tuple(namespaces)
    ID_WIDTH = {p: int(spec.get("width", 3)) for p, spec in namespaces.items()}
    BLOCKS = {p: (int(spec["block"][0]), int(spec["block"][1])) for p, spec in namespaces.items()}
    FOLDER_BLOCKS = {folder: {p: (int(block[0]), int(block[1])) for p, block in blocks.items()}
                     for folder, blocks in (data.get("folder_blocks") or {}).items()}
    SPEC_INDEX_FOLDERS = set(data.get("spec_index_folders") or [])
    ID_BODY = "|".join(PREFIXES)
    ID_RE, HEADING_ID_RE, ROW_ID_RE = id_patterns(ID_BODY)


# Placeholders and markers are quoted as text in the notes that define them, so those
# notes are exempt: the rules police claim-bearing notes, not the convention notes.
MARKER_EXEMPT_DIRS = {"00-vault", "_templates", "_tools"}
MARKER_EXEMPT_FILES = set()

# No exceptions ship with the template: every mechanism note is written with its RFC 2119
# keywords in inline code, which strip_nonprose() drops before the keyword loop. An exception
# is added only for verbatim text quoted from an outside source, and clearing one needs the
# owner's agreement, not a script edit.
RFC_EXCEPTIONS = set()

problems = []
notes = []
defined = defaultdict(list)
authored = defaultdict(list)
mentioned = defaultdict(set)
status_count = defaultdict(int)
type_count = defaultdict(int)


def flag(path, line, text):
    problems.append(f"{path}:{line}: {text}")


def parse_frontmatter(lines, path=None):
    """Return (fields, body_start). Absent or unclosed frontmatter is flagged only when a
    path is given, so the helper can be used read-only by other tools."""
    if not lines or lines[0].strip() != "---":
        if path is not None:
            flag(path, 1, "missing frontmatter")
        return {}, 0
    meta = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return meta, i + 1
        m = FIELD_RE.match(lines[i])
        if m:
            meta[m.group(1)] = m.group(2).strip()
    if path is not None:
        flag(path, 1, "frontmatter is not closed")
    return {}, 0


def strip_nonprose(lines):
    """Drop fenced blocks, inline code, link text and targets, and quoted spans."""
    out, fenced = [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        if fenced:
            out.append("")
            continue
        ln = re.sub(r"`[^`]*`", "", ln)
        ln = re.sub(r"\[[^\]]*\]\([^)]*\)", "", ln)
        ln = re.sub(r"\[\[[^\]]*\]\]", "", ln)
        ln = re.sub(r"“[^”]*”", "", ln)
        ln = re.sub(r"\"[^\"]*\"", "", ln)
        out.append(ln)
    return out


def iter_notes(root):
    """Yield (rel_str, path, meta, lines, body_start) for every markdown note in the vault."""
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if str(rel) in CLONE_FILES or rel.parts[0] in CLONE_DIRS:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        meta, body_start = parse_frontmatter(lines)
        yield str(rel), path, meta, lines, body_start


def body_lines(lines, body_start):
    return lines[body_start:]


def scan(root):
    problems.clear()
    notes.clear()
    defined.clear()
    authored.clear()
    mentioned.clear()
    status_count.clear()
    type_count.clear()
    configure(root)
    if CONFIG_ERROR:
        problems.append(CONFIG_ERROR)
    for name in sorted(CLONE_FILES):
        if (root / name).exists():
            flag(name, 1, CLONE_REPORT)

    for rel_str, path, meta, lines, body_start in iter_notes(root):
        rel = Path(rel_str)
        folder = rel.parts[0] if len(rel.parts) > 1 else ""
        body_lines_here = body_lines(lines, body_start)
        body = "\n".join(body_lines_here)
        notes.append((rel, meta))
        marker_exempt = folder in MARKER_EXEMPT_DIRS or rel_str in MARKER_EXEMPT_FILES

        for field in REQUIRED_FIELDS:
            if field not in meta:
                flag(rel, 1, f"missing frontmatter field: {field}")
        expected = expected_owner(rel_str)
        if meta.get("owner") != expected:
            kind = "core" if core_note(rel_str) else "content"
            flag(rel, 1, f"owner is {meta.get('owner') or 'unset'}, expected {expected} for a {kind} note")
        if meta.get("type") and meta["type"] not in TYPES:
            flag(rel, 1, f"illegal type: {meta['type']}")
        if meta.get("status") and meta["status"] not in STATUSES:
            flag(rel, 1, f"illegal status: {meta['status']}")
        if meta.get("updated") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["updated"]):
            flag(rel, 1, f"updated is not an ISO date: {meta['updated']}")

        nid = meta.get("id", "")
        if nid:
            status_count[meta.get("status", "?")] += 1
            type_count[meta.get("type", "?")] += 1
            defined[nid].append((rel_str, 1))
            authored[nid].append((rel_str, 1))
            m = re.fullmatch(rf"({'|'.join(PREFIXES)})-(\d{{1,4}})", nid)
            if m and folder != "_templates":
                prefix, number = m.group(1), int(m.group(2))
                lo, hi = FOLDER_BLOCKS.get(folder, {}).get(prefix, BLOCKS[prefix])
                if not lo <= number <= hi:
                    flag(rel, 1, f"id {nid} outside the block for {folder or rel_str} ({lo}-{hi})")

        for n, ln in enumerate(lines, 1):
            m = HEADING_ID_RE.match(ln)
            if m:
                defined[m.group(1)].append((rel_str, n))
                authored[m.group(1)].append((rel_str, n))
                continue
            m = ROW_ID_RE.match(ln)
            if m:
                defined[m.group(1)].append((rel_str, n))

        for m in ID_RE.finditer(body):
            mentioned[m.group(0)].add(rel_str)

        for m in LINK_RE.finditer(body):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#", "obsidian://")):
                continue
            target = target.split("#")[0].split("?")[0].strip("<>").replace("%20", " ")
            if not target:
                continue
            if not (path.parent / target).exists():
                line = body[:m.start()].count("\n") + body_start + 1
                flag(rel, line, f"broken link: {m.group(1)}")

        for n, ln in enumerate(lines, 1):
            if "requirement-language.md" in rel.parts:
                continue
            for bad in ("<TBD>", "TODO", "FIXME"):
                if bad in ln:
                    flag(rel, n, f"placeholder {bad}")
            if "<<" in ln and not marker_exempt:
                flag(rel, n, "template fill-in marker outside _templates/")
            if "[INFERENCE]" in ln and meta.get("status") == "accepted" and not marker_exempt:
                flag(rel, n, "[INFERENCE] inside an accepted note")
            for m in re.finditer(r"\bADR-\d+\b", ln):
                if not re.fullmatch(r"ADR-\d{4}", m.group(0)):
                    flag(rel, n, f"malformed decision reference: {m.group(0)}")

        if meta.get("type") and meta["type"] not in LICENSED_TYPES:
            for n, ln in enumerate(strip_nonprose(body_lines_here), body_start + 1):
                hits = [k for k in RFC_KEYWORDS if re.search(rf"\b{k}\b", ln)]
                if hits and (rel_str, n) not in RFC_EXCEPTIONS:
                    flag(rel, n, f"RFC 2119 keyword in a {meta['type']} note: {', '.join(hits)}")

    for folder in sorted({n[0].parts[0] for n in notes if len(n[0].parts) > 1}):
        if folder in SKIP_DIRS:
            continue
        index = root / folder / "_index.md"
        if not index.exists():
            problems.append(f"{folder}/_index.md: missing folder instruction file")
            continue
        itext = index.read_text(encoding="utf-8")
        if folder in SPEC_INDEX_FOLDERS:
            for section in ("## Evidence", "## Open issues"):
                if section not in itext:
                    problems.append(f"{folder}/_index.md: missing {section}")
            if re.search(r"^status:\s*accepted", itext, re.M):
                problems.append(f"{folder}/_index.md: a spec-folder index is accepted")

    for nid, spots in sorted(authored.items()):
        files = {s[0] for s in spots}
        if len(files) > 1:
            problems.append(f"{nid}: defined in {len(files)} notes: {', '.join(sorted(files))}")

    return {
        "root": root,
        "notes": notes,
        "defined": defined,
        "authored": authored,
        "mentioned": mentioned,
        "status_count": status_count,
        "type_count": type_count,
        "undefined": sorted(nid for nid in mentioned if nid not in defined),
        "problems": problems,
    }


def main():
    result = scan(ROOT)
    print(f"vault: {result['root']}")
    print(f"notes: {len(result['notes'])}")
    print("statuses: " + ", ".join(f"{k} {v}" for k, v in sorted(result["status_count"].items())))
    print("types: " + ", ".join(f"{k} {v}" for k, v in sorted(result["type_count"].items())))
    print(f"defined ids: {len(result['defined'])}")
    undefined = result["undefined"]
    print(f"mentioned ids with no definition ({len(undefined)}): " + ", ".join(undefined))
    print("problems:")
    for p in result["problems"]:
        print(f"  {p}")
    print(f"PROBLEMS: {len(result['problems'])}")
    return 1 if result["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
