#!/usr/bin/env python3
"""Vault check and query commands for an ideation vault.

Tooling, not a note: no frontmatter, no ID, never cited as evidence (ADR-0005).
The rules reported here are read from _tools/vault_scan.py, which restates
00-vault/conventions.md, 00-vault/id-scheme.md, 00-vault/status-model.md,
00-vault/requirement-language.md, 00-vault/userspace.md, and 00-vault/reshaping.md.
A disagreement between this script and those notes is a defect in this script.

Namespaces, ID blocks, digit widths, and the owner's name come from
00-vault/this-vault.json (ADR-0003); this script ships no vault-specific constants.

Run: python3 _tools/vault.py <command> [args]      (see -h on any command)
"""

import argparse
import datetime as dt
import json
import re
import shutil
import signal
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vault_scan as vs  # noqa: E402  (same folder, shared rule set)

TODAY = dt.date.today().isoformat()

# ADR-0004: these do not belong in the readable body of an issued instance - vault machinery,
# status or ownership language, and unfinished-work markers. Matching is case-insensitive where
# the term is already lowercase, anchored at word characters. Bare "superseded" is not banned:
# an instance may describe its own markers, so only the field name `superseded-by` is. Namespace
# prefixes are not listed here because vs.ID_RE already catches every ID this vault declares,
# and the owner's name is not banned: naming an author is not a leak of vault machinery.
OUTPUT_TERMS = [
    "[INFERENCE]", "[BLOCKED", "<TBD>", "TODO", "FIXME", "<<",
    "## Evidence", "## Open issues", "the vault", "this vault",
    "status: ", "superseded-by",
]
WORD_BUDGET_RE = re.compile(r"(\d[\d,]*)\s+to\s+(\d[\d,]*)\s+words")
LINK_RE = vs.LINK_RE
SKIP_SCHEMES = ("http://", "https://", "mailto:", "#", "obsidian://")


def term_regex(term):
    """Banned-term matcher: word-boundary anchored at word characters only, so
    `vault` does not match `vaulting` while `OQ-` and `## Evidence` still match."""
    pattern = re.escape(term)
    if re.match(r"\w", term[0]):
        pattern = r"\b" + pattern
    if re.search(r"\w$", term):
        pattern += r"\b"
    return re.compile(pattern, re.I if term.lower() == term else 0)


def fail(message):
    print(message)
    print("PROBLEMS: 1")
    return 1


def today():
    return dt.date.today()


class Note:
    def __init__(self, rel, path, meta, lines, body_start):
        self.rel = rel
        self.path = path
        self.meta = meta
        self.lines = lines
        self.body_start = body_start
        self.folder = rel.split("/")[0] if "/" in rel else ""

    @property
    def id(self):
        return self.meta.get("id", "")

    @property
    def type(self):
        return self.meta.get("type", "")

    @property
    def status(self):
        return self.meta.get("status", "")

    @property
    def title(self):
        return self.meta.get("title", "")

    @property
    def body(self):
        return "\n".join(self.lines[self.body_start:])

    @property
    def links(self):
        raw = self.meta.get("links", "")
        return [x.strip() for x in raw.strip("[] ").split(",") if x.strip()]

    @property
    def tags(self):
        raw = self.meta.get("tags", "")
        return [x.strip() for x in raw.strip("[] ").split(",") if x.strip()]

    def word_count(self, prose=False):
        text = "\n".join(vs.strip_nonprose(self.lines[self.body_start:])) if prose else self.body
        return len([w for w in text.split() if w.strip("|-#>")])

    def resolve(self, target):
        """Resolve a relative markdown link target against this note's folder."""
        cleaned = target.split("#")[0].split("?")[0].strip("<>").replace("%20", " ")
        if not cleaned:
            return None
        return (self.path.parent / cleaned).resolve()


class Vault:
    def __init__(self, root):
        self.root = Path(root).resolve()
        vs.configure(self.root)  # namespaces, blocks, and the owner name before anything reads them
        self.notes = []
        self.by_id = {}
        self.by_path = {}
        for rel, path, meta, lines, body_start in vs.iter_notes(self.root):
            note = Note(rel, path, meta, lines, body_start)
            self.notes.append(note)
            self.by_id.setdefault(note.id, note)
            self.by_path.setdefault(note.rel, note)
        # Headings and table rows define ids too, so the ledger comes from the scan.
        self.scan_result = vs.scan(self.root)
        self.defined = self.scan_result["defined"]

    def content(self):
        """Vault notes minus the _templates fill-in shapes."""
        return [n for n in self.notes if n.folder != "_templates"]

    def select(self, folders=None, types=None, statuses=None, tags=None, ids=None,
               skip_index=False, skip_templates=True):
        out = []
        for n in self.notes:
            if skip_templates and n.folder == "_templates":
                continue
            if skip_index and n.type == "index":
                continue
            if folders and n.folder not in folders:
                continue
            if types and n.type not in types:
                continue
            if statuses and n.status not in statuses:
                continue
            if tags and not set(tags) & set(n.tags):
                continue
            if ids and n.id not in ids:
                continue
            out.append(n)
        return out

    def git(self, *args):
        proc = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True)
        if proc.returncode:
            raise SystemExit(f"git {' '.join(args)}: {proc.stderr.strip()}")
        return proc.stdout.splitlines()

    def changed_paths(self, staged=False):
        """Markdown paths git reports as changed: the working tree, or the index when staged.
        The repository front page is not a note, so it is never a note to stamp or to check."""
        if staged:
            return [p for p in self.git("diff", "--cached", "--name-only")
                    if p.endswith(".md") and p not in vs.CLONE_FILES]
        out = []
        for line in self.git("status", "--short", "-uall"):
            if not line.strip():
                continue
            path = line[3:].strip().strip('"').split(" -> ")[-1]
            if path.endswith(".md") and path not in vs.CLONE_FILES:
                out.append(path)
        return out

    def numbers(self, prefix):
        """Numbers defined for a namespace, grouped by the folder that defines them.
        _templates placeholders (the -000 ids) are not allocations and are skipped."""
        used = defaultdict(set)
        for nid, spots in self.defined.items():
            m = re.fullmatch(rf"({'|'.join(vs.PREFIXES)})-(\d{{1,4}})", nid)
            if not m or m.group(1) != prefix:
                continue
            folders = {spot[0].split("/")[0] for spot in spots} - {"_templates"}
            for folder in folders:
                used[folder].add(int(m.group(2)))
        return used

    def allocated(self, prefix):
        taken = set()
        for numbers in self.numbers(prefix).values():
            taken |= numbers
        return taken

    def owners(self, prefix):
        """Folders whose recorded block allocates this namespace."""
        return {f for f, blocks in vs.FOLDER_BLOCKS.items() if prefix in blocks}

    def next_id(self, prefix, folder=None):
        block = vs.FOLDER_BLOCKS.get(folder or "", {}).get(prefix, vs.BLOCKS.get(prefix))
        if not block:
            return None
        lo, hi = block
        taken = self.allocated(prefix) | self.numbers(prefix).get(folder or "", set())
        for number in range(lo, hi + 1):
            if number not in taken:
                return f"{prefix}-{number:0{vs.ID_WIDTH.get(prefix, 3)}d}"
        return None


def emit(rows, header=None):
    if header:
        print(header)
    for row in rows:
        print(row)


def cmd_check(vault, args):
    result = vault.scan_result
    for problem in result["problems"]:
        print(problem)
    print(f"PROBLEMS: {len(result['problems'])}")
    return 1 if result["problems"] else 0


def cmd_status(vault, args):
    result = vault.scan_result
    print(f"vault: {vault.root}")
    print(f"notes: {len(vault.notes)}  (vault content {len(vault.content())}, templates {len(vault.notes) - len(vault.content())})")
    print("statuses: " + ", ".join(f"{k} {v}" for k, v in sorted(result["status_count"].items())))
    print("types: " + ", ".join(f"{k} {v}" for k, v in sorted(result["type_count"].items())))
    print(f"defined ids: {len(result['defined'])}")
    undefined = result["undefined"]
    print(f"mentioned ids with no definition ({len(undefined)}): " + ", ".join(undefined))
    counts = defaultdict(int)
    for n in vault.notes:
        counts[n.folder or "."] += 1
    print("folders: " + ", ".join(f"{f} {c}" for f, c in sorted(counts.items())))
    print("headroom:")
    for prefix, (lo, hi) in sorted(vs.BLOCKS.items()):
        used = vault.numbers(prefix)
        total = sum(len(v) for v in used.values())
        detail = ", ".join(f"{f} {min(v)}-{max(v)}" for f, v in sorted(used.items()) if v)
        print(f"  {prefix}: {lo}-{hi}, {total} allocated, next free "
              f"{vault.next_id(prefix) or 'exhausted'}" + (f"  [{detail}]" if detail else ""))
    print(f"PROBLEMS: {len(result['problems'])}")
    return 1 if result["problems"] else 0


def cmd_metrics(vault, args):
    """Health numbers for other tools to read: one key=value per line, keys are stable."""
    result = vault.scan_result
    inbound, broken = link_graph(vault)
    due_now = review_now = 0
    for n in vault.content():
        if n.status == "archived":
            continue
        if n.meta.get("due", "") and n.meta["due"] <= TODAY:
            due_now += 1
        if n.meta.get("review", "") and n.meta["review"] <= TODAY:
            review_now += 1
    questions = vault.select(types=["open-question"], skip_index=True)
    decisions = vault.select(types=["decision"], skip_index=True)
    instances = issued_instances(vault)
    over_budget = sum(1 for n in instances
                      if budget_of(vault, n)
                      and not (budget_of(vault, n)[0] <= n.word_count() <= budget_of(vault, n)[1]))
    exhausted = [prefix for prefix in sorted(vs.BLOCKS) if vault.next_id(prefix) is None]
    values = {
        "notes": len(vault.notes),
        "content_notes": len(vault.content()),
        "templates": len(vault.notes) - len(vault.content()),
        "defined_ids": len(result["defined"]),
        "undefined_ids": len(result["undefined"]),
        "open_questions": sum(1 for n in questions if n.status != "archived"),
        "decisions": len(decisions),
        "claims": sum(1 for n in vault.select(types=["requirement", "constraint", "assumption",
                                                     "acceptance-criteria"], skip_index=True)),
        "due_at_or_before_today": due_now,
        "review_at_or_before_today": review_now,
        "broken_links": len(broken),
        "unlinked_notes": len(unlinked_notes(vault, inbound)),
        "changed_notes": len(vault.changed_paths()),
        "output_instances": len(instances),
        "output_instances_over_budget": over_budget,
        "numbering_exhausted": ",".join(exhausted) if exhausted else "none",
        "scan_problems": len(result["problems"]),
    }
    for name, status in sorted(result["status_count"].items()):
        values[f"status_{name}"] = status
    for prefix in sorted(vs.BLOCKS):
        values[f"next_free_{prefix}"] = vault.next_id(prefix) or "none"
    for key, value in values.items():
        print(f"{key}={value}")
    print(f"PROBLEMS: {len(result['problems'])}")
    return 1 if result["problems"] else 0


def cmd_changed(vault, args):
    paths = vault.changed_paths(staged=args.staged)
    if not paths:
        print("no changed markdown files")
        print("PROBLEMS: 0")
        return 0
    problems = []
    dates = defaultdict(int)
    for rel in paths:
        note = vault.by_path.get(rel)
        if note is None:
            print(f"{rel}: not a parsed note")
            problems.append(rel)
            continue
        updated = note.meta.get("updated", "")
        dates[updated] += 1
        line = f"{rel}: type={note.type} status={note.status} updated={updated} title={note.title}"
        hits = []
        if note.type not in vs.LICENSED_TYPES:
            for i, ln in enumerate(vs.strip_nonprose(note.lines[note.body_start:]), note.body_start + 1):
                if (rel, i) in vs.RFC_EXCEPTIONS:
                    continue
                hits.extend(k for k in vs.RFC_KEYWORDS if re.search(rf"\b{k}\b", ln))
        if hits:
            line += f"  RFC:{','.join(sorted(set(hits)))}"
            problems.append(f"{rel}: RFC keyword in a {note.type} note")
        print(line)
    print("updated values: " + ", ".join(f"{k or 'missing'} {v}" for k, v in sorted(dates.items())))
    if args.date:
        for rel in paths:
            note = vault.by_path.get(rel)
            if note and note.meta.get("updated") != args.date:
                problems.append(f"{rel}: updated is {note.meta.get('updated')}, expected {args.date}")
    for p in sorted(set(problems)):
        print(f"  {p}")
    print(f"PROBLEMS: {len(set(problems))}")
    return 1 if problems else 0


def cmd_words(vault, args):
    notes = resolve_notes(vault, args.files)
    if not notes and args.files:
        return fail("no such note")
    if not notes:
        notes = issued_instances(vault)
    if not notes:
        return empty_output_report()
    problems = 0
    for n in notes:
        words = n.word_count()
        line = f"{n.rel}: {words} words"
        budget = budget_of(vault, n)
        if budget:
            lo, hi = budget
            ok = lo <= words <= hi
            line += f"  budget {lo}-{hi} {'ok' if ok else 'OUT OF BUDGET'}"
            problems += 0 if ok else 1
        print(line)
        if args.sections:
            for title, count in section_words(n):
                print(f"    {count:6}  {title}")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def section_words(note):
    """Words under each `## ` heading of the body."""
    out, title, count = [], None, 0
    for line in note.lines[note.body_start:]:
        if line.startswith("## "):
            if title is not None:
                out.append((title, count))
            title, count = line[3:].strip(), 0
            continue
        if title is not None:
            count += len([w for w in line.split() if w.strip("|-#>")])
    if title is not None:
        out.append((title, count))
    return out


def budget_of(vault, note):
    """Read the word budget from the note's output-kind definition, if it has one."""
    kind_id = next((l for l in note.links if l.startswith("OUT-")), None)
    kind = vault.by_id.get(kind_id)
    if kind is None:
        return None
    m = WORD_BUDGET_RE.search(kind.body)
    if not m:
        return None
    return (int(m.group(1).replace(",", "")), int(m.group(2).replace(",", "")))


def resolve_notes(vault, files):
    out = []
    for f in files:
        path = Path(f)
        rel = str(path.relative_to(vault.root)) if path.is_absolute() else f
        note = vault.by_path.get(rel)
        if note is None:
            matches = [n for n in vault.notes if n.rel.endswith(rel)]
            if not matches:
                print(f"{f}: no such note")
                continue
            out.extend(matches)
        else:
            out.append(note)
    return out


def issued_instances(vault):
    """Every note under an `issued/` folder: the generated instances of any declared kind."""
    return [n for n in vault.content() if "/issued/" in n.rel and n.type != "index"]


def empty_output_report():
    """The clean answer when a vault has generated nothing in any kind yet."""
    print("no issued outputs: nothing has been generated in any kind yet")
    print("PROBLEMS: 0")
    return 0


def cmd_noise(vault, args):
    terms = list(OUTPUT_TERMS) + (args.term or [])
    notes = resolve_notes(vault, args.files)
    if not notes and args.files:
        return fail("no such note")
    if not notes:
        notes = issued_instances(vault)
    if not notes:
        return empty_output_report()
    problems = 0
    for n in notes:
        body, hits = n.body, []
        for term in terms:
            for m in term_regex(term).finditer(body):
                hits.append((body[:m.start()].count("\n") + n.body_start + 1, term))
        for m in vs.ID_RE.finditer(body):
            hits.append((body[:m.start()].count("\n") + n.body_start + 1, m.group(0)))
        for keyword in vs.RFC_KEYWORDS:
            for m in re.finditer(rf"\b{keyword}\b", "\n".join(vs.strip_nonprose(n.lines[n.body_start:]))):
                hits.append((0, keyword))
        if hits:
            problems += 1
            print(f"{n.rel}: {len(hits)} banned hits")
            for line, term in sorted(set(hits)):
                print(f"  {n.rel}:{line or '-'}: {term}")
        else:
            print(f"{n.rel}: clean")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def cmd_audit(vault, args):
    instances = resolve_notes(vault, args.files)
    if not instances and args.files:
        return fail("no such note")
    if not instances:
        instances = issued_instances(vault)
    if not instances:
        return empty_output_report()
    problems = 0
    for n in instances:
        notes_problems = []
        kind_id = next((l for l in n.links if l.startswith("OUT-")), None)
        kind = vault.by_id.get(kind_id)
        if kind is None:
            notes_problems.append("no OUT-* kind in links")
        register = vault.by_path.get(str(Path(n.rel).parent / "_index.md"))
        words = n.word_count()
        budget = budget_of(vault, n)
        if budget and not (budget[0] <= words <= budget[1]):
            notes_problems.append(f"{words} words outside budget {budget[0]}-{budget[1]}")
        if n.status not in ("draft", "accepted"):
            notes_problems.append(f"status is {n.status}, expected draft or accepted")
        if n.meta.get("owner") != vs.HUMAN_OWNER:
            notes_problems.append(f"owner is not {vs.HUMAN_OWNER}")
        if register and n.path.name not in register.body:
            notes_problems.append("not recorded in issued/_index.md")
        terms = list(OUTPUT_TERMS)
        for term in terms:
            if term_regex(term).search(n.body):
                notes_problems.append(f"banned term: {term}")
        for m in vs.ID_RE.finditer(n.body):
            notes_problems.append(f"vault id in body: {m.group(0)}")
        for k in vs.RFC_KEYWORDS:
            if re.search(rf"\b{k}\b", "\n".join(vs.strip_nonprose(n.lines[n.body_start:]))):
                notes_problems.append(f"RFC keyword in body: {k}")
        verdict = "PASS" if not notes_problems else "FAIL"
        problems += 0 if not notes_problems else 1
        print(f"{verdict} {n.rel}  kind={kind_id or '?'}  {words} words"
              + (f"  budget {budget[0]}-{budget[1]}" if budget else ""))
        for p in notes_problems:
            print(f"  {p}")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def ids_namespace(vault, prefix):
    lo, hi = vs.BLOCKS[prefix]
    used = vault.numbers(prefix)
    owners = vault.owners(prefix)
    print(f"{prefix}: block {lo}-{hi}, {len(vault.allocated(prefix))} allocated, "
          f"next free {vault.next_id(prefix) or 'exhausted'}")
    problems = 0
    for folder, allocated in sorted(used.items()):
        low, high = min(allocated), max(allocated)
        if folder not in owners:
            print(f"  {folder}: {low}-{high} ({len(allocated)}) cross-listed")
            continue
        holes = sorted(n for n in range(low, high + 1) if n not in allocated)
        print(f"  {folder}: {low}-{high} ({len(allocated)})"
              + (f", gaps {', '.join(str(h) for h in holes)}" if holes else ""))
        problems += len(holes)
    return problems


def ids_where(vault, nid):
    spots = vault.defined.get(nid, [])
    print(f"{nid}: " + (", ".join(f"{rel}:{line}" for rel, line in spots) if spots else "no definition"))
    defining = {rel for rel, _ in spots}
    emit(sorted(n.rel for n in vault.content()
                if re.search(rf"\b{re.escape(nid)}\b", n.body) and n.rel not in defining),
         "mentioned in:")
    print(f"PROBLEMS: {0 if spots else 1}")
    return 0 if spots else 1


def cmd_ids(vault, args):
    target = args.target
    if target:
        if target in vs.BLOCKS:
            problems = ids_namespace(vault, target)
            print(f"PROBLEMS: {problems}")
            return 1 if problems else 0
        if re.fullmatch(rf"({'|'.join(vs.PREFIXES)})-\d{{1,4}}", target):
            return ids_where(vault, target)
        return fail(f"unknown namespace or id: {target} (namespaces: {', '.join(sorted(vs.BLOCKS))})")
    problems = sum(ids_namespace(vault, prefix) for prefix in vs.BLOCKS)
    emit(vault.scan_result["undefined"], "mentioned with no definition:")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def cmd_next(vault, args):
    nid = vault.next_id(args.prefix, args.folder)
    print(nid or f"no free {args.prefix} number" + (f" for {args.folder}" if args.folder else ""))
    print(f"PROBLEMS: {0 if nid else 1}")
    return 0 if nid else 1


def cmd_find(vault, args):
    pattern = args.pattern
    rx = re.compile(pattern if args.regex else re.escape(pattern), re.I)
    rows = []
    for n in vault.select(folders=args.folder, types=args.type, statuses=args.status,
                          tags=args.tag):
        haystacks = []
        if args.field:
            haystacks.append((args.field, n.meta.get(args.field, "")))
        else:
            haystacks.append(("title", n.title))
            haystacks.append(("id", n.id))
            haystacks.append(("body", n.body))
            for key, value in n.meta.items():
                if key not in ("title", "id", "body"):
                    haystacks.append((key, value))
        hits = [(field, value) for field, value in haystacks if rx.search(value)]
        if not hits:
            continue
        rows.append(f"{n.rel}  type={n.type} status={n.status} id={n.id}")
        if args.full:
            for number, line in enumerate(n.lines, 1):
                if rx.search(line):
                    rows.append(f"    {number}: {line.strip()[:160]}")
    emit(rows)
    print(f"matches: {len([r for r in rows if not r.startswith('    ')])}")
    print("PROBLEMS: 0")
    return 0


def link_graph(vault):
    """Inbound markdown links per note, plus the links whose target does not exist."""
    inbound, broken = defaultdict(set), []
    for n in vault.content():
        for m in LINK_RE.finditer(n.body):
            target = m.group(1)
            if target.startswith(SKIP_SCHEMES):
                continue
            resolved = n.resolve(target)
            if resolved is None:
                continue
            try:
                rel = str(resolved.relative_to(vault.root))
            except ValueError:
                continue
            if resolved.exists():
                inbound[rel].add(n.rel)
            else:
                broken.append(f"{n.rel}: {target}")
    return inbound, broken


def unlinked_notes(vault, inbound):
    """Content notes no other note links to or mentions by ID. Indexes are exempt."""
    content = vault.content()
    out = []
    for n in content:
        if n.type == "index" or inbound.get(n.rel):
            continue
        if n.id and any(m.rel != n.rel and re.search(rf"\b{re.escape(n.id)}\b", m.body)
                        for m in content):
            continue
        out.append(n.rel)
    return out


def cmd_links(vault, args):
    inbound, broken = link_graph(vault)
    target = args.target
    if target:
        if target.endswith(".md") or "/" in target:
            try:
                rel = str((vault.root / target).resolve().relative_to(vault.root))
            except ValueError:
                return fail(f"outside the vault: {target}")
            emit(sorted(inbound.get(rel, [])), f"{rel} is linked from:")
            print(f"PROBLEMS: 0")
            return 0
        emit(sorted(n.rel for n in vault.content()
                    if re.search(rf"\b{re.escape(target)}\b", n.body)),
             f"{target} is mentioned in:")
        print(f"PROBLEMS: 0")
        return 0
    orphans = unlinked_notes(vault, inbound)
    emit(sorted(broken), "broken links:")
    emit(sorted(orphans), "notes no other note links to or mentions:")
    counts = sorted(((len(v), k) for k, v in inbound.items()), reverse=True)
    emit([f"{c} {k}" for c, k in counts[:15]], "most-linked notes:")
    problems = len(broken) + len(orphans)
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def cmd_oq(vault, args):
    questions = sorted(vault.select(types=["open-question"], skip_index=True), key=lambda n: n.id)
    rows, problems, open_count = [], 0, 0
    for n in questions:
        due = n.meta.get("due", "")
        closed = n.meta.get("superseded-by", "")
        if n.status != "archived":
            open_count += 1
        rows.append(f"{n.id}  {n.status:9}  due {due or '-':10}  "
                    + (f"closed by {closed}  " if closed else "") + n.title)
        if not due and n.status != "archived":
            rows.append(f"    {n.id}: no due date")
            problems += 1
    emit(rows)
    print(f"open questions: {open_count}  (of {len(questions)})")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def cmd_adr(vault, args):
    decisions = sorted(vault.select(types=["decision"], skip_index=True), key=lambda n: n.id)
    by_next = {}
    for n in decisions:
        for target in re.findall(r"ADR-\d{4}", n.meta.get("supersedes", "")):
            by_next[target] = n.id
    problems = 0
    for n in decisions:
        supersedes = re.findall(r"ADR-\d{4}", n.meta.get("supersedes", ""))
        superseded_by = re.findall(r"ADR-\d{4}", n.meta.get("superseded-by", ""))
        print(f"{n.id}  {n.status:11}  {n.title}")
        if supersedes:
            print(f"    supersedes: {', '.join(supersedes)}")
        if superseded_by:
            print(f"    superseded-by: {', '.join(superseded_by)}")
        for target in supersedes + superseded_by:
            if target not in vault.by_id:
                print(f"    dangling reference: {target}")
                problems += 1
        for target in supersedes:
            other = vault.by_id[target]
            if other.type != "decision":
                print(f"    {target} is a {other.type}, not a decision")
                problems += 1
        if n.status == "accepted" and "Status:" not in n.body:
            print("    accepted decision carries no Status: line")
            problems += 1
    starts = sorted(n for n in by_next if n not in set(by_next.values()))
    for start in starts:
        chain, cursor, guard = [start], by_next[start], 0
        while cursor and guard < 50:
            chain.append(cursor)
            cursor = by_next.get(cursor)
            guard += 1
        print("superseded: " + " -> ".join(chain))
    print(f"decisions: {len(decisions)}  superseding chains: {len(starts)}")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def cmd_due(vault, args):
    as_of = args.date
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of):
        return fail(f"date is not ISO: {as_of}")
    rows, problems = [], 0
    for n in vault.content():
        for field in ("due", "review"):
            value = n.meta.get(field)
            if not value or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                continue
            if value <= as_of:
                rows.append(f"{value}  {field:6}  {n.status:11}  {n.rel}  {n.title}")
                if field == "due" and n.status != "archived":
                    problems += 1
    if args.stale:
        cutoff = (dt.date.fromisoformat(as_of) - dt.timedelta(days=args.stale)).isoformat()
        for n in vault.content():
            updated = n.meta.get("updated", "")
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated) and updated < cutoff:
                rows.append(f"{updated}  updated  {n.status:11}  {n.rel}  {n.title}")
    emit(sorted(rows))
    print(f"entries: {len(rows)}")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def cmd_stamp(vault, args):
    if args.changed:
        paths = vault.changed_paths()
        if not paths:
            print("no changed notes to stamp")
            print("PROBLEMS: 0")
            return 0
    else:
        paths = args.files
        if not paths:
            return fail("no files given (use files or --changed)")
    date = TODAY
    changed, problems = 0, 0
    for rel in paths:
        note = vault.by_path.get(rel)
        if note is None:
            print(f"{rel}: no such note")
            problems += 1
            continue
        current = note.meta.get("updated")
        if current is None:
            print(f"{rel}: no updated field")
            problems += 1
            continue
        if current == date:
            continue
        for index in range(1, note.body_start):
            if note.lines[index].startswith("updated:"):
                if args.dry_run:
                    print(f"{rel}:{index + 1}: {note.lines[index]} -> updated: {date}")
                else:
                    text = note.path.read_text(encoding="utf-8")
                    note.path.write_text(text.replace(note.lines[index], f"updated: {date}", 1),
                                         encoding="utf-8")
                    print(f"{rel}: updated {current} -> {date}")
                changed += 1
                break
    print(f"stamped: {changed}")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def cmd_scaffold(vault, args):
    if args.type not in vs.TYPES:
        return fail(f"unknown type {args.type} (types: {', '.join(sorted(vs.TYPES))})")
    prefix = default_prefix(args.type)
    folder = args.folder or "<folder>"
    owner = vs.CORE_OWNER if (args.folder or "") in vs.CORE_DIRS else vs.HUMAN_OWNER
    if prefix:
        nid = vault.next_id(prefix, args.folder)
        if not nid:
            return fail(f"no free {prefix} number" + (f" for {args.folder}" if args.folder else ""))
        hint = f"next free {prefix} id: {nid}; save as {folder}/{nid.lower()}-<slug>.md"
    else:
        nid = "<TAG>-<TOPIC>"
        handles = []
        if args.folder:
            handles = sorted(n.id for n in vault.content()
                             if n.folder == args.folder and n.id
                             and not re.search(r"-\d{1,4}$", n.id)
                             and not n.id.endswith("-REG") and not n.id.startswith("IDX-"))
        hint = (f"{args.type} notes take a descriptive handle (<TAG>-<TOPIC>, 00-vault/id-scheme.md); "
                f"handles in {folder}: " + (", ".join(handles) if handles else "none yet"))
    template = vault.root / "_templates" / f"{args.type}.md"
    fillins = "# <<...>> fill-ins and -000 placeholder ids are legal only inside _templates/: replace them before saving."
    if template.exists():
        text = template.read_text(encoding="utf-8")
        for pattern, replacement in ((r"^id:.*$", f"id: {nid}"),
                                     (r"^type:.*$", f"type: {args.type}"),
                                     (r"^title:.*$", f"title: {args.title}"),
                                     (r"^owner:.*$", f"owner: {owner}"),
                                     (r"^updated:.*$", f"updated: {TODAY}"),
                                     (r"^# .*$", f"# {nid}: {args.title}")):
            text = re.sub(pattern, replacement, text, count=1, flags=re.M)
        print(text)
        print(f"# {hint}")
        print(fillins)
        print("PROBLEMS: 0")
        return 0
    print("---")
    print(f"id: {nid}")
    print(f"type: {args.type}")
    print(f"title: {args.title}")
    print("status: draft")
    print(f"owner: {owner}")
    print(f"updated: {TODAY}")
    print(f"tags: [{args.type}]")
    print("links: []")
    print("---\n")
    print(f"# {nid}: {args.title}\n")
    print("Purpose: <<one sentence stating what the note is for.>>\n")
    print("<<Body in ## sections, per 00-vault/conventions.md.>>\n")
    print("## Evidence\n\n<<`FND-###` and `S-###` IDs this note relies on.>>\n")
    print("## Open issues\n\n<<`OQ-###` IDs that block this note from reaching `accepted`.>>")
    print(f"# {hint}\n{fillins}")
    print("PROBLEMS: 0")
    return 0


# The namespace a note type conventionally allocates from. The vault's declared blocks
# (00-vault/this-vault.json) decide whether a number is available; a type mapped to a
# namespace this vault does not declare fails with "no free <PREFIX> number" rather than
# inventing one.
TYPE_PREFIX = {
    "requirement": "REQ", "constraint": "CON", "assumption": "ASM",
    "acceptance-criteria": "AC", "component": "CMP", "interface": "IF",
    "risk": "RSK", "control": "CTL", "stage": "STG", "role": "ROLE",
    "gate": "GATE", "metric": "MET", "finding": "FND", "source": "S",
    "decision": "ADR", "open-question": "OQ",
    "note": None, "index": None, "glossary": None, "template": None,
}


def default_prefix(note_type):
    """The numeric namespace for a note type; None when the type uses a descriptive handle."""
    return TYPE_PREFIX.get(note_type)


def id_sort_key(nid):
    """Register order: the namespace order of 00-vault/id-scheme.md, then the id."""
    for position, prefix in enumerate(vs.PREFIXES):
        if nid.startswith(prefix + "-"):
            return (position, nid)
    return (len(vs.PREFIXES), nid)


def collapse_ids(ids):
    """Runs of three or more consecutive numbers in one namespace become S-016..S-019."""
    out, index = [], 0
    while index < len(ids):
        head = ids[index].rpartition("-")[0]
        run = [ids[index]]
        while index + 1 < len(ids):
            last = run[-1].rpartition("-")[2]
            nxt_head, _, nxt_tail = ids[index + 1].rpartition("-")
            if nxt_head != head or not last.isdigit() or not nxt_tail.isdigit():
                break
            if int(nxt_tail) != int(last) + 1:
                break
            run.append(ids[index + 1])
            index += 1
        if len(run) >= 3:
            out.append(f"{run[0]}..{run[-1].rpartition('-')[2]}")
        else:
            out.extend(run)
        index += 1
    return out


def cmd_commitmsg(vault, args):
    staged = vault.git("diff", "--cached", "--name-only")
    if not staged:
        return fail("nothing staged")
    folders = sorted({p.split("/")[0] for p in staged})
    # A template skeleton carries an example id for the note it scaffolds, not a vault record,
    # so _templates/ contributes folder prefixes but never an id to the message.
    ids = sorted({n.id for rel in staged
                  if (n := vault.by_path.get(rel)) is not None and n.id
                  and not rel.startswith("_templates/")}, key=id_sort_key)
    prefix = f"{' + '.join(folders)}: {args.subject}"
    print(f"{prefix} ({', '.join(collapse_ids(ids))})" if ids else prefix)
    print("PROBLEMS: 0")
    return 0


def cmd_instantiate(vault, args):
    """Name the owner in every content note, rewrite 00-vault/this-vault.json, and drop the
    repository's front page (ADR-0003).

    A template ships with the placeholder owner `owner`. Running this once, when the vault
    starts holding a real idea, replaces the placeholder in every note the human owns, so
    `owner:` stays a fact derived from the path instead of a hand-written guess. Mechanism
    notes, indexes, templates, and tooling keep `owner: vault`. `README.md` and `assets/` exist
    for a code forge's landing page, not for the vault; they are removed here because a vault
    is only self-describing when every file inside it is a note."""
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{1,31}", args.owner):
        return fail(f"owner name must be one word of letters, digits, - or _: {args.owner}")
    if args.owner == vs.CORE_OWNER:
        return fail("the owner's name cannot be `vault`: that value marks a note the vault owns")
    config_path = vault.root / vs.CONFIG_FILE
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return fail(f"{vs.CONFIG_FILE}: {exc}")
    previous = config.get("owner") or vs.HUMAN_OWNER
    changed, problems = 0, 0
    for note in vault.notes:
        if vs.core_note(note.rel):
            continue
        for index in range(1, note.body_start):
            if not note.lines[index].startswith("owner:"):
                continue
            if note.meta.get("owner") == args.owner:
                break
            if note.meta.get("owner") != previous:
                print(f"{note.rel}: owner is {note.meta.get('owner')}, expected {previous}; left alone")
                problems += 1
                break
            text = note.path.read_text(encoding="utf-8")
            note.path.write_text(text.replace(note.lines[index], f"owner: {args.owner}", 1),
                                 encoding="utf-8")
            changed += 1
            break
        else:
            print(f"{note.rel}: no owner field")
            problems += 1
    if args.title:
        config["name"] = args.title
    config["owner"] = args.owner
    if not problems:
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        print(f"{vs.CONFIG_FILE}: owner -> {args.owner}" + (f", name -> {args.title}" if args.title else ""))
        removed = []
        for name in sorted(vs.CLONE_FILES):
            if (vault.root / name).is_file():
                (vault.root / name).unlink()
                removed.append(name)
        for name in sorted(vs.CLONE_DIRS):
            if (vault.root / name).is_dir():
                shutil.rmtree(vault.root / name)
                removed.append(f"{name}/")
        if removed:
            print(f"removed: {', '.join(removed)} (the repository front page and its images are not part of the vault)")
            print("the removal is a change to the repository: stage it and commit it")
    print(f"content notes rewritten: {changed}")
    print(f"PROBLEMS: {problems}")
    return 1 if problems else 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="vault.py",
        description="Vault checks and queries. Every command does the useful thing with no flags.",
        epilog="Word counts exclude markdown delimiters. Exit code 0 = clean, 1 = problems reported.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent),
                        help="vault root (default: the folder above _tools/)")
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    sub.add_parser("check", help="integrity scan of every note").set_defaults(func=cmd_check)
    sub.add_parser("status", help="note, status, and type counts plus id headroom").set_defaults(func=cmd_status)
    sub.add_parser("metrics", help="health numbers as key=value lines for other tools").set_defaults(func=cmd_metrics)

    p = sub.add_parser("changed", help="changed notes with type, status, updated")
    p.add_argument("date", nargs="?", metavar="DATE", help="require this updated: date")
    p.add_argument("--staged", action="store_true", help="staged changes, not the working tree")
    p.set_defaults(func=cmd_changed)

    p = sub.add_parser("words", help="body word counts against the output kind's budget")
    p.add_argument("files", nargs="*", help="notes (default: every issued output instance)")
    p.add_argument("--sections", action="store_true", help="also count per ## section")
    p.set_defaults(func=cmd_words)

    p = sub.add_parser("noise", help="banned content terms for a generated document")
    p.add_argument("files", nargs="*", help="notes (default: every issued output instance)")
    p.add_argument("--term", action="append", metavar="TERM", help="extra term, repeatable")
    p.set_defaults(func=cmd_noise)

    p = sub.add_parser("audit", help="issued outputs: budget, content policy, registration")
    p.add_argument("files", nargs="*", help="notes (default: every issued output instance)")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("ids", help="id ledger, or where one id is defined and mentioned")
    p.add_argument("target", nargs="?", metavar="PREFIX|ID", help="ADR, or ADR-0021; default: every namespace")
    p.set_defaults(func=cmd_ids)

    p = sub.add_parser("next", help="the next free id to allocate")
    p.add_argument("prefix", metavar="PREFIX")
    p.add_argument("folder", nargs="?", help="folder whose block to allocate from")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("find", help="search titles, frontmatter, and bodies")
    p.add_argument("pattern")
    p.add_argument("--regex", action="store_true", help="pattern is a regex")
    p.add_argument("--field", metavar="FIELD", help="search only this frontmatter field")
    p.add_argument("--folder", action="append")
    p.add_argument("--type", action="append")
    p.add_argument("--status", action="append")
    p.add_argument("--tag", action="append")
    p.add_argument("--full", action="store_true", help="show the matching lines")
    p.set_defaults(func=cmd_find)

    p = sub.add_parser("links", help="broken links, orphans, most-linked, or one target's referrers")
    p.add_argument("target", nargs="?", metavar="PATH|ID", help="who links to this path, or mentions this id")
    p.set_defaults(func=cmd_links)

    sub.add_parser("oq", help="open questions with due dates").set_defaults(func=cmd_oq)
    sub.add_parser("adr", help="decision ledger, chains, missing Status lines").set_defaults(func=cmd_adr)

    p = sub.add_parser("due", help="due and review dates at or before a date")
    p.add_argument("date", nargs="?", default=TODAY, metavar="DATE", help="default: today")
    p.add_argument("--stale", type=int, metavar="DAYS", help="also list notes not updated within DAYS")
    p.set_defaults(func=cmd_due)

    p = sub.add_parser("stamp", help="set updated: to today")
    p.add_argument("files", nargs="*", help="notes to stamp")
    p.add_argument("--changed", action="store_true", help="every changed note per git status")
    p.add_argument("--dry-run", action="store_true", help="print what would change")
    p.set_defaults(func=cmd_stamp)

    p = sub.add_parser("scaffold", help="print a note skeleton with the next free id")
    p.add_argument("type")
    p.add_argument("title")
    p.add_argument("folder", nargs="?", help="folder the note will live in")
    p.set_defaults(func=cmd_scaffold)

    p = sub.add_parser("commitmsg", help="commit message built from the staged files")
    p.add_argument("subject")
    p.set_defaults(func=cmd_commitmsg)

    p = sub.add_parser("instantiate", help="name the owner in every content note and in this-vault.json, and remove the repository front page")
    p.add_argument("owner", help="the human owner's name, one word")
    p.add_argument("title", nargs="?", help="the vault's name (default: leave it as it is)")
    p.set_defaults(func=cmd_instantiate)

    return parser


def main(argv=None):
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # piping into head must not raise
    args = build_parser().parse_args(argv)
    vault = Vault(args.root)
    return args.func(vault, args)


if __name__ == "__main__":
    sys.exit(main())
