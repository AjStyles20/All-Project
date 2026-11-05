// Defence practice page. Token from the URL fragment, sent as a header; all text via textContent.
const token = new URLSearchParams(location.hash.slice(1)).get("token") || "";
history.replaceState(null, "", location.pathname);
const $ = (id) => document.getElementById(id);
const KIND = {
  UNSUPPORTED_CLAIM: "Strong claim without evidence", QUANTIFIED_CLAIM: "Claim with a figure", CONTRADICTION: "Figures disagree",
  LIMITATION: "Admitted limitation", REQUIREMENT: "Requirement", METHOD: "Method", SECURITY: "Security or privacy",
  GENERAL: "General question (not from your documents)",
};

function el(tag, text, cls) {
  const n = document.createElement(tag);
  if (text !== undefined && text !== null) n.textContent = text;
  if (cls) n.className = cls;
  return n;
}

function notice(text, kind = "error") { $("notice").replaceChildren(text ? el("p", text, kind) : ""); }

async function api(method, path, body, raw) {
  const headers = { "X-Token": token };
  if (body && !raw) headers["Content-Type"] = "application/json";
  const r = await fetch(path, { method, headers, body: raw ? body : body ? JSON.stringify(body) : undefined });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(typeof data.detail === "string" ? data.detail : Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join("; ") : `Request failed (${r.status})`);
  return data;
}

async function loadDocuments() {
  const docs = await api("GET", "/api/documents");
  $("documents").replaceChildren(...docs.map((d) => {
    const li = el("li", `${d.name} (${d.chunks} passages) `);
    const b = el("button", "Remove");
    b.type = "button";
    b.addEventListener("click", async () => { await api("DELETE", `/api/documents/${d.id}`); await loadDocuments(); });
    li.append(b);
    return li;
  }));
}

async function loadRoles() {
  const roles = await api("GET", "/api/roles");
  $("roles").replaceChildren(...roles.map((r, i) => {
    const row = el("div", undefined, "option");
    const box = el("input");
    Object.assign(box, { type: "checkbox", id: `role-${r.key}`, value: r.key, checked: i < 2 });
    const label = el("label", `${r.name}: ${r.purpose}`);
    label.htmlFor = box.id;
    row.append(box, label);
    return row;
  }));
}

function evidenceBlock(q) {
  const d = el("details");
  d.append(el("summary", q.grounded ? "Where this comes from" : "Not from your documents"));
  for (const c of q.evidence || []) d.append(el("p", `${c.document}, ${c.locator}:`, "meta"), el("blockquote", c.text));
  return d;
}

function feedbackList(items) {
  const ul = el("ul", undefined, "feedback");
  items.forEach((i) => ul.append(el("li", `${i.criterion} (${i.basis === "source" ? "checked against your documents" : "text check"}): ${i.observation}`)));
  return ul;
}

async function showSession(id) {
  const s = await api("GET", `/api/sessions/${id}`);
  const cards = s.questions.map((q, n) => {
    const card = el("article", undefined, "card");
    card.append(el("p", `${n + 1}. ${q.role} — ${KIND[q.category] || q.category}`, "tag"), el("p", q.text, "prompt"), evidenceBlock(q));
    if (q.answer) {
      card.append(el("p", `Your answer: ${q.answer}`), feedbackList(q.feedback));
    } else {
      const form = el("form");
      const area = el("textarea");
      Object.assign(area, { id: `a-${q.id}`, rows: 4, maxLength: 5000, required: true });
      const label = el("label", "Your answer");
      label.htmlFor = area.id;
      const b = el("button", "Submit answer");
      b.type = "submit";
      form.append(label, area, b);
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        try { await api("POST", `/api/questions/${q.id}/answer`, { text: area.value }); await showSession(id); } catch (err) { notice(err.message); }
      });
      card.append(form);
    }
    return card;
  });
  $("session").replaceChildren(el("p", "Feedback lists observations by criterion. It is not a grade.", "meta"), ...cards);
}

$("upload").addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = $("file").files[0];
  if (!file) return;
  try {
    const r = await api("POST", `/api/documents?name=${encodeURIComponent(file.name)}`, await file.arrayBuffer(), true);
    notice(`Added ${file.name}: ${r.chunks} passages.`, "ok");
    $("file").value = "";
    await loadDocuments();
  } catch (err) { notice(err.message); }
});

$("analyse").addEventListener("click", async () => {
  try {
    const f = await api("GET", "/api/findings");
    $("findings").replaceChildren(...(f.length ? f.map((x) => {
      const li = el("li");
      li.append(el("strong", `${KIND[x.kind]}: `), el("span", x.sentence), el("div", `${x.where}${x.detail ? ` · ${x.detail}` : ""}`, "meta"));
      return li;
    }) : [el("li", "Nothing found yet. Upload a document first.", "meta")]));
  } catch (err) { notice(err.message); }
});

$("new-session").addEventListener("submit", async (e) => {
  e.preventDefault();
  const roles = [...document.querySelectorAll("#roles input:checked")].map((b) => b.value);
  if (!roles.length) { notice("Choose at least one reviewer."); return; }
  try { const s = await api("POST", "/api/sessions", { roles }); await showSession(s.id); } catch (err) { notice(err.message); }
});

$("search").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    const r = await api("GET", `/api/search?q=${encodeURIComponent($("q").value)}`);
    $("results").replaceChildren(...(r.length ? r.map((x) => el("li", `${x.document}, ${x.locator}: ${x.snippet}`)) : [el("li", "No matches.", "meta")]));
  } catch (err) { notice(err.message); }
});

if (!token) notice("Open this page with the link printed when the program started.");
else Promise.all([loadDocuments(), loadRoles()]).catch((e) => notice(e.message));
