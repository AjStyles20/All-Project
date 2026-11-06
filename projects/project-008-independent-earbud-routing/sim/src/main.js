// Browser demo: runs the routing rules (router.js) and plays generated sounds through the left and
// right channels of the listener's headphones. All text is set with textContent.
import { assign, createRouter, describe, endCall, mix, prompt, setMode, setMute, startCall, tick } from "./router.js";
import { link, streamsFor } from "./link.js";

const $ = (id) => document.getElementById(id);
const r = createRouter();
const STEP = 0.1; // seconds per UI tick
let audio = null;

// ---------- generated sources ----------
// Each source exposes three nodes: L, R (its stereo channels) and mono (their average).
// Per ear, one gain per (source, channel) feeds a ChannelMerger input; mix() sets the gains.

function makeAudio() {
  const ctx = new AudioContext();
  const master = ctx.createGain();
  master.gain.value = Number($("volume").value);
  const merger = ctx.createChannelMerger(2);
  merger.connect(master).connect(ctx.destination);

  const channels = (L, R) => {
    const mono = ctx.createGain();
    mono.gain.value = 0.5;
    L.connect(mono); R.connect(mono);
    return { L, R, mono };
  };
  const sources = {
    music: channels(...music(ctx)),
    podcast: channels(...podcast(ctx)),
    call: channels(...call(ctx)),
    nav: channels(...nav(ctx)),
  };

  const gains = {};
  for (const ear of ["left", "right"]) {
    gains[ear] = {};
    for (const [name, nodes] of Object.entries(sources)) {
      for (const ch of ["L", "R", "mono"]) {
        const g = ctx.createGain();
        g.gain.value = 0;
        nodes[ch].connect(g).connect(merger, 0, ear === "left" ? 0 : 1);
        gains[ear][`${name}:${ch}`] = g;
      }
    }
  }
  return { ctx, master, gains, navNodes: sources.nav };
}

// Music: a bass line on the left channel and a melody on the right, so coupled stereo, downmix and
// split mode all sound different.
function music(ctx) {
  const L = ctx.createGain(), R = ctx.createGain();
  const bass = ctx.createOscillator(), lead = ctx.createOscillator();
  bass.type = "triangle"; lead.type = "square";
  const bassG = ctx.createGain(), leadG = ctx.createGain();
  bassG.gain.value = 0.5; leadG.gain.value = 0.12;
  bass.connect(bassG).connect(L); lead.connect(leadG).connect(R);
  const roots = [110, 87.31, 130.81, 98];                 // A2 F2 C3 G2
  const tune = [440, 523.25, 659.25, 523.25, 349.23, 440, 523.25, 440, 523.25, 659.25, 783.99, 659.25, 392, 493.88, 587.33, 493.88];
  const t0 = ctx.currentTime + 0.05;
  for (let bar = 0; bar < 400; bar++) {                    // ~13 minutes, scheduled up front
    const t = t0 + bar * 2;
    bass.frequency.setValueAtTime(roots[bar % 4], t);
    for (let i = 0; i < 4; i++) lead.frequency.setValueAtTime(tune[(bar % 4) * 4 + i], t + i * 0.5);
  }
  bass.start(); lead.start();
  return [L, R];
}

// Podcast: band-passed noise shaped into syllables, like a voice heard through a wall. Mono.
function podcast(ctx) {
  const buf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
  const data = buf.getChannelData(0);
  for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
  const noise = ctx.createBufferSource();
  noise.buffer = buf; noise.loop = true;
  const band = ctx.createBiquadFilter();
  band.type = "bandpass"; band.frequency.value = 700; band.Q.value = 1.2;
  const env = ctx.createGain();
  env.gain.value = 0;
  const t0 = ctx.currentTime + 0.05;
  let t = t0;
  let seed = 7;
  const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  while (t < t0 + 800) {
    const syllables = 3 + Math.floor(rand() * 6);
    for (let s = 0; s < syllables; s++) {
      const len = 0.12 + rand() * 0.12;
      env.gain.setValueAtTime(0, t);
      env.gain.linearRampToValueAtTime(0.9, t + 0.03);
      env.gain.linearRampToValueAtTime(0, t + len);
      band.frequency.setValueAtTime(500 + rand() * 700, t);
      t += len + 0.04;
    }
    t += 0.35 + rand() * 0.4;                              // pause between phrases
  }
  noise.connect(band).connect(env);
  noise.start();
  return [env, env];
}

// Phone call: a buzzy narrow-band tone that rises and falls, standing in for a voice on a call.
function call(ctx) {
  const osc = ctx.createOscillator();
  osc.type = "sawtooth"; osc.frequency.value = 150;
  const lfo = ctx.createOscillator(), lfoG = ctx.createGain();
  lfo.frequency.value = 3; lfoG.gain.value = 25;
  lfo.connect(lfoG).connect(osc.frequency);
  const band = ctx.createBiquadFilter();
  band.type = "bandpass"; band.frequency.value = 1000; band.Q.value = 2;
  const g = ctx.createGain(); g.gain.value = 0.35;
  osc.connect(band).connect(g);
  osc.start(); lfo.start();
  return [g, g];
}

// Navigation prompt: silent until chime() plays two beeps.
function nav(ctx) {
  const g = ctx.createGain();
  g.gain.value = 0;
  const osc = ctx.createOscillator();
  osc.frequency.value = 880;
  osc.connect(g); osc.start();
  return [g, g];
}

function chime() {
  if (!audio) return;
  const { ctx, navNodes } = audio;
  const g = navNodes.L.gain;                    // L and R are the same node for the prompt
  const t = ctx.currentTime;
  for (const [start, len] of [[0, 0.25], [0.4, 0.25]]) {
    g.setValueAtTime(0, t + start);
    g.linearRampToValueAtTime(0.4, t + start + 0.02);
    g.linearRampToValueAtTime(0, t + start + len);
  }
}

// ---------- apply the router's mix ----------

function applyMix() {
  const m = mix(r);
  if (audio) {
    const now = audio.ctx.currentTime;
    for (const ear of ["left", "right"]) {
      for (const [key, g] of Object.entries(audio.gains[ear])) {
        const hit = m[ear].find((x) => `${x.source}:${x.channel}` === key);
        g.gain.setTargetAtTime(hit ? hit.gain : 0, now, 0.03);
      }
    }
  }
  return m;
}

// ---------- UI ----------

function fmt(seconds) {
  const s = Math.floor(seconds);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

function render() {
  const m = applyMix();
  const d = describe(r);
  $("nowLeft").textContent = d.left;
  $("nowRight").textContent = d.right;
  $("mic").textContent = d.mic;
  $("modeNow").textContent = d.mode;
  $("posMusic").textContent = fmt(r.positions.music);
  $("posPodcast").textContent = fmt(r.positions.podcast);
  for (const [ear, id] of [["left", "meterLeft"], ["right", "meterRight"]]) {
    const level = Math.min(1, m[ear].reduce((a, x) => a + x.gain, 0));
    $(id).style.width = `${Math.round(level * 100)}%`;
  }

  // Controls follow the state.
  const inCall = !!r.call;
  for (const el of document.querySelectorAll("input[name=mode]")) {
    el.checked = el.value === r.mode;
    el.disabled = inCall;
  }
  $("coupled").value = r.coupledSource;
  $("coupled").disabled = r.mode !== "coupled" || inCall;
  $("left").value = r.assignment.left;
  $("right").value = r.assignment.right;
  const onCall = (ear) => inCall && (r.call.ear === ear || r.call.ear === "both");
  $("left").disabled = r.mode !== "split" || onCall("left");
  $("right").disabled = r.mode !== "split" || onCall("right");
  $("behaviour").disabled = inCall;
  $("callEar").disabled = inCall;
  $("call").textContent = inCall ? "End call" : "Start call";

  renderLink(m);
  renderLog();
}

function renderLink(m) {
  const loss = Number($("loss").value), retx = Number($("retx").value);
  $("lossOut").textContent = `${Math.round(loss * 100)}%`;
  $("retxOut").textContent = String(retx);
  const streams = streamsFor(m, r.mic);
  const result = link({ streams, loss, retransmissions: retx });
  const body = $("streams");
  body.replaceChildren();
  for (const [i, s] of result.streams.entries()) {
    const tr = document.createElement("tr");
    const cells = [`${s.ear} bud, ${streams[i].direction}`, `${s.kbps} kbps`, `${(s.frameSuccess * 100).toFixed(3)}%`, String(s.lostFramesPerMin)];
    for (const c of cells) {
      const td = document.createElement("td");
      td.textContent = c;
      tr.append(td);
    }
    body.append(tr);
  }
  if (!result.streams.length) {
    const tr = document.createElement("tr"), td = document.createElement("td");
    td.colSpan = 4; td.textContent = "No streams (both ears silent).";
    tr.append(td); body.append(tr);
  }
  $("worst").textContent = `${Math.round(result.worstCaseAirtime * 100)}%`;
  $("typical").textContent = `${Math.round(result.typicalAirtime * 100)}%`;
  $("fits").textContent = result.fitsBudget ? "fits the 60% audio budget" : "over the 60% audio budget";
  $("linkNote").textContent = result.note;
}

let shownLog = 0;
function renderLog() {
  const list = $("log");
  for (; shownLog < r.log.length; shownLog++) {
    const li = document.createElement("li");
    li.textContent = `${fmt(r.log[shownLog].t)} — ${r.log[shownLog].text}`;
    list.prepend(li);
  }
}

function act(fn) {
  $("error").textContent = "";
  try { fn(); } catch (e) { $("error").textContent = e.message; }
  render();
}

// ---------- wiring ----------

$("start").addEventListener("click", async () => {
  if (!audio) {
    audio = makeAudio();
    $("start").textContent = "Pause sound";
  } else if (audio.ctx.state === "running") {
    await audio.ctx.suspend();
    $("start").textContent = "Resume sound";
  } else {
    await audio.ctx.resume();
    $("start").textContent = "Pause sound";
  }
  render();
});
$("volume").addEventListener("input", () => { if (audio) audio.master.gain.value = Number($("volume").value); });
for (const el of document.querySelectorAll("input[name=mode]")) el.addEventListener("change", () => act(() => setMode(r, el.value)));
$("coupled").addEventListener("change", () => act(() => assign(r, "left", $("coupled").value)));
$("left").addEventListener("change", () => act(() => assign(r, "left", $("left").value)));
$("right").addEventListener("change", () => act(() => assign(r, "right", $("right").value)));
$("muteLeft").addEventListener("change", () => act(() => setMute(r, "left", $("muteLeft").checked)));
$("muteRight").addEventListener("change", () => act(() => setMute(r, "right", $("muteRight").checked)));
$("downmix").addEventListener("change", () => act(() => { r.settings.muteDownmix = $("downmix").checked; }));
$("behaviour").addEventListener("change", () => act(() => { r.settings.callBehaviour = $("behaviour").value; }));
$("callEar").addEventListener("change", () => act(() => { r.settings.callEar = $("callEar").value; }));
$("call").addEventListener("click", () => act(() => (r.call ? endCall(r) : startCall(r))));
$("prompt").addEventListener("click", () => act(() => {
  prompt(r, "In 200 metres, turn left", 2.5);
  if (r.prompt) chime();
}));
$("loss").addEventListener("input", render);
$("retx").addEventListener("input", render);

// Time moves only while sound is running (or always, if sound was never started).
setInterval(() => {
  if (audio && audio.ctx.state !== "running") return;
  const hadPrompt = !!r.prompt;
  tick(r, STEP);
  if (hadPrompt && !r.prompt) render();
  else if (Math.round(r.time * 10) % 5 === 0) render();
}, STEP * 1000);

render();
