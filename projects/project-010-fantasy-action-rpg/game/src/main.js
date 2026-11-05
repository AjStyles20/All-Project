// Browser layer: keyboard, fixed-step loop, party panel, story log, save and load.
import { HEROES, QUEST, createGame, deserialise, serialise, update } from "./engine.js";
import { draw } from "./render.js";

const SAVE_KEY = "brinewold.save.v1";
const STEP = 1 / 60;
const canvas = document.getElementById("view");
const ctx = canvas.getContext("2d");
const $ = (id) => document.getElementById(id);
const view = { reducedMotion: matchMedia("(prefers-reduced-motion: reduce)").matches };

let state = createGame(Date.now() % 100000);
let paused = true;
let shownLog = 0;
const held = new Set();
const pressed = new Set();

function storage(fn) {
  try { return fn(window.localStorage); } catch { return null; }
}

function input() {
  const x = (held.has("ArrowRight") || held.has("d") ? 1 : 0) - (held.has("ArrowLeft") || held.has("a") ? 1 : 0);
  const y = (held.has("ArrowDown") || held.has("s") ? 1 : 0) - (held.has("ArrowUp") || held.has("w") ? 1 : 0);
  let switchTo = null;
  for (const k of ["1", "2", "3", "4"]) if (pressed.has(k)) switchTo = Number(k) - 1;
  if (pressed.has("Tab")) {
    for (let i = 1; i <= 4; i++) {
      const next = (state.active + i) % 4;
      if (!state.heroes[next].downed) { switchTo = next; break; }
    }
  }
  return { move: { x, y }, attack: held.has(" ") || held.has("j"), special: pressed.has("k") || pressed.has("Shift"),
           interact: pressed.has("e"), switchTo, paused };
}

function setPaused(value) {
  paused = value;
  $("pause-panel").hidden = !paused || state.over || state.won;
  $("pause-button").textContent = paused ? "Resume" : "Pause";
}

function renderPanel() {
  $("party").replaceChildren(...state.heroes.map((h, i) => {
    const def = HEROES[i];
    const li = document.createElement("li");
    li.className = i === state.active ? "active" : "";
    const ready = h.specialCd === 0 ? "ready" : `${Math.ceil(h.specialCd)} s`;
    li.textContent = `${def.key}. ${def.name}, ${def.role}: ${Math.ceil(h.hp)}/${h.maxHp}` +
      `${h.downed ? " (down)" : ""} · ${def.special.name} ${ready}${i === state.active ? " · you" : ""}`;
    return li;
  }));
  $("goal").textContent = QUEST[state.quest].text;
  for (; shownLog < state.log.length; shownLog++) {
    const entry = state.log[shownLog];
    const li = document.createElement("li");
    if (entry.who) {
      const who = document.createElement("strong");
      who.textContent = `${entry.who}: `;
      li.append(who);
    }
    li.append(entry.text);
    $("log").prepend(li);
  }
  while ($("log").children.length > 30) $("log").lastChild.remove();
  if ((state.over || state.won) && $("end-panel").hidden) {
    $("end-title").textContent = state.won ? "The lights of Brinewold burn again." : "The Murk has taken the party.";
    $("end-panel").hidden = false;
    storage((s) => s.removeItem(SAVE_KEY));
  }
}

let last = performance.now();
let acc = 0;
let lastQuest = state.quest;
function frame(now) {
  acc += Math.min(0.25, (now - last) / 1000);
  last = now;
  while (acc >= STEP) {
    update(state, input(), STEP);
    pressed.clear();
    acc -= STEP;
  }
  if (state.quest !== lastQuest) {
    lastQuest = state.quest;
    storage((s) => s.setItem(SAVE_KEY, serialise(state)));     // autosave at each story step
  }
  draw(ctx, state, view);
  renderPanel();
  requestAnimationFrame(frame);
}

const GAME_KEYS = new Set(["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " ", "Tab", "Shift", "w", "a", "s", "d", "j", "k", "e", "1", "2", "3", "4"]);
addEventListener("keydown", (ev) => {
  if (ev.target.closest && ev.target.closest("button, input, a")) return;
  const key = ev.key.length === 1 ? ev.key.toLowerCase() : ev.key;
  if (key === "Escape" || key === "p") { setPaused(!paused); ev.preventDefault(); return; }
  if (!GAME_KEYS.has(key) || paused) return;
  ev.preventDefault();
  if (!held.has(key)) pressed.add(key);
  held.add(key);
});
addEventListener("keyup", (ev) => held.delete(ev.key.length === 1 ? ev.key.toLowerCase() : ev.key));
addEventListener("blur", () => { held.clear(); if (!state.over && !state.won) setPaused(true); });

$("start").addEventListener("click", () => { $("title-panel").hidden = true; setPaused(false); canvas.focus(); });
$("pause-button").addEventListener("click", () => setPaused(!paused));
$("resume").addEventListener("click", () => { setPaused(false); canvas.focus(); });
$("save").addEventListener("click", () => {
  const ok = storage((s) => { s.setItem(SAVE_KEY, serialise(state)); return true; });
  $("save-status").textContent = ok ? "Saved." : "Saving is not available in this browser.";
});
$("load").addEventListener("click", () => {
  const text = storage((s) => s.getItem(SAVE_KEY));
  if (!text) { $("save-status").textContent = "No saved game found."; return; }
  try { state = deserialise(text); shownLog = 0; $("log").replaceChildren(); lastQuest = state.quest;
        $("save-status").textContent = "Loaded."; } catch { $("save-status").textContent = "That save could not be read."; }
});
$("restart").addEventListener("click", () => {
  state = createGame(Date.now() % 100000); shownLog = 0; lastQuest = 0;
  $("log").replaceChildren(); $("end-panel").hidden = true; setPaused(false); canvas.focus();
});
$("has-save").hidden = !storage((s) => s.getItem(SAVE_KEY));

requestAnimationFrame(frame);
