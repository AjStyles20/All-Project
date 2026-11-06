// Per-ear routing rules for a pair of earbuds, as a *controlled* LE Audio prototype would run
// them (research Pass 002, level C: our own source and firmware). Pure and testable; the browser
// demo plays its output through the left and right channels of ordinary headphones.
//
// Modes:   coupled  both buds play one source in stereo (normal earbuds)
//          split    each bud plays its own source, downmixed to mono
// Extras:  per-ear mute, calls (pause media, or carry the call on one ear while media continues
//          on the other), navigation prompts that duck whatever is playing, microphone selection,
//          and returning to the earlier setup after a call.

export const SOURCES = {
  music: { label: "Music", kind: "media" },
  podcast: { label: "Podcast", kind: "media" },
  call: { label: "Phone call", kind: "call" },
  nav: { label: "Navigation prompt", kind: "prompt" },
};
const EARS = ["left", "right"];
const other = (ear) => (ear === "left" ? "right" : "left");

export function createRouter({ callBehaviour = "split", callEar = "right", muteDownmix = true } = {}) {
  return {
    mode: "coupled",
    coupledSource: "music",
    assignment: { left: "music", right: "podcast" },     // used in split mode
    mute: { left: false, right: false },
    playing: { music: true, podcast: true },
    positions: { music: 0, podcast: 0 },
    call: null,                                          // { ear | "both", saved }
    prompt: null,                                        // { ears, endsAt, text }
    mic: null,
    settings: { callBehaviour, callEar, muteDownmix },
    time: 0,
    log: [],
  };
}

function note(r, text) {
  r.log.push({ t: Math.round(r.time * 10) / 10, text });
}

export function setMode(r, mode) {
  if (!["coupled", "split"].includes(mode)) throw new Error("Mode must be coupled or split.");
  if (r.call) throw new Error("Finish the call before changing mode.");
  if (r.mode !== mode) note(r, `Mode: ${mode}`);
  r.mode = mode;
  return r;
}

export function assign(r, ear, source) {
  if (!EARS.includes(ear)) throw new Error("Ear must be left or right.");
  if (SOURCES[source]?.kind !== "media") throw new Error("Only media sources can be assigned to an ear.");
  if (r.call && (r.call.ear === ear || r.call.ear === "both")) throw new Error(`The ${ear} ear is on the call.`);
  if (r.mode === "coupled") {
    r.coupledSource = source;
  } else {
    r.assignment[ear] = source;
  }
  note(r, r.mode === "coupled" ? `Both ears: ${SOURCES[source].label}` : `${ear} ear: ${SOURCES[source].label}`);
  return r;
}

export function setMute(r, ear, muted) {
  if (!EARS.includes(ear)) throw new Error("Ear must be left or right.");
  r.mute[ear] = !!muted;
  note(r, `${ear} ear ${muted ? "muted" : "unmuted"}`);
  return r;
}

export function startCall(r) {
  if (r.call) return r;
  const saved = { mode: r.mode, coupledSource: r.coupledSource, assignment: { ...r.assignment }, playing: { ...r.playing } };
  if (r.settings.callBehaviour === "pause-media") {
    r.call = { ear: "both", saved };
    for (const s of Object.keys(r.playing)) r.playing[s] = false;
    r.mic = "both";
    note(r, "Call started on both ears; media paused.");
  } else {
    const ear = r.settings.callEar;
    // Media carries on in the other ear; it switches to split mode for the length of the call.
    const keep = r.mode === "coupled" ? r.coupledSource : r.assignment[other(ear)];
    r.mode = "split";
    r.assignment[other(ear)] = keep;
    r.call = { ear, saved };
    r.mic = ear;          // the bud carrying the call uses its microphone; the other mic stays off
    note(r, `Call on the ${ear} ear (its microphone on); ${SOURCES[keep].label.toLowerCase()} continues on the ${other(ear)} ear.`);
  }
  return r;
}

export function endCall(r) {
  if (!r.call) return r;
  const { saved } = r.call;
  r.mode = saved.mode;
  r.coupledSource = saved.coupledSource;
  r.assignment = { ...saved.assignment };
  r.playing = { ...saved.playing };
  r.call = null;
  r.mic = null;
  note(r, "Call ended; previous routing restored, playback positions kept.");
  return r;
}

export function prompt(r, text, seconds = 3) {
  // A prompt plays on the ears not carrying a call and ducks what is there.
  const ears = r.call ? EARS.filter((e) => r.call.ear !== e && r.call.ear !== "both") : EARS;
  if (!ears.length) {
    note(r, `Prompt held during the call: "${text}"`);
    return r;
  }
  r.prompt = { ears, endsAt: r.time + seconds, text };
  note(r, `Prompt on ${ears.join(" and ")}: "${text}"`);
  return r;
}

export function tick(r, dt) {
  r.time += dt;
  for (const s of Object.keys(r.positions)) if (r.playing[s] && audible(r, s)) r.positions[s] += dt;
  if (r.prompt && r.time >= r.prompt.endsAt) r.prompt = null;
  return r;
}

function audible(r, source) {
  const m = mix(r);
  return EARS.some((e) => m[e].some((x) => x.source === source && x.gain > 0));
}

// What each ear hears right now: [{ source, gain, channel }] where channel is "L", "R" or "mono".
export function mix(r) {
  const out = { left: [], right: [] };
  const DUCK = 0.25;
  for (const ear of EARS) {
    const ducked = r.prompt?.ears.includes(ear);
    if (r.call && (r.call.ear === ear || r.call.ear === "both")) {
      out[ear].push({ source: "call", gain: 1, channel: "mono" });
      continue;
    }
    if (r.mode === "coupled") {
      const s = r.coupledSource;
      if (r.playing[s]) out[ear].push({ source: s, gain: ducked ? DUCK : 1, channel: ear === "left" ? "L" : "R" });
    } else {
      const s = r.assignment[ear];
      if (r.playing[s]) out[ear].push({ source: s, gain: ducked ? DUCK : 1, channel: "mono" });
    }
    if (ducked) out[ear].push({ source: "nav", gain: 1, channel: "mono" });
  }
  // Muting: silence that ear. In coupled mode the other ear switches to a mono downmix so no part
  // of a stereo mix (for example a voice panned to one side) is lost.
  for (const ear of EARS) {
    if (!r.mute[ear]) continue;
    out[ear] = out[ear].map((x) => ({ ...x, gain: 0 }));
    if (r.settings.muteDownmix && !r.mute[other(ear)]) {
      out[other(ear)] = out[other(ear)].map((x) => (x.channel === "L" || x.channel === "R" ? { ...x, channel: "mono" } : x));
    }
  }
  return out;
}

export function describe(r) {
  const m = mix(r);
  const say = (ear) => (m[ear].filter((x) => x.gain > 0).map((x) => `${SOURCES[x.source].label}${x.channel === "mono" ? "" : ` (${x.channel})`}${x.gain < 1 ? " quietly" : ""}`).join(" + ") || "silence");
  return { left: say("left"), right: say("right"), mic: r.mic ? `${r.mic === "both" ? "both buds" : `${r.mic} bud`}` : "off", mode: r.mode };
}
