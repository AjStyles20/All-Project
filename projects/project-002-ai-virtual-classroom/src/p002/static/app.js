// Learning World page. Token from the URL fragment, sent as a header; text via textContent only.
const token = new URLSearchParams(location.hash.slice(1)).get("token") || "";
history.replaceState(null, "", location.pathname);
const $ = (id) => document.getElementById(id);

function el(tag, text, cls) {
  const n = document.createElement(tag);
  if (text !== undefined && text !== null) n.textContent = text;
  if (cls) n.className = cls;
  return n;
}

function notice(text) {
  $("notice").replaceChildren(text ? el("p", text, "error") : "");
}

async function api(method, path, body) {
  const r = await fetch(path, { method, headers: { "X-Token": token, ...(body ? { "Content-Type": "application/json" } : {}) },
    body: body ? JSON.stringify(body) : undefined });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(typeof data.detail === "string" ? data.detail : `Request failed (${r.status})`);
  return data;
}

const STATE_WORDS = {
  UNKNOWN: "Not started", ASSISTED_SUCCESS: "Done with help", PROVISIONAL: "Provisional", VERIFYING: "Ready for a check",
  INDEPENDENT: "Shown without help", REOPENED: "Needs another look",
};

function showQuestion(q) {
  const box = $("question");
  if (!q) { box.replaceChildren(el("p", "All three topics are shown without help. Well done.")); return; }
  const parts = [el("p", q.check ? `Check without help: ${q.concept}` : `Practice: ${q.concept}`, "tag")];
  if (q.tables) parts.push(el("pre", q.tables));
  parts.push(el("p", q.prompt, "prompt"));
  const form = el("form");
  const fieldset = el("fieldset");
  fieldset.append(el("legend", "Your answer"));
  q.options.forEach((opt, i) => {
    const id = `opt-${i}`;
    const input = el("input");
    Object.assign(input, { type: "radio", name: "choice", id, value: String(i), required: true });
    const label = el("label", opt);
    label.htmlFor = id;
    const row = el("div", undefined, "option");
    row.append(input, label);
    fieldset.append(row);
  });
  const access = el("input");
  Object.assign(access, { id: "accommodation", maxLength: 60, placeholder: "e.g. screen reader, extra time" });
  const accessLabel = el("label", "Accessibility support used (optional; never counts against you)");
  accessLabel.htmlFor = "accommodation";
  const actions = el("div", undefined, "row");
  const submit = el("button", "Answer");
  submit.type = "submit";
  actions.append(submit);
  if (!q.check && q.help_level < q.max_help) {
    const more = el("button", q.help_level === 0 ? "I'd like a hint" : "More help");
    more.type = "button";
    more.addEventListener("click", async () => {
      try { showQuestion((await api("POST", "/api/hint", { question_id: q.id })).question); } catch (e) { notice(e.message); }
    });
    actions.append(more);
  }
  form.append(fieldset, accessLabel, access, actions);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const choice = Number(new FormData(form).get("choice"));
    try {
      const r = await api("POST", "/api/answer", { question_id: q.id, choice, accommodation: access.value || null });
      $("feedback").replaceChildren(
        el("p", r.correct ? `Correct (help used: L${r.help_level}).` : `Not quite. The answer is ${r.answer}.`, r.correct ? "ok" : "error"),
        el("p", `${STATE_WORDS[r.mastery]}: ${r.reasons.join(" ")}`, "meta"));
      await loadPractice();
    } catch (e) { notice(e.message); }
  });
  if (q.hints.length) {
    const list = el("ol", undefined, "hints");
    q.hints.forEach((h) => list.append(el("li", h)));
    parts.push(el("h3", `Help so far (level ${q.help_level} of ${q.max_help})`), list);
  }
  parts.push(form);
  box.replaceChildren(...parts);
}

async function loadPractice() {
  showQuestion((await api("GET", "/api/practice")).question);
}

async function loadMastery() {
  const data = await api("GET", "/api/mastery");
  $("concepts").replaceChildren(...data.concepts.map((c) => {
    const card = el("article", undefined, "card");
    card.append(el("h3", `${c.label}: ${STATE_WORDS[c.mastery]}`), el("p", c.reasons.join(" ") || "No attempts yet.", "meta"));
    if (c.trail.length) {
      const ul = el("ul");
      c.trail.forEach((t) => ul.append(el("li", `${t.id} ${t.check ? "check" : "practice"}: ${t.correct ? "correct" : "incorrect"}, help ${t.help}${t.accommodation ? `, support: ${t.accommodation}` : ""}`)));
      card.append(ul);
    }
    return card;
  }));
  $("issues").replaceChildren(...data.issues.map((i) => {
    const li = el("li", `${i.concept}: ${i.description} (${i.state})`);
    const next = { OPEN: "WORKING", WORKING: "VERIFYING", VERIFYING: "RESOLVED", RESOLVED: null, REOPENED: "WORKING" }[i.state];
    if (next) {
      const b = el("button", `Mark ${next.toLowerCase()}`);
      b.type = "button";
      b.addEventListener("click", async () => {
        try { await api("POST", `/api/issues/${i.id}/move`, { to: next }); await loadMastery(); } catch (e) { notice(e.message); }
      });
      li.append(" ", b);
    }
    return li;
  }));
}

async function loadCourse() {
  const data = await api("GET", "/api/course");
  $("artifacts").replaceChildren(...data.artifacts.map((a) => {
    const li = el("li", `${a.kind} "${a.content}": `);
    li.append(el("strong", a.status, `status ${a.status.toLowerCase()}`));
    if (a.reasons.length) li.append(el("div", a.reasons.join("; "), "meta"));
    return li;
  }));
  $("claims").replaceChildren(...data.claims.map((c) => {
    const li = el("li");
    li.append(el("span", c.text), " ", el("strong", c.status, `status ${c.status.toLowerCase()}`));
    const why = el("details");
    why.append(el("summary", "Why?"), el("p", `Authority: ${c.authority}. Made by ${c.created_by}.`),
      el("p", c.reasons.join("; ")), el("p", `Path: ${c.path.join(" ← ")}`, "meta"));
    li.append(why);
    return li;
  }));
  $("sources").replaceChildren(...data.sources.map((s) => {
    const li = el("li", `${s.id} ${s.title} ${s.version} (${s.authority})${s.superseded_by ? `, replaced by ${s.superseded_by}` : ""}`);
    const d = el("details");
    d.append(el("summary", "Show text"), el("pre", s.text));
    li.append(d);
    return li;
  }));
}

document.querySelectorAll("nav button").forEach((b) => b.addEventListener("click", async () => {
  document.querySelectorAll("nav button").forEach((o) => o.setAttribute("aria-pressed", String(o === b)));
  for (const id of ["practice", "mastery", "course"]) $(id).hidden = id !== b.dataset.tab;
  try {
    if (b.dataset.tab === "mastery") await loadMastery();
    if (b.dataset.tab === "course") await loadCourse();
    if (b.dataset.tab === "practice") await loadPractice();
  } catch (e) { notice(e.message); }
}));

$("issue-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await api("POST", "/api/issues", { concept: $("issue-concept").value, description: $("issue-text").value });
    $("issue-text").value = "";
    await loadMastery();
  } catch (e) { notice(e.message); }
});

if (!token) notice("Open this page with the link printed when the program started.");
else loadPractice().catch((e) => notice(e.message));
