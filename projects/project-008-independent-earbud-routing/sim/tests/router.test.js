// Run with: node --test (from the sim folder)
import { test } from "node:test";
import assert from "node:assert/strict";
import { assign, createRouter, describe, endCall, mix, prompt, setMode, setMute, startCall, tick } from "../src/router.js";
import { frameSuccess, link, streamsFor } from "../src/link.js";

const heard = (r, ear) => mix(r)[ear].filter((x) => x.gain > 0).map((x) => `${x.source}:${x.channel}`);

test("coupled mode plays one source in stereo", () => {
  const r = createRouter();
  assert.deepEqual(heard(r, "left"), ["music:L"]);
  assert.deepEqual(heard(r, "right"), ["music:R"]);
});

test("split mode plays a different mono source in each ear", () => {
  const r = setMode(createRouter(), "split");
  assign(r, "left", "podcast"); assign(r, "right", "music");
  assert.deepEqual(heard(r, "left"), ["podcast:mono"]);
  assert.deepEqual(heard(r, "right"), ["music:mono"]);
});

test("muting one ear in coupled mode downmixes the other so nothing is lost", () => {
  const r = setMute(createRouter(), "left", true);
  assert.deepEqual(heard(r, "left"), []);
  assert.deepEqual(heard(r, "right"), ["music:mono"]);
  const plain = setMute(createRouter({ muteDownmix: false }), "left", true);
  assert.deepEqual(heard(plain, "right"), ["music:R"]);
});

test("a call on one ear keeps media going in the other and uses only that bud's microphone", () => {
  const r = createRouter({ callBehaviour: "split", callEar: "right" });
  startCall(r);
  assert.deepEqual(heard(r, "right"), ["call:mono"]);
  assert.deepEqual(heard(r, "left"), ["music:mono"]);
  assert.equal(r.mic, "right");
  assert.throws(() => assign(r, "right", "podcast"), /on the call/);
  assert.throws(() => setMode(r, "coupled"), /Finish the call/);
});

test("pause-media calls use both ears and pause everything", () => {
  const r = createRouter({ callBehaviour: "pause-media" });
  startCall(r);
  assert.deepEqual(heard(r, "left"), ["call:mono"]);
  assert.deepEqual(heard(r, "right"), ["call:mono"]);
  assert.equal(r.playing.music, false);
});

test("after a call the earlier routing and playback position come back", () => {
  const r = createRouter({ callBehaviour: "pause-media" });
  tick(r, 30);
  const before = r.positions.music;
  startCall(r);
  tick(r, 60);
  assert.equal(r.positions.music, before, "paused media does not advance");
  endCall(r);
  assert.equal(r.mode, "coupled");
  assert.deepEqual(heard(r, "left"), ["music:L"]);
  tick(r, 5);
  assert.equal(r.positions.music, before + 5);
  const s = createRouter({ callBehaviour: "split" });
  setMode(s, "split"); assign(s, "left", "podcast"); assign(s, "right", "music");
  startCall(s); endCall(s);
  assert.deepEqual([heard(s, "left"), heard(s, "right")], [["podcast:mono"], ["music:mono"]]);
});

test("navigation prompts duck media and avoid the call ear", () => {
  const r = createRouter();
  prompt(r, "Turn left", 3);
  assert.deepEqual(mix(r).left.map((x) => [x.source, x.gain]), [["music", 0.25], ["nav", 1]]);
  tick(r, 3.1);
  assert.equal(r.prompt, null);
  startCall(r);
  prompt(r, "Turn right", 3);
  assert.deepEqual(r.prompt.ears, ["left"]);
  const both = createRouter({ callBehaviour: "pause-media" });
  startCall(both); prompt(both, "Turn right");
  assert.equal(both.prompt, null);
  assert.match(both.log.at(-1).text, /held during the call/);
});

test("only media can be assigned, and bad input is refused", () => {
  const r = setMode(createRouter(), "split");
  assert.throws(() => assign(r, "left", "call"));
  assert.throws(() => assign(r, "middle", "music"));
  assert.throws(() => setMode(r, "surround"));
});

test("describe gives a plain summary", () => {
  const r = createRouter();
  startCall(r);
  assert.deepEqual(describe(r), { left: "Music", right: "Phone call", mic: "right bud", mode: "split" });
});

// ---------- link model ----------

test("retransmissions make frame loss much rarer", () => {
  assert.equal(frameSuccess(0.1, 0), 0.9);
  assert.ok(Math.abs(frameSuccess(0.1, 2) - 0.999) < 1e-12);
});

test("airtime grows with streams, bitrate and retransmissions; the budget flag trips", () => {
  const one = link({ streams: [{ ear: "left", kbps: 64 }] });
  const two = link({ streams: [{ ear: "left", kbps: 64 }, { ear: "right", kbps: 64 }] });
  assert.ok(two.worstCaseAirtime > one.worstCaseAirtime * 1.9);
  const heavy = link({ streams: [{ ear: "left", kbps: 124 }, { ear: "right", kbps: 124 }, { ear: "right", kbps: 64 }], retransmissions: 6 });
  assert.equal(heavy.fitsBudget, false);
  assert.ok(one.fitsBudget);
  assert.match(one.note, /Rough model/);
});

test("a split-mode call needs a microphone uplink stream", () => {
  const r = createRouter();
  startCall(r);
  const streams = streamsFor(mix(r), r.mic);
  assert.deepEqual(streams.map((s) => `${s.ear}:${s.direction}`), ["left:to bud", "right:to bud", "right:microphone"]);
});
