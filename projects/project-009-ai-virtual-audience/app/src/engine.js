// Rehearsal engine: pure and deterministic (seeded), no DOM, testable in Node.
// It schedules talk time, interruptions, questions and follow-ups, measures what can be observed
// in the text of each answer, and suggests the next drill. All scores describe practice
// performance in this tool; none is a judgement of the person or a clinical measure.
import { DEMEANOURS, DRILLS, FILLERS, SCENARIOS, SKILLS } from "./data.js";

export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const STOP = new Set(("a an the and or but of to in on for with is are was were be been it this that you your i we our they " +
  "what why how when where who which do did does have has had can could would should will just so as at by from about into " +
  "me my us them their there here not no yes if then than too very").split(" "));

export function words(text) {
  return (text.toLowerCase().match(/[a-z0-9']+/g) || []);
}

// Crude suffix stripping so "tested", "tests" and "testing" match "test" (found in browser testing:
// exact matching scored an on-topic answer 0 %). Good enough for overlap, not real linguistics.
export function stem(w) {
  for (const suf of ["ing", "ed", "es", "s", "ly"]) {
    if (w.endsWith(suf) && w.length - suf.length >= 3) return w.slice(0, -suf.length);
  }
  return w;
}

export function contentWords(text) {
  return new Set(words(text).filter((w) => w.length > 2 && !STOP.has(w)).map(stem));
}

export function countFillers(text) {
  const t = ` ${words(text).join(" ")} `;
  let n = 0;
  for (const f of FILLERS) {
    const re = new RegExp(` ${f} `, "g");
    n += (t.match(re) || []).length;
  }
  return n;
}

// ---------- session ----------

export function createSession(scenarioId, { seed = 1, stressors = [], questionsPerPerson = 1 } = {}) {
  const scenario = SCENARIOS.find((s) => s.id === scenarioId);
  if (!scenario) throw new Error(`Unknown scenario ${scenarioId}`);
  const random = rng(seed);
  const personas = scenario.personas.map((p) => ({
    ...p, demeanour: stressors.includes("skeptical") && p.demeanour === "supportive" ? "skeptical" : p.demeanour,
  }));
  const queue = [];
  for (let round = 0; round < questionsPerPerson; round++) {
    for (const p of personas) {
      const pool = scenario.questions[p.id];
      queue.push({ persona: p.id, text: pool[(round + Math.floor(random() * pool.length)) % pool.length], kind: "question" });
    }
  }
  if (stressors.includes("unexpected")) {
    const p = personas[Math.floor(random() * personas.length)];
    queue.splice(1, 0, { persona: p.id, text: "Here's one you may not expect: what would you do differently if you started again tomorrow?", kind: "question" });
  }
  const interruptChance = Math.max(...personas.map((p) => DEMEANOURS[p.demeanour].interruptChance));
  const interruptAt = stressors.includes("interrupt") || random() < interruptChance
    ? Math.round(scenario.talkSeconds * (0.3 + random() * 0.4)) : null;
  const answerSeconds = stressors.includes("strict-time") ? Math.round(scenario.answerSeconds * 0.5) : scenario.answerSeconds;
  return {
    scenario: scenario.id, seed, stressors, personas, phase: "talk", talkSeconds: scenario.talkSeconds, answerSeconds,
    interruptAt, interrupted: false, talkText: "", talkBeforeInterruption: "", queue, current: null,
    turns: [], random, moods: Object.fromEntries(personas.map((p) => [p.id, "listening"])), rapid: stressors.includes("rapid"),
  };
}

function persona(s, id) {
  return s.personas.find((p) => p.id === id);
}

function scenarioOf(s) {
  return SCENARIOS.find((x) => x.id === s.scenario);
}

// The presenter adds talk text; the engine may interrupt at the scheduled second.
export function talk(s, text, elapsedSeconds) {
  if (s.phase !== "talk") return s;
  s.talkText = `${s.talkText} ${text}`.trim();
  if (s.interruptAt != null && !s.interrupted && elapsedSeconds >= s.interruptAt) {
    s.interrupted = true;
    s.talkBeforeInterruption = s.talkText;
    const by = s.personas.reduce((a, b) => (DEMEANOURS[b.demeanour].interruptChance > DEMEANOURS[a.demeanour].interruptChance ? b : a));
    const lines = scenarioOf(s).interruptions;
    s.current = { persona: by.id, text: lines[Math.floor(s.random() * lines.length)], kind: "interruption", askedAt: elapsedSeconds };
    s.moods[by.id] = "interrupting";
    s.phase = "answer";
  }
  return s;
}

export function finishTalk(s) {
  if (s.phase === "talk") nextQuestion(s, 0);
  return s;
}

function nextQuestion(s, at) {
  const q = s.queue.shift();
  if (!q) {
    s.phase = "done";
    s.current = null;
    return;
  }
  s.current = { ...q, askedAt: at };
  for (const p of s.personas) s.moods[p.id] = p.id === q.persona ? "asking" : "listening";
  s.phase = "answer";
}

// One answer: text, seconds until the first word, and total seconds taken.
export function answer(s, text, { startedAfter, took }) {
  if (s.phase !== "answer") throw new Error("No question is waiting for an answer.");
  const q = s.current;
  const asker = persona(s, q.persona);
  const metrics = measure(text, q.text, asker, { startedAfter, took, limit: s.answerSeconds });
  const turn = { ...q, answer: text, metrics };
  s.turns.push(turn);
  s.moods[asker.id] = reaction(metrics, asker.demeanour);

  if (q.kind === "interruption") {
    s.phase = "talk";          // back to the talk; recovery is measured when the talk finishes
    s.current = null;
    return turn;
  }
  const d = DEMEANOURS[asker.demeanour];
  const weak = metrics.relevance < 0.25 || metrics.overTime || metrics.words < 15;
  const wantsMore = q.kind === "question" && (weak || s.rapid) && s.random() < Math.max(d.followUpChance, s.rapid ? 0.8 : 0);
  if (wantsMore) {
    const pool = scenarioOf(s).followUps[asker.demeanour];
    s.current = { persona: asker.id, text: pool[Math.floor(s.random() * pool.length)], kind: "follow-up", parent: q.text, askedAt: 0 };
    s.moods[asker.id] = "asking";
  } else {
    nextQuestion(s, 0);
  }
  return turn;
}

export function measure(text, question, asker, { startedAfter = 0, took = 0, limit = 60 } = {}) {
  const w = words(text);
  const q = contentWords(question);
  const focus = new Set(asker.focus.map(stem));
  const a = contentWords(text);
  const overlap = [...q].filter((x) => a.has(x)).length;
  const focusHit = [...focus].some((f) => a.has(f));
  const fillers = countFillers(text);
  return {
    words: w.length,
    startedAfter: Math.round(startedAfter * 10) / 10,
    took: Math.round(took),
    overTime: took > limit,
    fillers,
    fillerRate: w.length ? Math.round((fillers / w.length) * 1000) / 10 : 0,    // per 100 words
    relevance: q.size ? Math.round(Math.min(1, overlap / Math.min(4, q.size) + (focusHit ? 0.25 : 0)) * 100) / 100 : 0,
    usesEvidence: /\d|\b(test|tested|measured|data|result|results|users|customers|percent|survey)\b/i.test(text),
    acknowledgesLimit: /\b(but|however|limit|limitation|not yet|don't know|do not know|unsure|assumption)\b/i.test(text),
  };
}

function reaction(m, demeanour) {
  if (m.overTime) return "checking the time";
  if (m.relevance < 0.25) return demeanour === "supportive" ? "puzzled" : "unconvinced";
  if (demeanour === "skeptical" && !m.usesEvidence) return "unconvinced";
  return "nodding";
}

// ---------- report and journey ----------

export function report(s) {
  const answers = s.turns.filter((t) => t.kind !== "interruption");
  const follow = s.turns.filter((t) => t.kind === "follow-up");
  const interruption = s.turns.find((t) => t.kind === "interruption");
  const avg = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
  let recovery = null;
  if (interruption) {
    // Did the talk after the interruption pick up the thread from before it?
    const before = contentWords(s.talkBeforeInterruption.split(/[.!?]/).filter(Boolean).slice(-2).join(" "));
    const after = contentWords(s.talkText.slice(s.talkBeforeInterruption.length));
    const resumed = [...before].some((x) => after.has(x)) || /\b(back to|as i was saying|returning to|where was i)\b/i.test(s.talkText.slice(s.talkBeforeInterruption.length));
    recovery = { interruption: interruption.text, resumed, answeredBriefly: interruption.metrics.words <= 40 };
  }
  const skills = {
    start: avg(answers.map((t) => t.metrics.startedAfter)),
    structure: answers.length ? answers.filter((t) => !t.metrics.overTime).length / answers.length : null,
    relevance: avg(answers.map((t) => t.metrics.relevance)),
    fillers: avg(s.turns.map((t) => t.metrics.fillerRate)),
    recovery: recovery ? (recovery.resumed ? 1 : 0) : null,
    pushback: follow.length ? avg(follow.map((t) => (t.metrics.usesEvidence ? 0.5 : 0) + (t.metrics.relevance >= 0.25 ? 0.5 : 0))) : null,
  };
  return { scenario: s.scenario, stressors: s.stressors, turns: s.turns, recovery, skills,
           notes: notes(skills), when: null };
}

// Each skill as 0 (needs work) .. 1 (fine), so they can be compared.
export function normalise(skills) {
  const out = {};
  if (skills.start != null) out.start = Math.max(0, Math.min(1, 1 - (skills.start - 2) / 8));       // 2 s fine, 10 s+ needs work
  if (skills.structure != null) out.structure = skills.structure;
  if (skills.relevance != null) out.relevance = Math.min(1, skills.relevance / 0.6);
  if (skills.fillers != null) out.fillers = Math.max(0, Math.min(1, 1 - (skills.fillers - 2) / 8));  // per 100 words
  if (skills.recovery != null) out.recovery = skills.recovery;
  if (skills.pushback != null) out.pushback = skills.pushback;
  return out;
}

function notes(skills) {
  const n = normalise(skills);
  return Object.entries(n).filter(([, v]) => v < 0.6).map(([k]) => `${SKILLS[k]}: worth practising (${DRILLS[k].tip})`);
}

// Across sessions: average each skill over the last five sessions that measured it, pick the weakest.
export function nextDrill(history) {
  const recent = history.slice(-5).map((r) => normalise(r.skills));
  const totals = {};
  for (const r of recent) for (const [k, v] of Object.entries(r)) (totals[k] ||= []).push(v);
  const avgs = Object.entries(totals).map(([k, vs]) => [k, vs.reduce((a, b) => a + b, 0) / vs.length]);
  if (!avgs.length) return { skill: null, drill: { name: "Any scenario", stressors: [], tip: "Do a first run to get suggestions." }, averages: {} };
  avgs.sort((a, b) => a[1] - b[1] || a[0].localeCompare(b[0]));
  const [skill, value] = avgs[0];
  return { skill, value, label: SKILLS[skill], drill: DRILLS[skill], averages: Object.fromEntries(avgs) };
}

export { SCENARIOS, SKILLS, DRILLS };
