// Run with: node --test (from the app folder)
import { test } from "node:test";
import assert from "node:assert/strict";
import { answer, countFillers, createSession, finishTalk, measure, nextDrill, normalise, report, talk } from "../src/engine.js";

const GOOD = "We tested it with 40 users and measured a 30 percent drop in errors, but the sample is small.";

function playThrough(s, reply = () => GOOD) {
  for (let i = 0; i < 20 && s.phase === "answer"; i++) answer(s, reply(s.current), { startedAfter: 2, took: 20 });
  finishTalk(s);
  for (let i = 0; i < 20 && s.phase === "answer"; i++) answer(s, reply(s.current), { startedAfter: 2, took: 20 });
  return s;
}

test("fillers are counted as whole words and phrases", () => {
  assert.equal(countFillers("Um, so, you know, it's basically, uh, fine"), 4);
  assert.equal(countFillers("Umbrella likely"), 0);
});

test("relevance rewards using the question's words or the asker's focus", () => {
  const asker = { focus: ["evidence", "evaluation"], demeanour: "skeptical" };
  const q = "What evidence shows your system works better than the simplest alternative?";
  const on = measure("The evidence is a comparison with the simplest alternative system.", q, asker);
  const off = measure("I enjoyed the project and learned a lot about teamwork.", q, asker);
  assert.ok(on.relevance >= 0.75 && off.relevance === 0);
  assert.equal(measure(GOOD, q, asker).usesEvidence, true);
  assert.equal(measure(GOOD, q, asker).acknowledgesLimit, true);
});

test("time limits are enforced and the strict-time drill halves them", () => {
  const plain = createSession("project-defence", { seed: 1 });
  const strict = createSession("project-defence", { seed: 1, stressors: ["strict-time"] });
  assert.equal(strict.answerSeconds, plain.answerSeconds / 2);
  const m = measure("short", "q", { focus: [] }, { took: 70, limit: 60 });
  assert.equal(m.overTime, true);
});

test("an interruption fires at its scheduled second and recovery is detected", () => {
  const s = createSession("project-defence", { seed: 3, stressors: ["interrupt"] });
  assert.ok(s.interruptAt != null);
  talk(s, "Our system schedules exams for three hundred students using a constraint solver.", s.interruptAt - 1);
  assert.equal(s.phase, "talk");
  talk(s, "The solver handles room capacity.", s.interruptAt);
  assert.equal(s.phase, "answer");
  assert.equal(s.current.kind, "interruption");
  answer(s, "From the registry export.", { startedAfter: 1, took: 5 });
  assert.equal(s.phase, "talk");
  talk(s, "Back to my point: the solver also respects room capacity limits.", s.interruptAt + 10);
  const r = report(playThrough(s));
  assert.equal(r.recovery.resumed, true);
  assert.equal(r.recovery.answeredBriefly, true);
});

test("a talk that loses the thread after an interruption is not counted as recovered", () => {
  const s = createSession("project-defence", { seed: 3, stressors: ["interrupt"] });
  talk(s, "Our solver schedules exams for students.", s.interruptAt);
  answer(s, "From the registry.", { startedAfter: 1, took: 5 });
  talk(s, "Anyway, thank you all for coming today.", s.interruptAt + 10);
  assert.equal(report(playThrough(s)).recovery.resumed, false);
});

test("weak answers to a sceptic usually draw a follow-up; the session always ends", () => {
  let followUps = 0;
  for (let seed = 1; seed <= 20; seed++) {
    const s = createSession("project-defence", { seed, stressors: ["skeptical"] });
    playThrough(s, () => "Yes.");
    assert.equal(s.phase, "done");
    followUps += s.turns.filter((t) => t.kind === "follow-up").length;
  }
  assert.ok(followUps >= 20, `expected many follow-ups, got ${followUps}`);
});

test("strong answers rarely draw follow-ups from a supportive panel", () => {
  const s = createSession("job-interview", { seed: 2 });
  playThrough(s);
  assert.ok(s.turns.filter((t) => t.kind === "follow-up").length <= 1);
});

test("the unexpected-question drill adds a question", () => {
  const plain = createSession("pitch", { seed: 5 });
  const drill = createSession("pitch", { seed: 5, stressors: ["unexpected"] });
  assert.equal(drill.queue.length, plain.queue.length + 1);
});

test("sessions are reproducible from their seed", () => {
  const a = playThrough(createSession("pitch", { seed: 9 })).turns.map((t) => t.text);
  const b = playThrough(createSession("pitch", { seed: 9 })).turns.map((t) => t.text);
  assert.deepEqual(a, b);
});

test("the next drill targets the weakest measured skill", () => {
  const slowStarter = { skills: { start: 12, structure: 1, relevance: 0.8, fillers: 1, recovery: 1, pushback: 1 } };
  const filler = { skills: { start: 2, structure: 1, relevance: 0.8, fillers: 12, recovery: null, pushback: null } };
  assert.equal(nextDrill([slowStarter, slowStarter]).skill, "start");
  assert.equal(nextDrill([filler]).skill, "fillers");
  assert.equal(nextDrill([]).skill, null);
  const n = normalise(slowStarter.skills);
  assert.ok(n.start === 0 && n.structure === 1);
});

test("report notes speak about practice, never about the person", () => {
  const s = createSession("project-defence", { seed: 4 });
  const r = report(playThrough(s, () => "Um, like, um, you know, basically, um, yes."));
  const text = r.notes.join(" ").toLowerCase();
  assert.ok(text.includes("worth practising"));
  for (const word of ["anxiety", "anxious", "disorder", "diagnos", "treat"]) assert.ok(!text.includes(word));
});

test("word forms match: 'tested' counts as answering 'test'", () => {
  const asker = { focus: [], demeanour: "neutral" };
  const m = measure("We tested it with three hundred students.", "How did you test the part you are most proud of?", asker);
  assert.ok(m.relevance > 0, `relevance was ${m.relevance}`);
});
