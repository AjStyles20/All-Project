// A rough model of the radio link for one or two LE Audio connected isochronous streams (CIS).
// For intuition, not for engineering sign-off: real figures depend on the controller, PHY,
// scheduling, interference and firmware. Every assumption is a named parameter below.

export const DEFAULTS = {
  intervalMs: 10,        // LC3 frame / ISO interval
  phyMbps: 2,            // LE 2M PHY
  overheadBits: 80 + 32, // preamble, access address, header, MIC/CRC (approximate)
  ifsUs: 150,            // inter-frame space
  ackUs: 80,             // empty acknowledgement packet, approximate
  budgetShare: 0.6,      // share of air time we allow audio to use, leaving room for other traffic
};

// Per-stream success: a frame is lost only if the first try and every retransmission fail.
export function frameSuccess(loss, retransmissions) {
  return 1 - loss ** (retransmissions + 1);
}

export function link({ streams, loss = 0.05, retransmissions = 2, ...over } = {}) {
  const p = { ...DEFAULTS, ...over };
  const perStream = streams.map((s) => {
    const bytes = Math.ceil((s.kbps * 1000 * p.intervalMs) / 1000 / 8);
    const packetUs = ((bytes * 8 + p.overheadBits) / (p.phyMbps * 1e6)) * 1e6;
    const tryUs = packetUs + p.ifsUs + p.ackUs + p.ifsUs;
    // Expected tries per frame: geometric, capped by the retransmission limit.
    let expected = 0;
    for (let k = 0; k <= retransmissions; k++) expected += loss ** k;
    const ok = frameSuccess(loss, retransmissions);
    const framesPerMin = 60000 / p.intervalMs;
    return { ear: s.ear, kbps: s.kbps, bytes, worstCaseUs: tryUs * (retransmissions + 1), expectedUs: tryUs * expected,
             frameSuccess: ok, lostFramesPerMin: Math.round((1 - ok) * framesPerMin * 10) / 10 };
  });
  const intervalUs = p.intervalMs * 1000;
  const worst = perStream.reduce((a, s) => a + s.worstCaseUs, 0) / intervalUs;
  const typical = perStream.reduce((a, s) => a + s.expectedUs, 0) / intervalUs;
  return {
    params: { ...p, loss, retransmissions },
    streams: perStream,
    worstCaseAirtime: Math.round(worst * 1000) / 1000,
    typicalAirtime: Math.round(typical * 1000) / 1000,
    fitsBudget: worst <= p.budgetShare,
    note: "Rough model: assumptions are listed in params. Not a measurement.",
  };
}

// Streams implied by a routing mix: coupled stereo uses one stream per bud carrying its channel;
// split mode uses one mono stream per bud; a call adds a microphone uplink from the call bud.
export function streamsFor(mixed, mic, { mediaKbps = 64, callKbps = 32 } = {}) {
  const streams = [];
  for (const ear of ["left", "right"]) {
    const live = mixed[ear].filter((x) => x.gain > 0);
    if (!live.length) continue;
    const isCall = live.some((x) => x.source === "call");
    streams.push({ ear, kbps: isCall ? callKbps : mediaKbps, direction: "to bud" });
  }
  if (mic === "left" || mic === "right") streams.push({ ear: mic, kbps: callKbps, direction: "microphone" });
  if (mic === "both") streams.push({ ear: "left", kbps: callKbps, direction: "microphone" });
  return streams;
}
