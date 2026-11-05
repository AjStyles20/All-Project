// Game rules. Pure and deterministic: no DOM, no clock, a seeded random generator.
// update(state, input, dt) advances the world; the browser layer only draws and reads keys.
import { BANTER, ENEMIES, HEROES, LANTERNS, NPCS, QUEST, SPAWNS, TILE, buildMap } from "./data.js";

const REVIVE_TIME = 2.5;
const REVIVE_RANGE = 44;
// Generous: a hero standing on the tile next to a lantern or person should always reach it.
const INTERACT_RANGE = 60;
const BANTER_GAP = 4;
export const MARK_BONUS = 1.5;   // was 2: with ~2/3 uptime it trivialised the boss

export function rng(seed) {
  // mulberry32: small, fast, reproducible
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const centre = (tx, ty) => ({ x: tx * TILE + TILE / 2, y: ty * TILE + TILE / 2 });
const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);

function makeEnemy(type, tx, ty, id) {
  const e = ENEMIES[type];
  return { id, type, ...centre(tx, ty), hp: e.hp, maxHp: e.hp, cd: 0, markedFor: 0, alive: true };
}

export function createGame(seed = 1) {
  const start = centre(4, 10);
  const heroes = HEROES.map((h, i) => ({
    id: h.id, x: start.x - i * 18, y: start.y + (i % 2) * 18, hp: h.hp, maxHp: h.hp,
    cd: 0, specialCd: 0, facing: { x: 1, y: 0 }, downed: false, revive: 0,
  }));
  return {
    seed, time: 0, map: buildMap(), heroes, active: 0,
    enemies: SPAWNS.map((s, i) => makeEnemy(s.type, s.x, s.y, `e${i}`)),
    projectiles: [], effects: [], nextId: 100,
    quest: 0, lit: [], ferry: false, gate: false, bossSpawned: false,
    kills: 0, over: false, won: false,
    log: [], lastBanter: -99, said: {},
    random: rng(seed),
  };
}

// ---------- map ----------

export function tileAt(state, x, y) {
  const tx = Math.floor(x / TILE);
  const ty = Math.floor(y / TILE);
  return state.map[ty]?.[tx] ?? "~";
}

export function walkable(state, x, y) {
  const t = tileAt(state, x, y);
  if (t === "~" || t === "#") return false;
  if (t === "=") return state.ferry;
  if (t === "|") return state.gate;
  return true;
}

function move(state, body, dx, dy, speed, dt) {
  const len = Math.hypot(dx, dy);
  if (!len) return;
  const slow = tileAt(state, body.x, body.y) === "," ? 0.6 : 1;
  const step = (speed * slow * dt) / len;
  const nx = body.x + dx * step;
  const ny = body.y + dy * step;
  // Slide along walls: try both axes, then each separately.
  if (walkable(state, nx, ny)) { body.x = nx; body.y = ny; }
  else if (walkable(state, nx, body.y)) body.x = nx;
  else if (walkable(state, body.x, ny)) body.y = ny;
}

// ---------- events ----------

function say(state, event, force = false) {
  const lines = BANTER[event];
  if (!lines || (!force && state.time - state.lastBanter < BANTER_GAP)) return;
  const n = state.said[event] || 0;
  const [speaker, text] = lines[n % lines.length];
  state.said[event] = n + 1;
  state.lastBanter = state.time;
  const who = HEROES.find((h) => h.id === speaker)?.name ?? speaker;
  state.log.push({ t: state.time, who, text });
}

function note(state, text) {
  state.log.push({ t: state.time, who: "", text });
}

function hurtEnemy(state, enemy, amount) {
  if (!enemy.alive) return;
  const mult = enemy.markedFor > 0 ? MARK_BONUS : 1;
  enemy.hp -= amount * mult;
  state.effects.push({ kind: "number", x: enemy.x, y: enemy.y - 14, text: String(Math.round(amount * mult)), life: 0.8 });
  if (enemy.hp <= 0) {
    enemy.alive = false;
    state.kills += 1;
    if (state.kills === 1) say(state, "firstKill", true);
    if (ENEMIES[enemy.type].boss) win(state);
  }
}

function hurtHero(state, hero, amount) {
  if (hero.downed) return;
  hero.hp = Math.max(0, hero.hp - amount);
  state.effects.push({ kind: "number", x: hero.x, y: hero.y - 14, text: String(amount), life: 0.8, hurt: true });
  if (hero.hp === 0) {
    hero.downed = true;
    hero.revive = 0;
    note(state, `${HEROES.find((h) => h.id === hero.id).name} is down! Stand next to them to help them up.`);
    say(state, "downed", true);
    if (state.heroes.every((h) => h.downed)) {
      state.over = true;
      note(state, "The whole party has fallen. The Murk closes in.");
    }
  }
}

function win(state) {
  state.won = true;
  state.quest = 3;
  note(state, QUEST[3].text);
  say(state, "win", true);
}

// ---------- abilities ----------

function nearestEnemy(state, from, range) {
  let best = null;
  let bestD = range;
  for (const e of state.enemies) {
    if (!e.alive) continue;
    const d = dist(from, e);
    if (d <= bestD) { best = e; bestD = d; }
  }
  return best;
}

function basicAttack(state, hero, def) {
  const a = def.attack;
  if (a.kind === "melee") {
    for (const e of state.enemies) if (e.alive && dist(hero, e) <= a.range + 12) hurtEnemy(state, e, a.damage);
  } else {
    const target = nearestEnemy(state, hero, a.range);
    const dir = target ? { x: target.x - hero.x, y: target.y - hero.y } : hero.facing;
    const len = Math.hypot(dir.x, dir.y) || 1;
    state.projectiles.push({ owner: "hero", x: hero.x, y: hero.y, vx: (dir.x / len) * a.speed, vy: (dir.y / len) * a.speed,
                             damage: a.damage, range: a.range, travelled: 0 });
  }
  hero.cd = a.cooldown;
}

function special(state, hero, def) {
  const s = def.special;
  if (s.kind === "spin") {
    for (const e of state.enemies) if (e.alive && dist(hero, e) <= s.radius) hurtEnemy(state, e, s.damage);
    state.effects.push({ kind: "ring", x: hero.x, y: hero.y, r: s.radius, life: 0.3 });
  } else if (s.kind === "bomb") {
    const target = nearestEnemy(state, hero, 260);
    const dir = target ? { x: target.x - hero.x, y: target.y - hero.y } : hero.facing;
    const len = Math.hypot(dir.x, dir.y) || 1;
    const reach = target ? Math.min(len, 260) : 160;
    state.projectiles.push({ owner: "hero", bomb: true, x: hero.x, y: hero.y, vx: (dir.x / len) * s.speed, vy: (dir.y / len) * s.speed,
                             damage: s.damage, radius: s.radius, range: reach, travelled: 0 });
    say(state, "bomb");
  } else if (s.kind === "heal") {
    for (const h of state.heroes) {
      if (!h.downed && dist(hero, h) <= s.radius) h.hp = Math.min(h.maxHp, h.hp + s.amount);
    }
    state.effects.push({ kind: "ring", x: hero.x, y: hero.y, r: s.radius, life: 0.4, heal: true });
    say(state, "heal");
  } else if (s.kind === "mark") {
    for (const e of state.enemies) if (e.alive && dist(hero, e) <= s.radius) e.markedFor = s.duration;
    state.effects.push({ kind: "ring", x: hero.x, y: hero.y, r: s.radius, life: 0.4 });
  }
  hero.specialCd = s.cooldown;
}

// ---------- interaction ----------

function interact(state, hero) {
  const def = HEROES.find((h) => h.id === hero.id);
  for (const npc of NPCS) {
    const p = centre(npc.x, npc.y);
    if (dist(hero, p) <= INTERACT_RANGE) {
      note(state, `${npc.name}: "${npc.lines[state.quest === 0 ? 0 : 1]}"`);
      if (state.quest === 0) {
        state.quest = 1;
        state.ferry = true;
        note(state, "The ferry raft is in place. New goal: " + QUEST[1].text);
      }
      return true;
    }
  }
  for (const l of LANTERNS) {
    const p = centre(l.x, l.y);
    if (dist(hero, p) > INTERACT_RANGE || state.lit.includes(l.id)) continue;
    if (state.quest < 1) { note(state, "A dead lantern. Someone at the river may know what to do."); return true; }
    if (def.id !== "oswin") { note(state, `${def.name} fumbles with the wick. Only Oswin can light it (press 2).`); return true; }
    state.lit.push(l.id);
    say(state, "lantern", true);
    // The Murk answers each lit lantern with an ambush.
    for (let i = 0; i < 2; i++) {
      state.enemies.push(makeEnemy(i ? "wisp" : "shambler", l.x + (i ? 3 : -3), l.y + (i ? -2 : 2), `e${state.nextId++}`));
    }
    if (state.lit.length === LANTERNS.length) {
      state.gate = true;
      state.quest = 2;
      note(state, "The chapel gate grinds open. New goal: " + QUEST[2].text);
    } else {
      note(state, `Lantern lit (${state.lit.length} of ${LANTERNS.length}).`);
    }
    return true;
  }
  return false;
}

// ---------- the update step ----------

export function update(state, input, dt) {
  if (state.over || state.won || input.paused) return state;
  state.time += dt;
  if (state.time < dt * 1.5) say(state, "start", true);

  if (input.switchTo != null && state.heroes[input.switchTo] && !state.heroes[input.switchTo].downed) {
    state.active = input.switchTo;
  }
  if (state.heroes[state.active].downed) {
    const next = state.heroes.findIndex((h) => !h.downed);
    if (next >= 0) state.active = next;
  }
  const leader = state.heroes[state.active];

  state.heroes.forEach((hero, i) => {
    const def = HEROES[i];
    hero.cd = Math.max(0, hero.cd - dt);
    hero.specialCd = Math.max(0, hero.specialCd - dt);
    if (hero.downed) return;
    if (i === state.active) {
      const { x, y } = input.move || { x: 0, y: 0 };
      if (x || y) {
        move(state, hero, x, y, def.speed, dt);
        const len = Math.hypot(x, y);
        hero.facing = { x: x / len, y: y / len };
      }
      if (input.attack && hero.cd === 0) basicAttack(state, hero, def);
      if (input.special && hero.specialCd === 0) special(state, hero, def);
    } else {
      companion(state, hero, def, leader, i, dt);
    }
  });
  if (input.interact) interact(state, leader);

  // Revive: a standing hero next to a downed one helps them up.
  for (const h of state.heroes) {
    if (!h.downed) continue;
    const helper = state.heroes.some((o) => o !== h && !o.downed && dist(o, h) <= REVIVE_RANGE);
    h.revive = helper ? h.revive + dt : Math.max(0, h.revive - dt);
    if (h.revive >= REVIVE_TIME) {
      h.downed = false;
      h.hp = Math.round(h.maxHp * 0.3);
      note(state, `${HEROES.find((d) => d.id === h.id).name} is back on their feet.`);
    }
  }

  // Boss appears when the party first steps into the chapel.
  if (state.gate && !state.bossSpawned && leader.x > 42 * TILE) {
    state.bossSpawned = true;
    state.enemies.push(makeEnemy("eater", 52, 10, "boss"));
    say(state, "boss", true);
  }

  for (const e of state.enemies) enemyAct(state, e, dt);
  stepProjectiles(state, dt);
  for (const fx of state.effects) fx.life -= dt;
  state.effects = state.effects.filter((fx) => fx.life > 0);
  state.enemies = state.enemies.filter((e) => e.alive);
  if (state.log.length > 60) state.log.splice(0, state.log.length - 60);
  return state;
}

function companion(state, hero, def, leader, i, dt) {
  // Healer first: patch up anyone below 40 %.
  if (def.special.kind === "heal" && hero.specialCd === 0 &&
      state.heroes.some((h) => !h.downed && h.hp < h.maxHp * 0.4 && dist(hero, h) <= def.special.radius)) {
    special(state, hero, def);
  }
  // Go to a downed friend, else follow the leader in loose formation.
  const downed = state.heroes.find((h) => h.downed);
  const angle = (i / state.heroes.length) * Math.PI * 2;
  const goal = downed ?? { x: leader.x + Math.cos(angle) * 40, y: leader.y + Math.sin(angle) * 40 };
  const far = dist(hero, goal);
  if (far > (downed ? 20 : 30)) move(state, hero, goal.x - hero.x, goal.y - hero.y, def.speed, dt);
  const target = nearestEnemy(state, hero, def.attack.kind === "melee" ? def.attack.range + 12 : def.attack.range * 0.8);
  if (target && hero.cd === 0) basicAttack(state, hero, def);
}

function enemyAct(state, e, dt) {
  if (!e.alive) return;
  const def = ENEMIES[e.type];
  e.cd = Math.max(0, e.cd - dt);
  e.markedFor = Math.max(0, e.markedFor - dt);
  if (def.slam) bossSlam(state, e, def.slam, dt);
  let target = null;
  let best = def.aggro;
  for (const h of state.heroes) {
    if (h.downed) continue;
    const d = dist(e, h);
    if (d < best) { best = d; target = h; }
  }
  if (!target) return;
  const keep = def.ranged ? def.range * 0.7 : def.range * 0.8;
  if (best > keep) {
    const jitter = (state.random() - 0.5) * 0.4;
    move(state, e, target.x - e.x + jitter * 20, target.y - e.y, def.speed, dt);
  }
  if (best <= def.range && e.cd === 0) {
    e.cd = def.cooldown;
    if (def.ranged) {
      const len = best || 1;
      state.projectiles.push({ owner: "enemy", x: e.x, y: e.y, vx: ((target.x - e.x) / len) * 200, vy: ((target.y - e.y) / len) * 200,
                               damage: def.damage, range: def.range + 20, travelled: 0 });
    } else {
      hurtHero(state, target, def.damage);
    }
  }
}

// The boss telegraphs its area attack with a shrinking ring, so a player can step out of it.
function bossSlam(state, e, slam, dt) {
  e.slamTimer = (e.slamTimer ?? slam.every) - dt;
  if (e.slamWarn == null && e.slamTimer <= slam.warning) {
    e.slamWarn = slam.warning;
    state.effects.push({ kind: "ring", x: e.x, y: e.y, r: slam.radius, life: slam.warning, warn: true });
    if (!state.said.slamHint) { state.said.slamHint = 1; note(state, `The Lantern-Eater inhales... (${slam.name}: step out of the ring!)`); }
  }
  if (e.slamWarn != null) {
    e.slamWarn -= dt;
    if (e.slamWarn <= 0) {
      for (const h of state.heroes) if (!h.downed && dist(e, h) <= slam.radius) hurtHero(state, h, slam.damage);
      e.slamWarn = null;
      e.slamTimer = slam.every;
    }
  }
}

function stepProjectiles(state, dt) {
  for (const p of state.projectiles) {
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.travelled += Math.hypot(p.vx, p.vy) * dt;
    let hit = !walkable(state, p.x, p.y) && tileAt(state, p.x, p.y) === "#";
    if (p.owner === "hero") {
      const enemy = state.enemies.find((e) => e.alive && dist(p, e) < (ENEMIES[e.type].boss ? 30 : 16));
      if (enemy) hit = true;
      if (hit || p.travelled >= p.range) {
        if (p.bomb) {
          for (const e of state.enemies) if (e.alive && dist(p, e) <= p.radius) hurtEnemy(state, e, p.damage);
          state.effects.push({ kind: "ring", x: p.x, y: p.y, r: p.radius, life: 0.35, fire: true });
        } else if (enemy) {
          hurtEnemy(state, enemy, p.damage);
        }
        p.done = true;
      }
    } else {
      const hero = state.heroes.find((h) => !h.downed && dist(p, h) < 14);
      if (hero) { hurtHero(state, hero, p.damage); p.done = true; }
      if (hit || p.travelled >= p.range) p.done = true;
    }
  }
  state.projectiles = state.projectiles.filter((p) => !p.done);
}

// ---------- saving ----------

export function serialise(state) {
  const { random, map, ...rest } = state;
  return JSON.stringify({ v: 1, ...rest, randomState: Math.floor(state.random() * 2 ** 32) });
}

export function deserialise(text) {
  const data = JSON.parse(text);
  if (data.v !== 1 || !Array.isArray(data.heroes) || data.heroes.length !== HEROES.length) throw new Error("Not a save from this version.");
  const { v, randomState, ...rest } = data;
  return { ...createGame(data.seed), ...rest, map: buildMap(), random: rng(randomState) };
}

export { QUEST, HEROES, ENEMIES, LANTERNS, NPCS, dist, centre };
