// Run with: node --test (from the game folder)
import { test } from "node:test";
import assert from "node:assert/strict";
import { TILE } from "../src/data.js";
import { ENEMIES, HEROES, LANTERNS, MARK_BONUS, NPCS, centre, createGame, deserialise, serialise, update, walkable } from "../src/engine.js";

const idle = { move: { x: 0, y: 0 } };
const step = (s, input = idle, n = 1, dt = 1 / 60) => { for (let i = 0; i < n; i++) update(s, input, dt); return s; };
const clearEnemies = (s) => { s.enemies = []; return s; };
const place = (body, tx, ty) => Object.assign(body, centre(tx, ty));

test("the river blocks the way until the ferrywoman is found", () => {
  const s = createGame();
  const raft = centre(20, 9);
  assert.equal(walkable(s, raft.x, raft.y), false);
  clearEnemies(s);
  place(s.heroes[0], NPCS[0].x, NPCS[0].y + 1);
  step(s, { ...idle, interact: true });
  assert.equal(s.quest, 1);
  assert.equal(walkable(s, raft.x, raft.y), true);
});

test("only Oswin can relight lanterns, and each one brings an ambush", () => {
  const s = clearEnemies(createGame());
  s.quest = 1; s.ferry = true;
  const lantern = LANTERNS[0];
  for (const h of s.heroes) place(h, lantern.x, lantern.y + 1);
  step(s, { ...idle, interact: true });
  assert.deepEqual(s.lit, []);
  assert.match(s.log.at(-1).text, /Only Oswin/);
  step(s, { ...idle, switchTo: 1, interact: true });
  assert.deepEqual(s.lit, [lantern.id]);
  assert.equal(s.enemies.length, 2);
});

test("all three lanterns open the chapel and the boss appears inside", () => {
  const s = clearEnemies(createGame());
  s.quest = 1; s.ferry = true; s.active = 1;
  for (const l of LANTERNS) {
    for (const h of s.heroes) place(h, l.x, l.y + 1);
    step(s, { ...idle, interact: true });
  }
  assert.equal(s.gate, true);
  assert.equal(s.quest, 2);
  clearEnemies(s);
  for (const h of s.heroes) place(h, 44, 10);
  step(s);
  assert.ok(s.enemies.some((e) => e.type === "eater"));
});

test("defeating the Lantern-Eater wins the game", () => {
  const s = clearEnemies(createGame());
  s.gate = true; s.bossSpawned = true;
  for (const h of s.heroes) place(h, 50, 10);
  s.enemies.push({ id: "boss", type: "eater", ...centre(51, 10), hp: 1, maxHp: ENEMIES.eater.hp, cd: 9, markedFor: 0, alive: true });
  step(s, { ...idle, attack: true });
  assert.equal(s.won, true);
  assert.equal(s.quest, 3);
});

test("walls and water block movement; reeds slow it", () => {
  const s = clearEnemies(createGame());
  const bran = s.heroes[0];
  place(bran, 18, 5);
  step(s, { move: { x: 1, y: 0 } }, 120);
  assert.ok(bran.x < 19 * TILE, "should stop at the river");
  const fast = clearEnemies(createGame());
  const slow = clearEnemies(createGame());
  place(fast.heroes[0], 3, 10); place(slow.heroes[0], 11, 0 + 1);
  // Find a reed tile to start on for the slow hero.
  const reed = slow.map.findIndex((row) => row.includes(","));
  place(slow.heroes[0], slow.map[reed].indexOf(","), reed);
  const fx = fast.heroes[0].x, sx = slow.heroes[0].x;
  step(fast, { move: { x: 0, y: 1 } }, 1); step(slow, { move: { x: 0, y: 1 } }, 1);
  assert.ok(Math.abs(slow.heroes[0].y - centre(0, reed).y) < Math.abs(fast.heroes[0].y - centre(0, 10).y));
  assert.equal(fast.heroes[0].x, fx); assert.equal(slow.heroes[0].x, sx);
});

test("attacks respect cooldowns and Kettle's mark adds damage", () => {
  const s = clearEnemies(createGame());
  const bran = s.heroes[0];
  for (const h of s.heroes.slice(1)) place(h, 3, 3);   // keep companions out of the fight
  place(bran, 10, 10);
  const foe = { id: "x", type: "shambler", ...centre(11, 10), hp: 200, maxHp: 200, cd: 99, markedFor: 0, alive: true };
  s.enemies.push(foe);
  step(s, { ...idle, attack: true }, 2);
  assert.equal(foe.hp, 200 - HEROES[0].attack.damage);          // second press is still on cooldown
  foe.markedFor = 5;
  step(s, idle, 40);
  step(s, { ...idle, attack: true });
  assert.equal(foe.hp, 200 - (1 + MARK_BONUS) * HEROES[0].attack.damage);
});

test("the healer's bargain restores nearby allies but not past full", () => {
  const s = clearEnemies(createGame());
  s.active = 2;
  for (const h of s.heroes) { place(h, 10, 10); h.hp = 20; }
  step(s, { ...idle, special: true });
  for (const [i, h] of s.heroes.entries()) assert.equal(h.hp, Math.min(HEROES[i].hp, 20 + HEROES[2].special.amount));
  step(s, { ...idle, special: true });
  assert.equal(s.heroes[0].hp, 20 + HEROES[2].special.amount, "special is on cooldown");
});

test("downed heroes are revived by a friend standing beside them; a full wipe ends the game", () => {
  const s = clearEnemies(createGame());
  for (const h of s.heroes) place(h, 10, 10);
  s.heroes[3].hp = 0; s.heroes[3].downed = true;
  step(s, idle, Math.ceil(2.6 * 60));
  assert.equal(s.heroes[3].downed, false);
  // Back at 30 %, and the healer's AI may top them up straight away.
  assert.ok(s.heroes[3].hp >= Math.round(HEROES[3].hp * 0.3));
  const t = clearEnemies(createGame());
  for (const h of t.heroes) { h.hp = 1; place(h, 10, 10); }
  t.enemies.push({ id: "w", type: "shambler", ...centre(10, 10), hp: 999, maxHp: 999, cd: 0, markedFor: 0, alive: true });
  for (let i = 0; i < 4; i++) { t.enemies.push({ ...t.enemies[0], id: `w${i}`, cd: 0 }); }
  step(t, idle, 600);
  assert.equal(t.over, true);
});

test("save and load round-trip, and foreign saves are refused", () => {
  const s = step(createGame(7), { move: { x: 1, y: 0 } }, 30);
  const loaded = deserialise(serialise(s));
  assert.equal(loaded.heroes[0].x, s.heroes[0].x);
  assert.equal(loaded.quest, s.quest);
  assert.throws(() => deserialise(JSON.stringify({ v: 99 })));
});

test("the same seed and inputs give the same game", () => {
  const run = () => step(createGame(3), { move: { x: 1, y: 0.2 }, attack: true }, 400);
  const a = run(), b = run();
  assert.deepEqual(a.heroes.map((h) => [h.x, h.y, h.hp]), b.heroes.map((h) => [h.x, h.y, h.hp]));
  assert.deepEqual(a.enemies.map((e) => [e.x, e.y, e.hp]), b.enemies.map((e) => [e.x, e.y, e.hp]));
});

test("a scripted playthrough finishes the quest chain", () => {
  const s = createGame(5);
  // Walk to the ferrywoman, fighting whatever comes, then follow the quest steps.
  const goTo = (tx, ty, max = 3000) => {
    const goal = centre(tx, ty);
    for (let i = 0; i < max && !s.over; i++) {
      const me = s.heroes[s.active];
      const dx = goal.x - me.x, dy = goal.y - me.y;
      if (Math.hypot(dx, dy) < 24) return true;
      update(s, { move: { x: dx, y: dy }, attack: true, special: true }, 1 / 60);
    }
    return false;
  };
  assert.ok(goTo(NPCS[0].x, NPCS[0].y + 1), "reach the ferry");
  update(s, { ...idle, interact: true }, 1 / 60);
  assert.equal(s.quest, 1);
  update(s, { ...idle, switchTo: 1 }, 1 / 60);
  for (const l of LANTERNS) {
    assert.ok(goTo(l.x, l.y + 1), `reach lantern ${l.id}`);
    update(s, { ...idle, switchTo: 1, interact: true }, 1 / 60);
  }
  assert.equal(s.gate, true, "gate opens");
  assert.ok(goTo(46, 10), "enter the chapel");
  for (let i = 0; i < 20000 && !s.won && !s.over; i++) {
    const boss = s.enemies.find((e) => e.type === "eater");
    const me = s.heroes[s.active];
    const goal = boss ?? me;
    update(s, { move: { x: goal.x - me.x, y: goal.y - me.y }, attack: true, special: true,
                switchTo: s.heroes.findIndex((h) => !h.downed) }, 1 / 60);
  }
  assert.ok(s.won || s.over, "the fight resolves");
  assert.ok(s.log.some((l) => /Lantern-Eater|chapel/.test(l.text)));
});

test("the boss warns before its area attack, and stepping out of the ring avoids it", () => {
  const s = clearEnemies(createGame());
  s.gate = true; s.bossSpawned = true;
  const slam = ENEMIES.eater.slam;
  const boss = { id: "boss", type: "eater", ...centre(52, 10), hp: 9999, maxHp: 9999, cd: 999, markedFor: 0, alive: true };
  s.enemies.push(boss);
  place(s.heroes[0], 52, 12);                       // inside the ring (64 px away)
  for (const h of s.heroes.slice(1)) { place(h, 47, 10); h.hp = h.maxHp; }   // outside (160 px)
  const before = s.heroes.map((h) => h.hp);
  step(s, idle, Math.ceil((slam.every - slam.warning) * 60) + 2);
  assert.ok(s.effects.some((fx) => fx.warn), "a warning ring appears first");
  assert.match(s.log.map((l) => l.text).join(" "), /step out of the ring/);
  assert.equal(s.heroes[0].hp, before[0], "no damage during the warning");
  step(s, idle, Math.ceil(slam.warning * 60) + 2);
  assert.ok(s.heroes[0].hp <= before[0] - slam.damage + 1, "the hero inside is hit");
});
