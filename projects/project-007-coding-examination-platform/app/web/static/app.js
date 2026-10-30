// P001 web UI: sign-in and routing. Plain JavaScript over the existing JSON API; business
// rules stay on the server (DR-017). Screens live in candidate.js, examiner.js and admin.js.
import { adminExamView, adminHome } from "./admin.js";
import { clearLeaveGuard, examsView, researchView, resultView, rulesView, sessionView } from "./candidate.js";
import { TOKEN_KEY, api, el, ensureAccount, forgetAccount, say, show } from "./core.js";
import { contractView, examView, examinerHome, reviewView, sessionsView } from "./examiner.js";

// Each role's home screen; Administrator also passes the API's examiner role check.
const AREAS = [
  { role: "CANDIDATE", hash: "#/exams", text: "My examinations" },
  { role: "EXAMINER", also: "ADMINISTRATOR", hash: "#/examiner", text: "Examiner" },
  { role: "ADMINISTRATOR", hash: "#/admin", text: "Research admin" },
];

const areasFor = (me) => AREAS.filter((a) => me.roles.includes(a.role) || me.roles.includes(a.also));

function loginView() {
  document.getElementById("account").hidden = true;
  const username = el("input", { id: "username", type: "text", autocomplete: "username", required: true });
  const password = el("input", { id: "password", type: "password", autocomplete: "current-password", required: true });
  const submit = el("button", { type: "submit", class: "primary", text: "Sign in" });
  const form = el("form", {
    class: "card",
    onsubmit: async (event) => {
      event.preventDefault();
      submit.disabled = true;
      try {
        const result = await api("POST", "/auth/login", { username: username.value, password: password.value });
        sessionStorage.setItem(TOKEN_KEY, result.access_token);
        location.hash = "#/home";
      } catch (error) {
        say(error.message, "error");
      } finally {
        submit.disabled = false;
      }
    },
  },
    el("h2", { text: "Sign in" }),
    el("label", { for: "username", text: "Username" }), username,
    el("label", { for: "password", text: "Password" }), password,
    el("div", { class: "actions" }, submit),
  );
  show(form);
  username.focus();
}

const ROUTES = [
  [/^#\/exams$/, examsView],
  [/^#\/exam\/([^/]+)\/rules$/, rulesView],
  [/^#\/exam\/([^/]+)\/research$/, researchView],
  [/^#\/exam\/([^/]+)\/result$/, resultView],
  [/^#\/session\/([^/]+)$/, sessionView],
  [/^#\/examiner$/, examinerHome],
  [/^#\/examiner\/exam\/([^/]+)$/, examView],
  [/^#\/examiner\/exam\/([^/]+)\/contract$/, contractView],
  [/^#\/examiner\/exam\/([^/]+)\/sessions$/, sessionsView],
  [/^#\/examiner\/session\/([^/]+)$/, reviewView],
  [/^#\/admin$/, adminHome],
  [/^#\/admin\/exam\/([^/]+)$/, adminExamView],
];

async function route() {
  clearLeaveGuard();
  const hash = location.hash || "#/home";
  // A notice belongs to the screen it was shown on, not the next one.
  if (hash !== "#/login" || sessionStorage.getItem(TOKEN_KEY)) say("");
  if (!sessionStorage.getItem(TOKEN_KEY)) {
    if (hash !== "#/login") location.hash = "#/login"; else loginView();
    return;
  }
  if (hash === "#/login") { loginView(); return; }
  try {
    const me = await ensureAccount();
    const areas = areasFor(me);
    document.getElementById("areas").replaceChildren(...areas.map((a) => el("a", { href: a.hash, text: a.text })));
    if (hash === "#/home") {
      location.hash = areas.length ? areas[0].hash : "#/none";
      return;
    }
    for (const [pattern, view] of ROUTES) {
      const match = hash.match(pattern);
      if (match) { await view(...match.slice(1).map(decodeURIComponent)); return; }
    }
    show(el("section", { class: "card" }, el("h2", { text: "Nothing here" }),
      el("p", { text: areas.length ? "That page does not exist." : "Your account has no screens in this interface yet." })));
  } catch (error) {
    say(error.message, "error");
  }
}

document.getElementById("logout").addEventListener("click", async () => {
  try { await api("POST", "/auth/logout"); } catch { /* already signed out */ }
  sessionStorage.removeItem(TOKEN_KEY);
  forgetAccount();
  location.hash = "#/login";
  say("You are signed out.");
});
window.addEventListener("hashchange", route);
route();
