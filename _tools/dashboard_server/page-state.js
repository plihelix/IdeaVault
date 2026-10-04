// Words, card shapes and icons the page shows. Kept apart from the polling logic so
// the plain-English vocabulary and the card layout are one readable list.

export const WORDS = {
  ok: "All clear",
  attention: "Needs attention",
  error: "Checking failed",
  waiting: "Waiting",
};

export const STATUS_WORDS = {
  ok: "clear",
  attention: "needs looking at",
  error: "could not finish",
  waiting: "not run yet",
};

// Number names the vault tooling uses, said in ordinary words.
export const NUMBER_WORDS = {
  notes: "notes",
  content_notes: "notes with content",
  templates: "templates",
  defined_ids: "artifact identities",
  undefined_ids: "undefined artifacts",
  open_questions: "open questions",
  decisions: "decision records",
  output_instances: "issued outputs",
  output_instances_over_budget: "outputs over budget",
  numbering_exhausted: "numbering full",
  scan_problems: "rule problems",
  broken_links: "broken links",
  unlinked_notes: "notes with no links",
  changed_notes: "notes changed",
  due_at_or_before_today: "dates arrived",
  review_at_or_before_today: "reviews due",
  status_accepted: "finished",
  status_proposed: "proposed",
  status_draft: "draft",
  status_archived: "archived",
};

// Numbers worth a table in the popup that would only clutter a panel's single line.
export const PANEL_MUTED = ["numbering_exhausted"];

// Icons for the card titles. Drawn here so the page needs no image files and no
// network: 24x24, stroke follows the card's colour.
export const ICONS = {
  shield: '<path d="M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-4.5"/>',
  stack: '<path d="M12 3 3 7.5 12 12l9-4.5z"/><path d="m3 12 9 4.5L21 12"/><path d="m3 16.5 9 4.5 9-4.5"/>',
  link: '<path d="m10 14 4-4"/><path d="m11 7 1.6-1.6a4 4 0 0 1 5.7 5.7L16.5 13"/><path d="M7.5 11 6 12.6a4 4 0 0 0 5.7 5.7L13 17"/>',
  question: '<circle cx="12" cy="12" r="9"/><path d="M9.8 9.4a2.4 2.4 0 1 1 3.4 2.2c-.8.4-1.2 1-1.2 1.9v.4"/><path d="M12 17.4h.01"/>',
  record: '<path d="m12 3 2.2 1.6 2.7-.3 1 2.5 2.3 1.4-.8 2.6.8 2.6-2.3 1.4-1 2.5-2.7-.3L12 21l-2.2-1.6-2.7.3-1-2.5-2.3-1.4.8-2.6-.8-2.6 2.3-1.4 1-2.5 2.7.3z"/><path d="m9 12 2 2 4-4"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
  pencil: '<path d="M4 20h4l10-10-4-4L4 16z"/><path d="m14 6 4 4"/>',
  draft: '<path d="M7 3h7l4 4v14H7z"/><path d="m14 3 4 4h-4z"/><path d="M9.5 12h5M9.5 16h4"/>',
  speech: '<path d="M20 6.5v8a2 2 0 0 1-2 2h-6l-4 3v-3H6a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2z"/><path d="m8.5 9 7 5"/>',
  search: '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/>',
  server: '<path d="M4 5h16v5H4z"/><path d="M4 14h16v5H4z"/><path d="M7.5 7.5h.01M7.5 16.5h.01"/>',
};

// The cards the dashboard shows. A card is one glanceable answer, and it may be
// answered by more than one check: "Vault stats" is answered by the size measurements
// and the numbering check together. A check the operator adds that is not named here
// still gets its own card.
export const CARDS = [
  {
    key: "integrity",
    label: "Note rules",
    icon: "shield",
    checks: ["integrity"],
    numbers: ["scan_problems"],
  },
  {
    key: "vault_stats",
    label: "Vault stats",
    icon: "stack",
    checks: ["size", "numbering"],
    numbers: ["notes", "status_accepted", "status_draft", "defined_ids", "undefined_ids", "numbering_exhausted"],
  },
  {
    key: "links",
    label: "Links between notes",
    icon: "link",
    checks: ["links"],
    numbers: ["broken_links", "unlinked_notes"],
  },
  {
    key: "open_questions",
    label: "Open questions",
    icon: "question",
    checks: ["open_questions"],
    numbers: ["open_questions"],
  },
  {
    key: "decisions",
    label: "Decision records",
    icon: "record",
    checks: ["decisions"],
    numbers: ["decisions"],
  },
  {
    key: "due_dates",
    label: "Overdue and expired",
    icon: "clock",
    checks: ["due_dates"],
    numbers: ["due_at_or_before_today", "review_at_or_before_today"],
  },
  {
    key: "recent_edits",
    label: "Edits since commit",
    icon: "pencil",
    checks: ["recent_edits"],
    numbers: ["changed_notes"],
  },
  {
    key: "output_drafts",
    label: "Generated outputs",
    icon: "draft",
    checks: ["output_drafts"],
    numbers: ["output_instances", "output_instances_over_budget"],
  },
  {
    key: "language",
    label: "Prohibited words",
    icon: "speech",
    checks: ["language"],
    numbers: [],
  },
];

export const ABOUT = `
  <h2>What is this vault?</h2>
  <p class="lede">A vault is the project's own working record, not a notebook: one note for each
  claim, design choice, decision, question and measurement, kept in ordinary text files.
  Every note is addressable, dated, owned by someone, and traceable to the evidence behind it,
  so a claim can be checked instead of remembered.</p>
  <h3>How the notes are arranged</h3>
  <p>Notes live in folders by what they are about — the idea itself, its claims, its parts, its
  risks, its measurements, its evidence, and the questions and decisions the owner is working
  through. Each note carries a small header saying what kind of note it is, who it belongs to,
  when it was last changed and how settled it is.</p>
  <h3>Every note has its own identity</h3>
  <p>A requirement is <code>REQ-012</code>, a decision is <code>ADR-0007</code>, an
  open question is <code>OQ-003</code>. Notes quote each other by these identities, so a
  claim can always be traced back to the note that made it.</p>
  <h3>How settled a note is</h3>
  <p>A note starts as a <em>draft</em>, becomes <em>proposed</em> once it is written up,
  and reaches <em>accepted</em> when the project has agreed to it. <em>Archived</em> means
  it is kept for the record but no longer in force.</p>
  <h3>What this page does</h3>
  <p>A small service reads the vault on a fixed schedule and keeps the answer ready.
  This page asks that service as often as you choose and shows the answer. It never reads
  the vault itself, so looking at the page cannot disturb the work.</p>
`;

export const $ = (id) => document.getElementById(id);

export function icon(name) {
  const body = ICONS[name] || ICONS.search;
  return '<svg class="icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" ' +
    'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + body + "</svg>";
}

// The label for a number, said in the singular when the count is one.
export function words(key, value) {
  const label = NUMBER_WORDS[key] || key.replace(/_/g, " ");
  if (String(value) !== "1") return label;
  const [first, ...rest] = label.split(" ");
  if (first.length < 2 || !first.endsWith("s")) return label;
  return [first.slice(0, -1), ...rest].join(" ");
}

export function numberValue(value) {
  if (value === "" || value === "none") return "none";
  return value.split(",").map((part) => part.trim()).join(", ");
}

export function clock(iso) {
  if (!iso) return "";
  return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export function escape(text) {
  const holder = document.createElement("div");
  holder.textContent = text === null || text === undefined ? "" : String(text);
  return holder.innerHTML;
}

// The saved theme is applied as soon as the page loads, so the colours do not flash.
const savedTheme = localStorage.getItem("theme") ||
  (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
document.documentElement.dataset.theme = savedTheme;
