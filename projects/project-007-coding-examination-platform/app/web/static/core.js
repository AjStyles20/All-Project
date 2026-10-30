// Shared helpers for the P001 UI (no framework; TECHNOLOGY_PLATFORM_SELECTION §5–6).
//
// Safety rule: every value from the API is written with textContent via el(), never as HTML.

const main = document.getElementById("main");
const notice = document.getElementById("notice");
export const TOKEN_KEY = "p001.token";

// ---------- small helpers ----------

export function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value === undefined || value === null || value === false) continue;
    if (key === "text") node.textContent = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value === true ? "" : value);
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined || child === false) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

export function show(...nodes) {
  main.replaceChildren(...nodes);
  main.focus();
}

export function say(message, kind = "info") {
  notice.textContent = message;
  notice.dataset.kind = kind;
  notice.hidden = !message;
}

export function when(iso) {
  // The API sends naive UTC timestamps; show them in the viewer's local time.
  if (!iso) return "—";
  const date = new Date(iso.endsWith("Z") || iso.includes("+") ? iso : iso + "Z");
  return date.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
}

export class ApiError extends Error {
  constructor(status, detail) {
    super(typeof detail === "string" ? detail : `Request failed (${status}).`);
    this.status = status;
  }
}

export async function api(method, path, body) {
  const headers = { "Accept": "application/json" };
  const token = sessionStorage.getItem(TOKEN_KEY);
  if (token) headers["Authorization"] = "Bearer " + token;
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const response = await fetch(path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
  if (response.status === 401 && path !== "/auth/login") {
    sessionStorage.removeItem(TOKEN_KEY);
    account = null;
    location.hash = "#/login";
    throw new ApiError(401, "Your session has ended. Please sign in again.");
  }
  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok) throw new ApiError(response.status, data && data.detail);
  return data;
}

let account = null;

export async function ensureAccount() {
  // Loaded once per page for every signed-in route, so deep links also show "Sign out".
  if (!account) account = await api("GET", "/auth/me");
  document.getElementById("account").hidden = false;
  document.getElementById("who").textContent = `${account.username} (${account.roles.join(", ")})`;
  return account;
}

export function forgetAccount() {
  account = null;
}

export function words(code) {
  // "INTERNAL_ONLY" -> "internal only": readable labels for contract enum values.
  return code.replace(/_/g, " ").toLowerCase();
}

export function capabilityText(value) {
  if (typeof value === "string") return words(value);
  const detail = value.allowlist || value.sources || value.limits;
  return `${words(value.value)}: ${Array.isArray(detail) ? detail.join(", ") : detail}`;
}

