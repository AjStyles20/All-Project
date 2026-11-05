// Chess page. Seat tokens live in the URL fragment, which browsers never send to the server.
// All text goes through textContent.
const $ = (id) => document.getElementById(id);
const GLYPH = { K: "♔", Q: "♕", R: "♖", B: "♗", N: "♘", P: "♙", k: "♚", q: "♛", r: "♜", b: "♝", n: "♞", p: "♟" };
const NAMES = { k: "king", q: "queen", r: "rook", b: "bishop", n: "knight", p: "pawn" };
const FILES = "abcdefgh";

const params = new URLSearchParams(location.hash.slice(1));
const gameId = params.get("game");
const token = params.get("seat");
let state = null;
let selected = null;
let lastMessage = 0;

function notice(text) {
  $("notice").replaceChildren();
  if (text) { const p = document.createElement("p"); p.className = "error"; p.textContent = text; $("notice").append(p); }
}

async function api(method, path, body) {
  const response = await fetch(path, {
    method, headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join("; ") : data.detail || `Request failed (${response.status})`);
  }
  return data;
}

function seatColour() {
  if (!token) return null;
  return params.get("colour");
}

function parseBoard(fen) {
  const squares = {};
  fen.split(" ")[0].split("/").forEach((row, i) => {
    let f = 0;
    for (const c of row) {
      if (/\d/.test(c)) f += Number(c);
      else { squares[FILES[f] + (8 - i)] = c; f += 1; }
    }
  });
  return squares;
}

function drawBoard() {
  const squares = parseBoard(state.fen);
  const flip = seatColour() === "black";
  const cells = [];
  for (let r = 0; r < 8; r++) {
    for (let f = 0; f < 8; f++) {
      const file = flip ? 7 - f : f;
      const rank = flip ? r + 1 : 8 - r;
      const sq = FILES[file] + rank;
      const piece = squares[sq];
      const cell = document.createElement("button");
      cell.type = "button";
      cell.className = "sq " + ((file + rank) % 2 ? "light" : "dark") + (selected === sq ? " selected" : "");
      cell.textContent = piece ? GLYPH[piece] : "";
      cell.setAttribute("aria-label", piece ? `${sq} ${piece === piece.toUpperCase() ? "white" : "black"} ${NAMES[piece.toLowerCase()]}` : `${sq} empty`);
      cell.addEventListener("click", () => clickSquare(sq));
      cells.push(cell);
    }
  }
  $("board").replaceChildren(...cells);
}

async function play(uci) {
  try {
    state = await api("POST", `/api/games/${gameId}/move`, { token, uci });
    notice("");
    render();
  } catch (error) { notice(error.message); }
}

function clickSquare(sq) {
  if (!token || !state || state.result) return;
  if (selected && selected !== sq) {
    let uci = selected + sq;
    if (!state.legal.includes(uci) && state.legal.includes(uci + "q")) uci += $("promotion").value;
    selected = null;
    if (state.legal.includes(uci)) play(uci); else { notice(`${uci} is not legal here.`); drawBoard(); }
    return;
  }
  selected = selected === sq ? null : sq;
  drawBoard();
}

function addMessages(messages) {
  for (const m of messages) {
    const li = document.createElement("li");
    const who = document.createElement("strong");
    who.textContent = `${m.author}${m.role === "SPECTATOR" ? " (spectator)" : ""}: `;
    const text = document.createElement("span");
    text.textContent = m.text;
    li.append(who, text);
    if (m.ruling !== "NO VIOLATION") {
      const note = document.createElement("div");
      note.className = "arbiter";
      note.textContent = `Arbiter: ${m.ruling}. ${m.evidence.join("; ")}.`;
      li.append(note);
    }
    $("messages").append(li);
    lastMessage = Math.max(lastMessage, m.n);
  }
}

function render() {
  drawBoard();
  const you = seatColour() ? `You play ${seatColour()}. ` : "You are watching. ";
  const turn = state.result ? `Game over: ${state.result} (${state.reason}).` : `${state.turn[0].toUpperCase() + state.turn.slice(1)} to move${state.in_check ? ", in check" : ""}.`;
  $("status").textContent = `${you}${turn} Rules: ${state.contract.toLowerCase()}.`;
  $("moves").textContent = state.moves.length ? state.moves.map((m, i) => (i % 2 ? m : `${i / 2 + 1}. ${m}`)).join(" ") : "No moves yet.";
  $("resign").hidden = !token || !!state.result;
}

async function poll() {
  try {
    const next = await api("GET", `/api/games/${gameId}?since=${lastMessage}`);
    const changed = !state || next.fen !== state.fen || next.result !== state.result;
    state = next;
    addMessages(next.messages);
    if (changed) render();
  } catch (error) { notice(error.message); }
}

function link(label, hash) {
  const p = document.createElement("p");
  const strong = document.createElement("strong");
  strong.textContent = label + ": ";
  const a = document.createElement("a");
  a.href = `${location.pathname}#${hash}`;
  a.textContent = `${location.origin}${location.pathname}#${hash}`;
  p.append(strong, a);
  return p;
}

$("new-game").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const g = await api("POST", "/api/games", { contract: $("contract").value });
    $("links").replaceChildren(
      link("White (keep private)", `game=${g.game_id}&seat=${g.white_token}&colour=white`),
      link("Black (send to your opponent)", `game=${g.game_id}&seat=${g.black_token}&colour=black`),
      link("Spectators", `game=${g.game_id}`),
    );
  } catch (error) { notice(error.message); }
});

$("move-form").addEventListener("submit", (event) => {
  event.preventDefault();
  play($("move-text").value.trim().toLowerCase());
  $("move-text").value = "";
});

$("resign").addEventListener("click", async () => {
  if (!confirm("Resign this game?")) return;
  try { state = await api("POST", `/api/games/${gameId}/resign`, { token }); render(); } catch (error) { notice(error.message); }
});

$("chat-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await api("POST", `/api/games/${gameId}/chat`, { token, name: $("chat-name").value || "spectator", text: $("chat-text").value });
    $("chat-text").value = "";
    await poll();
  } catch (error) { notice(error.message); }
});

window.addEventListener("hashchange", () => location.reload());

if (gameId) {
  $("start").hidden = true;
  $("game").hidden = false;
  $("chat-name").hidden = !!token;
  poll();
  setInterval(poll, 1500);
}
