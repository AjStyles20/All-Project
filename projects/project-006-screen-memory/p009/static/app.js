// Screen Memory dashboard. The token arrives in the URL fragment and is sent as a header;
// everything shown goes through textContent.
const token = new URLSearchParams(location.hash.slice(1)).get("token") || "";
history.replaceState(null, "", location.pathname);  // keep the token out of the address bar
const $ = (id) => document.getElementById(id);
let shownUrl = null;
let shownId = null;

function notice(text, kind = "error") {
  $("notice").replaceChildren();
  if (text) {
    const p = document.createElement("p");
    p.className = kind;
    p.textContent = text;
    $("notice").append(p);
  }
}

async function api(method, path, body) {
  const response = await fetch(path, {
    method,
    headers: { "X-Token": token, ...(body ? { "Content-Type": "application/json" } : {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(typeof data.detail === "string" ? data.detail : `Request failed (${response.status})`);
  }
  return response;
}

const when = (seconds) => new Date(seconds * 1000).toLocaleString();

async function refreshStatus() {
  const s = await (await api("GET", "/api/status")).json();
  $("state").textContent = s.recorder === "recording" ? "● Recording" : `○ ${s.recorder[0].toUpperCase()}${s.recorder.slice(1)}`;
  $("state").className = "state " + s.recorder.replaceAll(" ", "-");
  const skipped = s.skipped.excluded || 0;
  $("stats").textContent = `${s.frames} images, ${(s.bytes / 1e6).toFixed(1)} MB. ` +
    `Kept for ${s.retention_days} days, up to ${(s.max_bytes / 1e9).toFixed(0)} GB. ` +
    `Private windows skipped: ${skipped} times.`;
}

async function search(event) {
  event?.preventDefault();
  const rows = await (await api("GET", `/api/frames?q=${encodeURIComponent($("q").value)}`)).json();
  const items = rows.map((r) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "link";
    button.textContent = `${when(r.captured_at)} — ${r.title || r.app}`;
    button.addEventListener("click", () => show(r));
    const meta = document.createElement("span");
    meta.className = "meta";
    meta.textContent = ` ${r.app}${r.departure ? " · last view before you switched away" : ""}`;
    li.append(button, meta);
    return li;
  });
  if (!items.length) {
    const li = document.createElement("li");
    li.className = "meta";
    li.textContent = "Nothing found.";
    items.push(li);
  }
  $("results").replaceChildren(...items);
}

async function show(row) {
  const blob = await (await api("GET", `/api/frames/${row.frame_id}/image`)).blob();
  if (shownUrl) URL.revokeObjectURL(shownUrl);
  shownUrl = URL.createObjectURL(blob);
  shownId = row.frame_id;
  $("viewer-img").src = shownUrl;
  $("viewer-img").alt = `Screenshot of ${row.title || row.app}`;
  $("viewer-caption").textContent = `${when(row.captured_at)} — ${row.app} — ${row.title}`;
  $("viewer").hidden = false;
  $("viewer").scrollIntoView();
}

function action(fn) {
  return async () => {
    try { await fn(); notice(""); await refreshStatus(); } catch (error) { notice(error.message); }
  };
}

$("pause").addEventListener("click", action(() => api("POST", "/api/pause")));
$("resume").addEventListener("click", action(() => api("POST", "/api/resume")));
$("del15").addEventListener("click", action(async () => {
  const n = (await (await api("POST", "/api/delete-recent", { minutes: 15 })).json()).deleted;
  notice(`Deleted ${n} images.`, "ok"); await search();
}));
$("del60").addEventListener("click", action(async () => {
  const n = (await (await api("POST", "/api/delete-recent", { minutes: 60 })).json()).deleted;
  notice(`Deleted ${n} images.`, "ok"); await search();
}));
$("delall").addEventListener("click", action(async () => {
  const typed = prompt("This deletes every image and record. Type DELETE to confirm.");
  if (typed !== "DELETE") return;
  const n = (await (await api("POST", "/api/delete-all", { confirm: typed })).json()).deleted;
  $("viewer").hidden = true;
  notice(`Deleted ${n} images.`, "ok"); await search();
}));
$("viewer-delete").addEventListener("click", action(async () => {
  if (!shownId) return;
  await api("DELETE", `/api/frames/${shownId}`);
  $("viewer").hidden = true;
  await search();
}));
$("search").addEventListener("submit", (e) => search(e).catch((error) => notice(error.message)));

if (!token) {
  notice("Open the dashboard with the link printed when the program started.");
} else {
  refreshStatus().then(() => search()).catch((error) => notice(error.message));
  setInterval(() => refreshStatus().catch(() => {}), 5000);
}
