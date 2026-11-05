// World data for "Lanterns of Brinewold": an original setting, party and story.
// Everything here (names, places, lines) was written for this project; see docs/IP_NOTES.md.

export const TILE = 32;
export const MAP_W = 60;
export const MAP_H = 20;

// . grass   , reeds (slow)   ~ water   # ruin wall   = ferry raft (walkable after the ferry is called)
// | gate (walkable once all lanterns are lit)
export function buildMap() {
  const rows = [];
  for (let y = 0; y < MAP_H; y++) {
    let row = "";
    for (let x = 0; x < MAP_W; x++) {
      let c = ".";
      if (y === 0 || y === MAP_H - 1 || x === 0 || x === MAP_W - 1) c = "~";
      else if (x >= 19 && x <= 21) c = y >= 9 && y <= 10 ? "=" : "~";          // the Grey Ferry river
      else if (x === 41) c = y >= 8 && y <= 11 ? "|" : "#";                     // the drowned chapel wall
      else if ((x + y * 3) % 11 === 0 && x < 40) c = ",";                       // reed beds
      else if ((x >= 8 && x <= 10 && y >= 3 && y <= 5) || (x >= 28 && x <= 30 && y >= 13 && y <= 15)) c = "#";
      row += c;
    }
    rows.push(row);
  }
  return rows;
}

export const HEROES = [
  {
    id: "bran", name: "Brannoch Vey", role: "Anchor-brawler", key: "1",
    blurb: "A retired dock fighter who swings a ship's anchor and apologises to nobody.",
    hp: 160, speed: 105, colour: "#c8794a",
    attack: { kind: "melee", damage: 18, range: 46, cooldown: 0.55 },
    special: { name: "Anchor Swing", kind: "spin", damage: 30, radius: 70, cooldown: 6 },
  },
  {
    id: "oswin", name: "Oswin Tallow", role: "Lamplighter", key: "2",
    blurb: "A nervous lamplighter with a satchel of firebombs. The only one who can relight the waymarkers.",
    hp: 95, speed: 120, colour: "#e2b13c",
    attack: { kind: "bolt", damage: 12, range: 240, cooldown: 0.7, speed: 320 },
    special: { name: "Firebomb", kind: "bomb", damage: 36, radius: 72, cooldown: 7, speed: 260 },
  },
  {
    id: "ilse", name: "Ilse Marrow", role: "Hedge-healer", key: "3",
    blurb: "Heals by bargaining with marsh spirits. Keeps a tally of who owes her.",
    hp: 100, speed: 112, colour: "#6fae7a",
    attack: { kind: "bolt", damage: 9, range: 200, cooldown: 0.8, speed: 280 },
    special: { name: "Marsh Bargain", kind: "heal", amount: 38, radius: 170, cooldown: 8 },
  },
  {
    id: "kettle", name: "Kettle", role: "Clockwork heron", key: "4",
    blurb: "A brass heron built by Oswin's late aunt. Spots weak points and judges everyone silently.",
    hp: 85, speed: 140, colour: "#8fb0c9",
    attack: { kind: "melee", damage: 11, range: 40, cooldown: 0.35 },
    special: { name: "Mark Weakness", kind: "mark", radius: 210, duration: 6, cooldown: 9 },
  },
];

export const ENEMIES = {
  shambler: { name: "Drowned shambler", hp: 48, speed: 55, damage: 11, range: 30, cooldown: 1.2, aggro: 230, shape: "square", colour: "#5a7f73" },
  wisp: { name: "Murk wisp", hp: 30, speed: 70, damage: 7, range: 180, cooldown: 1.8, aggro: 260, shape: "diamond", colour: "#9b8cc9", ranged: true },
  // Tuned with a scripted bot (docs/BALANCE.md): at 520 HP it won in 6.6 s unhurt; now about 26 s with two
  // heroes down. Needs a human playtest; the bot is a rough instrument.
  eater: { name: "The Lantern-Eater", hp: 2200, speed: 52, damage: 20, range: 56, cooldown: 1.4, aggro: 400, shape: "octagon", colour: "#3c3a52", boss: true,
           slam: { name: "Swallow the Light", every: 6, warning: 1.2, radius: 130, damage: 30 } },
};

export const SPAWNS = [
  { type: "shambler", x: 12, y: 7 }, { type: "shambler", x: 14, y: 12 }, { type: "wisp", x: 16, y: 4 },
  { type: "shambler", x: 26, y: 6 }, { type: "wisp", x: 31, y: 9 }, { type: "shambler", x: 35, y: 12 },
  { type: "shambler", x: 38, y: 5 }, { type: "wisp", x: 36, y: 15 },
];

export const NPCS = [
  { id: "dilly", name: "Dilly Pask, ferrywoman", x: 17, y: 9,
    lines: ["Ferry's free, the toll's not. Light the waymarkers past the river and we'll call it even.",
            "The Murk took the chapel. Without the lanterns, nothing comes back out of that fog."] },
];

export const LANTERNS = [{ id: "east", x: 25, y: 3 }, { id: "low", x: 33, y: 16 }, { id: "chapel", x: 39, y: 9 }];

export const QUEST = [
  { id: "ferry", text: "Find the ferrywoman by the river." },
  { id: "lanterns", text: "Relight the three waymarker lanterns (switch to Oswin and press E beside each)." },
  { id: "boss", text: "Enter the drowned chapel and defeat the Lantern-Eater." },
  { id: "done", text: "Brinewold's lights are burning again." },
];

// Banter: [speaker id, line]. Picked by event; at most one line every few seconds.
export const BANTER = {
  start: [["bran", "Fog, mud and a heron. Lovely holiday, Oswin."], ["kettle", "*clicks disapprovingly*"]],
  firstKill: [["ilse", "That's one less thing that wants to drown us. Write it down."], ["bran", "Stay down this time!"]],
  heal: [["ilse", "That one's on credit. Interest is steep."], ["ilse", "Hold still, the spirits hate fidgeting."]],
  bomb: [["oswin", "Sorry! Sorry. That was meant to be smaller."], ["bran", "Warn a man before you throw fire, Tallow!"]],
  downed: [["ilse", "Up you get, I'm not carrying you."], ["bran", "Nobody naps on my watch."]],
  lantern: [["oswin", "Light's back. You can stop holding my sleeve now, Bran."], ["kettle", "*a pleased whirr*"]],
  boss: [["bran", "That's not a fish. Why is it eating the light?"], ["oswin", "Because it's hungry and we're the last lamps left."]],
  win: [["ilse", "Ferry's paid, lights are lit. Somebody owes me dinner."], ["kettle", "*the heron bows, very slightly*"]],
};
