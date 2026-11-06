// StartupMatch page. All text goes through textContent; every write sends X-Requested-With.
const $ = (id) => document.getElementById(id);
let vocab = { sectors: [], stages: [], disclaimer: "" };

function el(tag, text, cls) {
  const n = document.createElement(tag);
  if (text !== undefined && text !== null) n.textContent = text;
  if (cls) n.className = cls;
  return n;
}

function notice(text, kind = "error") { $("notice").replaceChildren(text ? el("p", text, kind) : ""); }

async function api(method, path, body) {
  const r = await fetch(path, { method, credentials: "same-origin",
    headers: { "X-Requested-With": "fetch", ...(body ? { "Content-Type": "application/json" } : {}) },
    body: body ? JSON.stringify(body) : undefined });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw Object.assign(new Error(typeof data.detail === "string" ? data.detail : Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join("; ") : `Request failed (${r.status})`), { status: r.status });
  return data;
}

function options(select, values, blank = "Not given") {
  select.replaceChildren(el("option", blank), ...values.map((v) => { const o = el("option", v); o.value = v; return o; }));
  select.firstChild.value = "";
}

function checks(box, name, values) {
  box.replaceChildren(...values.map((v) => {
    const label = el("label");
    const input = el("input");
    Object.assign(input, { type: "checkbox", name, value: v });
    label.append(input, ` ${v}`);
    return label;
  }));
}

const num = (v) => (v === "" || v == null ? null : Number(v));
const money = (v) => (v == null ? "?" : Number(v).toLocaleString());

function componentList(components) {
  const ul = el("ul", undefined, "components");
  for (const c of components) {
    const mark = c.score === null ? "unknown" : c.score >= 1 ? "fits" : c.score > 0 ? "partly" : "does not fit";
    const li = el("li");
    li.append(el("strong", `${c.name}: ${mark}. `), c.reason);
    ul.append(li);
  }
  return ul;
}

async function loadFounder(profile) {
  $("s-name").value = profile.name || ""; $("s-line").value = profile.one_liner || "";
  $("s-sector").value = profile.sector || ""; $("s-stage").value = profile.stage || "";
  $("s-country").value = profile.country || ""; $("s-raising").value = profile.raising ?? "";
  $("s-contact").value = profile.contact || ""; $("s-listed").checked = !!profile.listed;
  const data = await api("GET", "/api/matches");
  $("f-disclaimer").textContent = data.disclaimer;
  $("matches").replaceChildren(...data.matches.map((m) => {
    const li = el("li", undefined, "card");
    li.append(el("h3", `${m.name} — ${m.score === null ? "not enough information" : `fit ${Math.round(m.score * 100)} %`} (confidence: ${m.confidence})`));
    li.append(componentList(m.components));
    for (const w of m.warnings) li.append(el("p", `⚠ ${w}`, "warn"));
    if (m.deals.length) {
      const d = el("details");
      d.append(el("summary", `Recorded deals (${m.deals.length})`));
      const ul = el("ul");
      m.deals.forEach((x) => ul.append(el("li", `${x.on_date} ${x.company} (${x.sector}, ${x.stage}) — source: ${x.source}${x.verified ? `, checked ${x.verified}` : ", not checked"}`)));
      d.append(ul);
      li.append(d);
    }
    const form = el("form", undefined, "intro");
    const area = el("textarea");
    Object.assign(area, { id: `msg-${m.investor_id}`, rows: 2, minLength: 10, maxLength: 1500, required: true, placeholder: "Why this investor, in a few lines" });
    const label = el("label", "Ask for an intro");
    label.htmlFor = area.id;
    const b = el("button", "Send request"); b.type = "submit";
    form.append(label, area, b);
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      try { await api("POST", "/api/intros", { investor_id: m.investor_id, message: area.value }); notice("Intro request sent.", "ok"); area.value = ""; await loadIntros(); }
      catch (err) { notice(err.message); }
    });
    li.append(form);
    return li;
  }));
}

async function loadInvestor(profile) {
  $("i-name").value = profile.name || "";
  document.querySelectorAll("#i-sectors input").forEach((b) => { b.checked = profile.sectors.includes(b.value); });
  document.querySelectorAll("#i-stages input").forEach((b) => { b.checked = profile.stages.includes(b.value); });
  $("i-countries").value = profile.countries.join(", "); $("i-min").value = profile.check_min ?? ""; $("i-max").value = profile.check_max ?? "";
  $("i-contact").value = profile.contact || "";
  $("deals").replaceChildren(...profile.deals.map((d) => {
    const li = el("li", `${d.on_date} ${d.company} (${d.sector}, ${d.stage}) — ${d.source}${d.verified ? `, checked ${d.verified}` : ", not checked"} `);
    const b = el("button", "Remove"); b.type = "button";
    b.addEventListener("click", async () => { try { await api("DELETE", `/api/deals/${d.id}`); await refresh(); } catch (err) { notice(err.message); } });
    li.append(b);
    return li;
  }));
  const data = await api("GET", "/api/startups");
  $("i-disclaimer").textContent = data.disclaimer;
  $("says-vs-does").replaceChildren(...data.says_vs_does.map((n) => el("p", `⚠ Your recorded deals differ from your stated focus: ${n}`, "warn")));
  $("startups").replaceChildren(...data.startups.map((s) => {
    const li = el("li", undefined, "card");
    li.append(el("h3", `${s.name} — ${s.score === null ? "not enough information" : `fit ${Math.round(s.score * 100)} %`}`),
      el("p", `${s.one_liner || ""} ${[s.sector, s.stage, s.country].filter(Boolean).join(" · ")} · raising ${money(s.raising)}`, "meta"),
      componentList(s.components));
    return li;
  }));
}

async function loadIntros() {
  const list = await api("GET", "/api/intros");
  $("intros").replaceChildren(...(list.length ? list.map((i) => {
    const li = el("li", undefined, "card");
    li.append(el("h3", `${i.startup} → ${i.investor}: ${i.status}`), el("p", i.message));
    if (i.their_contact) li.append(el("p", `Contact: ${i.their_contact}`, "ok"));
    if (i.you === "investor" && !["declined", "passed"].includes(i.status)) {
      const row = el("div", undefined, "row");
      for (const s of ["accepted", "in-talks", "passed", "declined"]) {
        if (s === i.status) continue;
        const b = el("button", s); b.type = "button";
        b.addEventListener("click", async () => { try { await api("POST", `/api/intros/${i.id}/status`, { status: s }); await loadIntros(); } catch (err) { notice(err.message); } });
        row.append(b);
      }
      li.append(row);
    }
    if (["accepted", "in-talks"].includes(i.status)) {
      const box = el("div", undefined, "thread");
      api("GET", `/api/intros/${i.id}/messages`).then((msgs) => {
        box.replaceChildren(...msgs.map((m) => el("p", `${m.mine ? "You" : m.from}: ${m.text}`)));
      }).catch((err) => notice(err.message));
      const form = el("form", undefined, "row");
      const input = el("input"); Object.assign(input, { maxLength: 2000, required: true, placeholder: "Message" });
      input.setAttribute("aria-label", "Message");
      const b = el("button", "Send"); b.type = "submit";
      form.append(input, b);
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        try { await api("POST", `/api/intros/${i.id}/messages`, { text: input.value }); await loadIntros(); } catch (err) { notice(err.message); }
      });
      li.append(box, form);
    }
    return li;
  }) : [el("li", "No intros yet.", "meta")]));
}

async function refresh() {
  try {
    const me = await api("GET", "/api/me");
    if (!me.role) {
      $("auth").hidden = false; $("account").hidden = true;
      $("founder").hidden = $("investor").hidden = $("intros-section").hidden = true;
      return;
    }
    $("auth").hidden = true; $("account").hidden = false; $("intros-section").hidden = false;
    $("who").textContent = `${me.email} (${me.role})`;
    $("founder").hidden = me.role !== "founder"; $("investor").hidden = me.role !== "investor";
    if (me.role === "founder") await loadFounder(me.profile); else await loadInvestor(me.profile);
    await loadIntros();
  } catch (err) {
    if (err.status === 401) { $("auth").hidden = false; $("account").hidden = true; $("founder").hidden = $("investor").hidden = $("intros-section").hidden = true; }
    else notice(err.message);
  }
}

$("login").addEventListener("submit", async (e) => {
  e.preventDefault();
  try { await api("POST", "/api/login", { email: $("li-email").value, password: $("li-pw").value }); notice(""); await refresh(); } catch (err) { notice(err.message); }
});
$("register").addEventListener("submit", async (e) => {
  e.preventDefault();
  const role = document.querySelector('input[name="role"]:checked').value;
  try { await api("POST", "/api/register", { role, name: $("re-name").value, email: $("re-email").value, password: $("re-pw").value }); notice(""); await refresh(); }
  catch (err) { notice(err.message); }
});
$("logout").addEventListener("click", async () => { await api("POST", "/api/logout"); await refresh(); });
$("startup-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await api("PUT", "/api/startup", { name: $("s-name").value, one_liner: $("s-line").value, sector: $("s-sector").value || null,
      stage: $("s-stage").value || null, country: $("s-country").value || null, raising: num($("s-raising").value),
      contact: $("s-contact").value, listed: $("s-listed").checked });
    notice("Saved.", "ok"); await refresh();
  } catch (err) { notice(err.message); }
});
$("investor-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const picked = (sel) => [...document.querySelectorAll(`${sel} input:checked`)].map((b) => b.value);
  try {
    await api("PUT", "/api/investor", { name: $("i-name").value, sectors: picked("#i-sectors"), stages: picked("#i-stages"),
      countries: $("i-countries").value.split(",").map((s) => s.trim()).filter(Boolean), check_min: num($("i-min").value),
      check_max: num($("i-max").value), contact: $("i-contact").value });
    notice("Saved.", "ok"); await refresh();
  } catch (err) { notice(err.message); }
});
$("deal-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await api("POST", "/api/deals", { company: $("d-company").value, sector: $("d-sector").value, stage: $("d-stage").value,
      on_date: $("d-date").value, source: $("d-source").value, verified: $("d-verified").value || null });
    e.target.reset(); await refresh();
  } catch (err) { notice(err.message); }
});

api("GET", "/api/vocab").then((v) => {
  vocab = v;
  options($("s-sector"), v.sectors); options($("s-stage"), v.stages);
  options($("d-sector"), v.sectors, "Choose"); options($("d-stage"), v.stages, "Choose");
  $("d-sector").required = $("d-stage").required = true;
  checks($("i-sectors"), "sectors", v.sectors); checks($("i-stages"), "stages", v.stages);
  return refresh();
}).catch((err) => notice(err.message));
