// Canvas drawing. Reads the game state; never changes it.
// Shapes tell enemy types apart (not only colour): square shambler, diamond wisp, octagon boss.
import { ENEMIES, HEROES, LANTERNS, NPCS, TILE } from "./data.js";

const TILE_COLOURS = { ".": "#4d6b45", ",": "#5f7d3f", "~": "#24465a", "#": "#57524b", "=": "#7a5a3a", "|": "#3d3a4f" };

export function draw(ctx, state, view) {
  const { width, height } = ctx.canvas;
  const leader = state.heroes[state.active];
  const camX = Math.max(0, Math.min(state.map[0].length * TILE - width, leader.x - width / 2));
  const camY = Math.max(0, Math.min(state.map.length * TILE - height, leader.y - height / 2));
  ctx.save();
  ctx.clearRect(0, 0, width, height);
  ctx.translate(-Math.round(camX), -Math.round(camY));

  const x0 = Math.floor(camX / TILE), y0 = Math.floor(camY / TILE);
  for (let ty = y0; ty <= y0 + Math.ceil(height / TILE) && ty < state.map.length; ty++) {
    for (let tx = x0; tx <= x0 + Math.ceil(width / TILE) && tx < state.map[0].length; tx++) {
      let c = state.map[ty][tx];
      if (c === "=" && !state.ferry) c = "~";
      ctx.fillStyle = c === "|" && state.gate ? TILE_COLOURS["."] : TILE_COLOURS[c];
      ctx.fillRect(tx * TILE, ty * TILE, TILE, TILE);
      if (c === ",") reeds(ctx, tx, ty);
      if (c === "~" && !view.reducedMotion) ripple(ctx, tx, ty, state.time);
      if (c === "=") planks(ctx, tx, ty);
    }
  }

  // Murk: fog over the unlit east, thinning as lanterns are lit.
  const fog = 0.45 - state.lit.length * 0.12;
  if (fog > 0) {
    ctx.fillStyle = `rgba(30, 28, 45, ${fog})`;
    ctx.fillRect(22 * TILE, 0, (state.map[0].length - 22) * TILE, state.map.length * TILE);
  }

  for (const l of LANTERNS) lantern(ctx, l, state.lit.includes(l.id), state.time, view.reducedMotion);
  for (const n of NPCS) person(ctx, n.x * TILE + TILE / 2, n.y * TILE + TILE / 2, "#d8c7a0", "D");
  for (const e of state.enemies) enemy(ctx, e);
  state.heroes.forEach((h, i) => hero(ctx, h, HEROES[i], i === state.active));
  for (const p of state.projectiles) {
    ctx.fillStyle = p.owner === "enemy" ? "#b9a6ff" : p.bomb ? "#ff8a3c" : "#ffe9a8";
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.bomb ? 6 : 4, 0, Math.PI * 2);
    ctx.fill();
  }
  for (const fx of state.effects) effect(ctx, fx);
  ctx.restore();
}

function reeds(ctx, tx, ty) {
  ctx.strokeStyle = "#86a35a";
  ctx.lineWidth = 2;
  for (let i = 0; i < 4; i++) {
    const x = tx * TILE + 6 + i * 7;
    ctx.beginPath();
    ctx.moveTo(x, ty * TILE + TILE - 4);
    ctx.lineTo(x + 2, ty * TILE + 8);
    ctx.stroke();
  }
}

function ripple(ctx, tx, ty, t) {
  ctx.strokeStyle = "rgba(160, 200, 220, 0.25)";
  ctx.lineWidth = 1;
  const off = Math.sin(t * 1.5 + tx * 0.7 + ty) * 4;
  ctx.beginPath();
  ctx.moveTo(tx * TILE + 6, ty * TILE + 16 + off);
  ctx.lineTo(tx * TILE + 26, ty * TILE + 16 + off);
  ctx.stroke();
}

function planks(ctx, tx, ty) {
  ctx.strokeStyle = "#5a4128";
  for (let i = 1; i < 4; i++) {
    ctx.beginPath();
    ctx.moveTo(tx * TILE + i * 8, ty * TILE);
    ctx.lineTo(tx * TILE + i * 8, ty * TILE + TILE);
    ctx.stroke();
  }
}

function lantern(ctx, l, lit, t, still) {
  const x = l.x * TILE + TILE / 2, y = l.y * TILE + TILE / 2;
  ctx.fillStyle = "#2b2b2b";
  ctx.fillRect(x - 3, y - 4, 6, 18);
  if (lit) {
    const glow = still ? 1 : 0.85 + Math.sin(t * 6) * 0.15;
    ctx.fillStyle = `rgba(255, 210, 110, ${0.25 * glow})`;
    ctx.beginPath(); ctx.arc(x, y - 8, 40, 0, Math.PI * 2); ctx.fill();
  }
  ctx.fillStyle = lit ? "#ffd36e" : "#55575a";
  ctx.fillRect(x - 7, y - 16, 14, 12);
}

function person(ctx, x, y, colour, letter) {
  ctx.fillStyle = colour;
  ctx.beginPath(); ctx.arc(x, y, 12, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "#1b1b1b";
  ctx.font = "bold 12px system-ui";
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillText(letter, x, y + 1);
}

function bar(ctx, x, y, w, frac, colour) {
  ctx.fillStyle = "rgba(0,0,0,0.6)";
  ctx.fillRect(x - w / 2, y, w, 4);
  ctx.fillStyle = colour;
  ctx.fillRect(x - w / 2, y, w * Math.max(0, frac), 4);
}

function hero(ctx, h, def, active) {
  if (active) {
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(h.x, h.y, 16, 0, Math.PI * 2); ctx.stroke();
  }
  ctx.globalAlpha = h.downed ? 0.45 : 1;
  person(ctx, h.x, h.y, def.colour, def.name[0]);
  ctx.globalAlpha = 1;
  bar(ctx, h.x, h.y - 22, 26, h.hp / h.maxHp, "#7ee07e");
  if (h.downed) bar(ctx, h.x, h.y + 16, 26, h.revive / 2.5, "#ffffff");
}

function enemy(ctx, e) {
  const def = ENEMIES[e.type];
  const r = def.boss ? 26 : 12;
  ctx.fillStyle = def.colour;
  ctx.beginPath();
  if (def.shape === "square") ctx.rect(e.x - r, e.y - r, r * 2, r * 2);
  else if (def.shape === "diamond") { ctx.moveTo(e.x, e.y - r); ctx.lineTo(e.x + r, e.y); ctx.lineTo(e.x, e.y + r); ctx.lineTo(e.x - r, e.y); }
  else for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2 + Math.PI / 8;
    ctx[i ? "lineTo" : "moveTo"](e.x + Math.cos(a) * r, e.y + Math.sin(a) * r);
  }
  ctx.closePath();
  ctx.fill();
  if (e.markedFor > 0) {
    ctx.strokeStyle = "#ffef7a"; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(e.x, e.y, r + 5, 0, Math.PI * 2); ctx.stroke();
  }
  bar(ctx, e.x, e.y - r - 8, def.boss ? 60 : 24, e.hp / e.maxHp, "#e05a5a");
}

function effect(ctx, fx) {
  if (fx.kind === "number") {
    ctx.fillStyle = fx.hurt ? "#ff9a9a" : "#ffffff";
    ctx.font = "bold 12px system-ui";
    ctx.textAlign = "center";
    ctx.fillText(fx.text, fx.x, fx.y - (0.8 - fx.life) * 20);
  } else {
    ctx.strokeStyle = fx.warn ? "rgba(235, 80, 80, 0.9)" : fx.heal ? "rgba(126, 224, 126, 0.8)" : fx.fire ? "rgba(255, 140, 60, 0.85)" : "rgba(255,255,255,0.7)";
    if (fx.warn) ctx.setLineDash([10, 6]);
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(fx.x, fx.y, fx.r, 0, Math.PI * 2); ctx.stroke();
    ctx.setLineDash([]);
  }
}
