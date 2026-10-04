// The page: one server card, one card per question, popups for depth.

import { $, ABOUT, CARDS, PANEL_MUTED, STATUS_WORDS, WORDS, clock, escape, icon, numberValue, words } from "./page-state.js";

const page = {
  service: localStorage.getItem("service") || "http://127.0.0.1:8791",
  interval: Number(localStorage.getItem("interval") || 10),
  etag: "",
  reading: null,
  timer: null,
  asking: false,
  asked: false,
  fails: 0,
  txTimer: null,
  txLitUntil: 0,
  drawer: localStorage.getItem("drawer") !== "closed",
};

// How serious each answer is, so a card covering several checks shows the worst one.
const SEVERITY = { error: 3, attention: 2, waiting: 1, ok: 0 };

async function ask() {
  if (page.asking) return;
  page.asking = true;
  $("refresh").disabled = true;
  txFlash();
  const base = page.service.replace(/\/+$/, "");
  try {
    const url = base + "/health" + (page.etag ? "?etag=" + encodeURIComponent(page.etag) : "");
    const response = await fetch(url);
    if (response.status === 304 && page.reading) {
      linkOk();
      render();
      return;
    }
    if (!response.ok) {
      fail("The service answered " + response.status + ".", base);
      return;
    }
    const etag = response.headers.get("ETag");
    if (etag) page.etag = etag;
    page.reading = await response.json();
    linkOk();
    render();
  } catch {
    fail("No answer from the health service.", base);
  } finally {
    page.asking = false;
    $("refresh").disabled = false;
  }
}

function fail(summary, base) {
  page.reading = {
    overall: "error",
    summary,
    detail: "Tried " + base + "/health. Start it with: go run . in _tools/health_service.",
    checks: [],
  };
  page.etag = "";
  linkFail();
  render();
}

// The name shown on the server card: the machine the page is talking to, no port.
function hostOf(service) {
  try {
    const url = new URL(service);
    return url.hostname || service;
  } catch (error) {
    return service;
  }
}

function oldest(checks) {
  let earliest = "";
  for (const check of checks) {
    if (check.ran_at && (!earliest || check.ran_at < earliest)) earliest = check.ran_at;
  }
  return earliest;
}

function ago(iso) {
  if (!iso) return "";
  const seconds = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 1000));
  if (seconds < 60) return seconds + (seconds === 1 ? " second ago" : " seconds ago");
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return minutes + (minutes === 1 ? " minute ago" : " minutes ago");
  const hours = Math.round(minutes / 60);
  if (hours < 24) return hours + (hours === 1 ? " hour ago" : " hours ago");
  return Math.round(hours / 24) + " days ago";
}

function worst(statuses) {
  let outcome = "ok";
  for (const status of statuses) {
    if ((SEVERITY[status] || 0) > (SEVERITY[outcome] || 0)) outcome = status;
  }
  return outcome;
}

function render() {
  const reading = page.reading || { overall: "waiting", summary: "No reading yet. Press \"Check now\".", checks: [] };
  const checks = reading.checks || [];

  // The left edge stripe carries the overall colour; the box at the right end says it in words.
  $("server").className = serverClasses(reading.overall);
  $("server-host").textContent = hostOf(page.service);
  $("server-state").textContent = WORDS[reading.overall] || reading.overall;
  // Nothing is added to the card when the service does not answer, so the reason is kept
  // for the tooltip on the state box instead of a line of its own.
  $("server-state").title = (reading.summary || "") + (reading.detail ? " " + reading.detail : "");

  const cards = cardsFor(checks);
  const mini = $("mini");
  mini.textContent = "";
  for (const card of cards) mini.appendChild(chip(card));
  const held = $("cards");
  held.textContent = "";
  for (const card of cards) held.appendChild(cardButton(card));
}

// One small icon per card, coloured by that card's answer, opening the same popup.
function chip(card) {
  const status = cardStatus(card.answers);
  const button = document.createElement("button");
  button.type = "button";
  button.className = "chip " + status;
  button.title = card.label + " — " + (STATUS_WORDS[status] || status);
  button.innerHTML = icon(card.icon);
  button.addEventListener("click", () => openCard(card));
  return button;
}

// The two lights beside the server's name work like a modem's. Rx is the service's
// side of the link: green while the last request was answered, yellow after one failure,
// red from the fourth. Tx is this page's side: amber while the link is up, and green
// only for the moment a request is on its way out.
function linkOk() {
  page.asked = true;
  page.fails = 0;
  paintLink();
}

function linkFail() {
  page.asked = true;
  page.fails += 1;
  paintLink();
}

function paintLink() {
  const rx = $("rx");
  rx.className = "light rx";
  if (page.asked) rx.classList.add(page.fails === 0 ? "green" : page.fails < 4 ? "warn" : "down");
  paintTx();
}

// Tx keeps its own clock. A send lights it for a moment, and an answer that comes back
// sooner than that moment does not put the light out early.
function paintTx() {
  const tx = $("tx");
  tx.className = "light tx";
  if (Date.now() < page.txLitUntil) {
    tx.classList.add("green");
    return;
  }
  tx.classList.add(page.asked && page.fails < 4 ? "ready" : "off");
}

function txFlash() {
  clearTimeout(page.txTimer);
  page.txLitUntil = Date.now() + 900;
  paintTx();
  page.txTimer = setTimeout(paintTx, 900);
}

// A new address is a new link, so the lights start over.
function resetLink() {
  page.asked = false;
  page.fails = 0;
  page.txLitUntil = 0;
  paintLink();
}

// A check the operator adds may only have its own name for a label; said out loud,
// underscores become spaces.
function readable(check) {
  const label = check.label || check.name;
  return label === check.name ? check.name.replace(/_/g, " ") : label;
}

// Cards come from the CARDS list, so a question can be answered by several checks.
// Any check the operator added that no card claims gets a card of its own.
function cardsFor(checks) {
  const held = new Map(checks.map((check) => [check.name, check]));
  const cards = [];
  const claimed = new Set();
  for (const card of CARDS) {
    const mine = card.checks.map((name) => held.get(name)).filter(Boolean);
    // With nothing answered the shape is kept: every question still gets its panel and its
    // icon, greyed out, so the card is the same size whether or not the service is up.
    if (!mine.length && checks.length) continue;
    for (const name of card.checks) claimed.add(name);
    cards.push({ ...card, answers: mine });
  }
  for (const check of checks) {
    if (claimed.has(check.name)) continue;
    cards.push({
      key: check.name,
      label: readable(check),
      icon: "search",
      numbers: [],
      answers: [check],
    });
  }
  return cards;
}

function cardStatus(answers) {
  // No answer is not a clear answer: the panel and its icon go grey.
  if (!answers.length) return "waiting";
  return worst(answers.map((check) => check.status));
}

function cardSummary(answers) {
  if (!answers.length) return "";
  if (answers.length === 1) return answers[0].summary || "";
  const odd = answers.filter((check) => check.status !== "ok");
  if (!odd.length) {
    const shared = [...new Set(answers.map((check) => check.summary).filter(Boolean))];
    return shared.join(" · ") || "nothing to fix";
  }
  return odd.map((check) => readable(check) + ": " + (STATUS_WORDS[check.status] || check.status)).join(", ");
}

// A card leads with the numbers that answer its question. When the card names none,
// the checks' own numbers fill in; a card that names an empty list shows none.
function cardNumbers(card, answers) {
  const own = {};
  for (const check of answers) Object.assign(own, check.numbers || {});
  const merged = { ...(page.reading && page.reading.numbers), ...own };
  const wanted = card.numbers.length ? card.numbers : Object.keys(own).slice(0, 3);
  const picked = {};
  for (const key of wanted) {
    if (key in merged) picked[key] = merged[key];
  }
  return picked;
}

function cardButton(card) {
  const status = cardStatus(card.answers);
  const button = document.createElement("button");
  button.type = "button";
  button.className = "card " + status;
  button.dataset.card = card.key;
  button.title = card.label + " — " + (cardSummary(card.answers) || STATUS_WORDS[status] || status);
  button.addEventListener("click", () => openCard(card));

  const mark = document.createElement("span");
  mark.className = "card-icon";
  mark.innerHTML = icon(card.icon);

  const label = document.createElement("span");
  label.className = "card-label";
  label.textContent = card.label;

  const state = document.createElement("span");
  state.className = "card-status";
  state.textContent = STATUS_WORDS[status] || status;

  // A panel has no room for the sentence a card used to carry, so it lives in the tooltip
  // and in the popup; the status column and the numbers answer it here.
  const numbers = cardNumbers(card, card.answers);
  const row = document.createElement("span");
  row.className = "card-numbers";
  for (const key of Object.keys(numbers)) {
    if (PANEL_MUTED.includes(key)) continue;
    const pair = document.createElement("span");
    const value = document.createElement("b");
    value.textContent = numberValue(numbers[key]);
    pair.append(value, " " + words(key, numbers[key]));
    row.appendChild(pair);
  }

  const when = document.createElement("span");
  when.className = "card-when";
  const at = oldest(card.answers.map((check) => ({ ran_at: check.ran_at })));
  const every = card.answers.map((check) => check.interval_seconds).filter(Boolean);
  when.textContent = at
    ? "checked " + ago(at) + (every.length ? " · every " + Math.max(...every) + " s" : "")
    : "not checked yet";

  button.append(mark, label, state, row, when);
  return button;
}

function openModal(html) {
  $("modal-body").innerHTML = html;
  $("modal").hidden = false;
  $("modal-close").focus();
}

function closeModal() {
  $("modal").hidden = true;
  $("modal-body").textContent = "";
}

function pill(status) {
  return '<span class="pill ' + status + '">' + (STATUS_WORDS[status] || status) + "</span>";
}

async function fullReport(name) {
  try {
    const response = await fetch(page.service.replace(/\/+$/, "") + "/report?check=" + encodeURIComponent(name));
    if (response.ok) return await response.json();
  } catch (error) {
    // The held reading is enough to show.
  }
  return null;
}

function logRows(history, at) {
  if (!history || !history.length) return "<p>Only one reading so far.</p>";
  const rows = history.map((round) =>
    "<li><time>" + clock(at(round)) + "</time>" +
    '<span class="mark ' + (round.status || round.overall) + '">' +
    (STATUS_WORDS[round.status] || WORDS[round.overall] || round.status || round.overall) + "</span>" +
    '<span class="text">' + escape(round.summary || "") + "</span></li>");
  return '<ul class="log">' + rows.join("") + "</ul>";
}

function numbersTable(numbers, note) {
  const keys = Object.keys(numbers || {});
  if (!keys.length) return "";
  const rows = keys.sort().map((key) =>
    "<dt>" + escape(words(key, numbers[key])) + "</dt><dd>" + escape(numberValue(numbers[key])) + "</dd>");
  const source = note ? '<p class="note">' + escape(note) + "</p>" : "";
  return "<h3>Numbers</h3>" + source + "<dl>" + rows.join("") + "</dl>";
}

// Each answer is shown under its own name when a card holds more than one check.
function titled(card, check, body) {
  if (card.answers.length === 1) return body;
  return "<h4>" + escape(check.label || check.name) + "</h4>" + body;
}

// A question with no answer still has a popup: the name, the fact that nothing was
// answered, and the reason the service gave.
function noAnswerCard(card) {
  const reading = page.reading;
  const reason = reading ? reading.summary + (reading.detail ? " " + reading.detail : "") : "No reading yet.";
  return `
    <h2>${icon(card.icon)}<span>${escape(card.label)}</span></h2>
    <p>${pill("waiting")}</p>
    <h3>What it found</h3>
    <p class="lede">${escape(reason)}</p>
    <p class="note">Nothing has been answered, so there is nothing to look at yet.</p>
  `;
}

async function openCard(card) {
  if (!card.answers.length) {
    openModal(noAnswerCard(card));
    return;
  }
  const fulls = await Promise.all(card.answers.map((check) => fullReport(check.name)));
  const answers = card.answers.map((check, index) => fulls[index] || check);
  const status = cardStatus(answers);
  const many = answers.length > 1;

  const looks = answers.map((check) =>
    titled(card, check, '<p class="lede">' + escape(check.description ||
      "This check asks the vault tooling one question and reports what it finds.") + "</p>")).join("");
  const found = answers.map((check) =>
    titled(card, check,
      "<p class=\"lede\">" + escape(check.summary || "") + "</p>" +
      (check.problems ? "<p><b>" + check.problems + "</b> item" + (check.problems === 1 ? "" : "s") + " named.</p>" : "<p>Nothing to fix.</p>") +
      (check.detail ? "<pre class=\"report\">" + escape(check.detail) + "</pre>" : ""))).join("");
  const places = answers.map((check) => {
    const lines = (check.lines || []).map(escape).join("\n");
    return titled(card, check,
      (lines ? "<pre class=\"report\">" + lines + "</pre>" : "<p>The check reported no lines.</p>") +
      (check.more_lines ? "<p>" + check.more_lines + " further lines were left out of the message.</p>" : ""));
  }).join("");
  const runs = answers.map((check) =>
    titled(card, check, logRows(check.history, (round) => round.ran_at))).join("");
  const details = answers.map((check) =>
    titled(card, check,
      "<dl><dt>Last checked</dt><dd>" + (check.ran_at ? ago(check.ran_at) + " (" + clock(check.ran_at) + ")" : "not yet") + "</dd>" +
      "<dt>It took</dt><dd>" + check.took_ms + " ms</dd>" +
      "<dt>Question asked</dt><dd><code>vault.py " + escape(check.command) + "</code></dd></dl>")).join("");

  openModal(`
    <h2>${icon(card.icon)}<span>${escape(card.label)}</span></h2>
    <p>${pill(status)}</p>
    <h3>What this looks at</h3>
    ${looks}
    <h3>What it found</h3>
    ${found}
    ${numbersTable(cardNumbers(card, answers), many ? "" : "These come from the vault's own measurements.")}
    <h3>Exact places to look</h3>
    ${places}
    <h3>Recent runs</h3>
    ${runs}
    <h3>Details</h3>
    ${details}
  `);
}

function schedule() {
  clearInterval(page.timer);
  page.timer = null;
  if (page.interval > 0) page.timer = setInterval(ask, page.interval * 1000);
}

function showTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("theme", theme);
  $("theme").textContent = theme === "dark" ? "Light" : "Dark";
  $("theme").setAttribute("aria-pressed", String(theme === "light"));
}

// The answers hang underneath the row: one box, one stripe, opened from the row itself.
function serverClasses(overall) {
  return "server " + overall + (page.drawer ? " open" : " closed");
}

function showDrawer(open) {
  page.drawer = open;
  localStorage.setItem("drawer", open ? "open" : "closed");
  $("server").className = serverClasses(page.reading ? page.reading.overall : "waiting");
  $("drawer-toggle").setAttribute("aria-expanded", String(open));
}

function start() {
  $("service").value = page.service;
  $("interval").value = String(page.interval);
  $("server-icon").innerHTML = icon("server");
  showDrawer(page.drawer);
  showTheme(document.documentElement.dataset.theme);
  $("drawer-toggle").addEventListener("click", () => showDrawer(!page.drawer));
  $("theme").addEventListener("click", () => {
    showTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
  });
  $("service").addEventListener("change", (event) => {
    page.service = event.target.value.trim() || "http://127.0.0.1:8791";
    event.target.value = page.service;
    localStorage.setItem("service", page.service);
    page.etag = "";
    page.reading = null;
    resetLink();
    ask();
  });
  $("interval").addEventListener("change", (event) => {
    page.interval = Number(event.target.value);
    localStorage.setItem("interval", String(page.interval));
    schedule();
  });
  $("refresh").addEventListener("click", ask);
  $("about").addEventListener("click", () => openModal(ABOUT));
  $("modal-close").addEventListener("click", closeModal);
  $("modal").addEventListener("click", (event) => {
    if (event.target.id === "modal") closeModal();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !$("modal").hidden) closeModal();
  });
  schedule();
  ask();
}

start();
