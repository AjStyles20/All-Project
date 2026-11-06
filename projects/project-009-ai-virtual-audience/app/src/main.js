// Browser layer: set-up, the room (talk, interruptions, questions), the report and local history.
import { SCENARIOS, SKILLS, answer, createSession, finishTalk, nextDrill, normalise, report, talk } from "./engine.js";

const HISTORY_KEY = "rehearsal.history.v1";
const $ = (id) => document.getElementById(id);
const el = (tag, text, cls) => { const n = document.createElement(tag); if (text != null) n.textContent = text; if (cls) n.className = cls; return n; };
const SVG = "http://www.w3.org/2000/svg";

let s = null;
let talkStart = 0;
let askedAt = 0;
let firstInputAt = null;
let timer = null;
let recognition = null;

function storage(fn, fallback = null) { try { return fn(window.localStorage); } catch { return fallback; } }
const history = () => storage((ls) => JSON.parse(ls.getItem(HISTORY_KEY) || "[]"), []);
function notice(text) { $("notice").replaceChildren(text ? el("p", text, "error") : ""); }

// ---------- audience drawing ----------

const MOUTH = { listening: "M-8 8 Q0 10 8 8", nodding: "M-9 6 Q0 14 9 6", asking: "M-5 7 Q0 12 5 7 Q0 4 -5 7",
                interrupting: "M-6 6 Q0 13 6 6 Q0 4 -6 6", puzzled: "M-8 9 Q-2 6 8 8", unconvinced: "M-8 9 L8 7",
                "checking the time": "M-8 9 L8 9" };

function face(p, mood) {
  const svg = document.createElementNS(SVG, "svg");
  svg.setAttribute("viewBox", "-30 -30 60 60");
  svg.setAttribute("aria-hidden", "true");
  const add = (tag, attrs) => { const n = document.createElementNS(SVG, tag); for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); svg.append(n); return n; };
  add("circle", { r: 26, class: `head d-${p.demeanour}` });
  const brow = mood === "unconvinced" || mood === "puzzled" ? -2 : 0;
  add("line", { x1: -14, y1: -10 + brow, x2: -5, y2: -11, class: "feature" });
  add("line", { x1: 5, y1: -11, x2: 14, y2: -10 - brow, class: "feature" });
  add("circle", { cx: -9, cy: -3, r: 2.5, class: "eye" });
  add("circle", { cx: 9, cy: mood === "checking the time" ? 0 : -3, r: 2.5, class: "eye" });
  add("path", { d: MOUTH[mood] || MOUTH.listening, class: "feature", fill: "none" });
  return svg;
}

function drawAudience() {
  $("audience").replaceChildren(...s.personas.map((p) => {
    const fig = el("figure", null, `seat ${s.current?.persona === p.id ? "speaking" : ""}`);
    const mood = s.moods[p.id];
    fig.append(face(p, mood), el("figcaption", `${p.name}, ${p.role}`), el("span", mood, "mood"));
    return fig;
  }));
}

// ---------- flow ----------

function speak(text) {
  if (!$("speak-questions").checked || !("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  speechSynthesis.speak(new SpeechSynthesisUtterance(text));
}

function showQuestion() {
  const q = s.current;
  const who = s.personas.find((p) => p.id === q.persona);
  const label = q.kind === "interruption" ? "interrupts" : q.kind === "follow-up" ? "follows up" : "asks";
  $("bubble").hidden = false;
  $("bubble").textContent = `${who.name} ${label}: “${q.text}”`;
  $("phase").textContent = "Answer the question.";
  $("input-label").textContent = "Your answer";
  $("send").textContent = "Answer";
  $("finish").hidden = true;
  $("input").value = "";
  askedAt = performance.now();
  firstInputAt = null;
  speak(q.text);
  drawAudience();
  $("input").focus();
}

function showTalk() {
  $("bubble").hidden = true;
  $("phase").textContent = s.interrupted ? "Carry on with your talk." : "Give your talk.";
  $("input-label").textContent = "Your talk";
  $("send").textContent = "Add to talk";
  $("finish").hidden = false;
  $("input").value = "";
  drawAudience();
}

function tick() {
  if (!s) return;
  const elapsed = (performance.now() - talkStart) / 1000;
  if (s.phase === "talk") {
    const left = Math.max(0, s.talkSeconds - elapsed);
    $("clock").textContent = `Talk time left: ${Math.ceil(left)} s`;
    const before = s.phase;
    talk(s, "", elapsed);
    if (before === "talk" && s.phase === "answer") showQuestion();
    else if (left <= 0) { finishTalk(s); afterStep(); }
  } else if (s.phase === "answer") {
    const used = (performance.now() - askedAt) / 1000;
    $("clock").textContent = `Answer time: ${Math.floor(used)} of ${s.answerSeconds} s`;
  }
}

function afterStep() {
  if (s.phase === "answer") showQuestion();
  else if (s.phase === "talk") showTalk();
  else finish();
}

function start(ev) {
  ev.preventDefault();
  const stressors = [...document.querySelectorAll("input[name=stressor]:checked")].map((b) => b.value);
  s = createSession($("scenario").value, { seed: Math.floor(Math.random() * 1e9), stressors });
  $("setup").hidden = true; $("result").hidden = true; $("room").hidden = false;
  talkStart = performance.now();
  showTalk();
  timer = setInterval(tick, 250);
  $("mic").hidden = !$("use-mic").checked || !recognitionAvailable();
  $("input").focus();
}

function submit(ev) {
  ev.preventDefault();
  const text = $("input").value.trim();
  if (s.phase === "talk") {
    if (!text) return;
    talk(s, text, (performance.now() - talkStart) / 1000);
    if (s.phase === "answer") showQuestion(); else { $("input").value = ""; drawAudience(); }
    return;
  }
  if (!text) { notice("Type or say an answer first (even 'I don't know' is a valid practice answer)."); return; }
  notice("");
  const now = performance.now();
  answer(s, text, { startedAfter: ((firstInputAt ?? now) - askedAt) / 1000, took: (now - askedAt) / 1000 });
  afterStep();
}

function finish() {
  clearInterval(timer);
  stopMic();
  const r = report(s);
  r.when = new Date().toISOString();
  const all = history().concat([{ when: r.when, scenario: r.scenario, stressors: r.stressors, skills: r.skills }]).slice(-50);
  storage((ls) => ls.setItem(HISTORY_KEY, JSON.stringify(all)));
  $("room").hidden = true; $("result").hidden = false;
  renderReport(r, all);
  s = null;
}

function renderReport(r, all) {
  const parts = [];
  const table = el("table");
  table.append(el("caption", "Every answer"));
  const head = el("tr");
  ["Who / what", "Started after", "Took", "Words", "Fillers per 100 words", "On the question", "Evidence", "Limits"].forEach((h) => head.append(el("th", h)));
  table.append(head);
  for (const t of r.turns) {
    const tr = el("tr");
    const m = t.metrics;
    const who = SCENARIOS.find((x) => x.id === r.scenario).personas.find((p) => p.id === t.persona).name;
    [`${who} (${t.kind}): ${t.text}`, `${m.startedAfter} s`, `${m.took} s${m.overTime ? " (over)" : ""}`, m.words, m.fillerRate,
     `${Math.round(m.relevance * 100)} %`, m.usesEvidence ? "yes" : "no", m.acknowledgesLimit ? "yes" : "no"]
      .forEach((v) => tr.append(el("td", String(v))));
    table.append(tr);
  }
  parts.push(table);
  if (r.recovery) parts.push(el("p", `Interruption (“${r.recovery.interruption}”): ${r.recovery.answeredBriefly ? "answered briefly" : "long answer"}, and you ${r.recovery.resumed ? "picked your thread back up" : "did not clearly return to your point"}.`));
  const n = normalise(r.skills);
  const list = el("ul", null, "skills");
  for (const [k, v] of Object.entries(n)) {
    const li = el("li");
    const bar = el("meter"); bar.min = 0; bar.max = 1; bar.value = v; bar.setAttribute("aria-label", SKILLS[k]);
    li.append(el("span", `${SKILLS[k]}: ${v >= 0.6 ? "fine" : "worth practising"} `), bar);
    list.append(li);
  }
  parts.push(el("h3", "This run"), list);
  r.notes.forEach((t) => parts.push(el("p", t, "suggest")));
  const next = nextDrill(all);
  if (next.skill) parts.push(el("p", `Next suggested drill: ${next.drill.name}, for ${next.label.toLowerCase()} (based on your last ${Math.min(5, all.length)} runs). Tip: ${next.drill.tip}`, "suggest"));
  parts.push(el("p", "These are simple measures of the text of your answers, made by this page. They are a practice guide, not a grade or an assessment of you.", "meta"));
  $("report").replaceChildren(...parts);
}

// ---------- history and set-up ----------

function renderHistory() {
  const all = history();
  if (!all.length) { $("history").replaceChildren(el("p", "No runs yet.", "meta")); $("suggestion").textContent = ""; return; }
  const ul = el("ul");
  all.slice(-8).reverse().forEach((h) => ul.append(el("li", `${new Date(h.when).toLocaleString()} — ${SCENARIOS.find((x) => x.id === h.scenario)?.name}${h.stressors.length ? ` (${h.stressors.join(", ")})` : ""}`)));
  $("history").replaceChildren(ul);
  const next = nextDrill(all);
  if (next.skill) {
    $("suggestion").textContent = `Suggested from your recent runs: ${next.drill.name} (${next.label.toLowerCase()}).`;
    document.querySelectorAll("input[name=stressor]").forEach((b) => { b.checked = next.drill.stressors.includes(b.value); });
  }
}

function recognitionAvailable() { return "webkitSpeechRecognition" in window || "SpeechRecognition" in window; }

function stopMic() { if (recognition) { recognition.onend = null; recognition.stop(); recognition = null; $("mic").textContent = "Start speaking"; } }

$("mic").addEventListener("click", () => {
  if (recognition) { stopMic(); return; }
  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new Rec();
  recognition.continuous = true;
  recognition.interimResults = false;
  recognition.onresult = (e) => {
    if (firstInputAt == null) firstInputAt = performance.now();
    for (let i = e.resultIndex; i < e.results.length; i++) if (e.results[i].isFinal) $("input").value += `${e.results[i][0].transcript} `;
  };
  recognition.onerror = (e) => { notice(`Speech recognition stopped: ${e.error}. You can type instead.`); stopMic(); };
  recognition.onend = () => stopMic();
  recognition.start();
  $("mic").textContent = "Stop speaking";
});

$("input").addEventListener("input", () => { if (firstInputAt == null && s?.phase === "answer") firstInputAt = performance.now(); });
$("setup-form").addEventListener("submit", start);
$("input-form").addEventListener("submit", submit);
$("finish").addEventListener("click", () => {
  const text = $("input").value.trim();
  if (text) talk(s, text, (performance.now() - talkStart) / 1000);
  if (s.phase === "talk") finishTalk(s);
  afterStep();
});
$("again").addEventListener("click", () => { $("result").hidden = true; $("setup").hidden = false; renderHistory(); });
$("clear-history").addEventListener("click", () => {
  if (confirm("Delete your practice history from this browser?")) { storage((ls) => ls.removeItem(HISTORY_KEY)); renderHistory(); }
});
$("scenario").replaceChildren(...SCENARIOS.map((sc) => { const o = el("option", sc.name); o.value = sc.id; return o; }));
const describe = () => {
  const sc = SCENARIOS.find((x) => x.id === $("scenario").value);
  $("scenario-info").textContent = `${Math.round(sc.talkSeconds)} s talk, ${sc.answerSeconds} s per answer. Panel: ${sc.personas.map((p) => `${p.name} (${p.role})`).join(", ")}.`;
};
$("scenario").addEventListener("change", describe);
describe();
if (!recognitionAvailable()) { $("use-mic").disabled = true; $("mic-note").textContent = "Speech-to-text is not available in this browser; typing works everywhere."; }
renderHistory();
