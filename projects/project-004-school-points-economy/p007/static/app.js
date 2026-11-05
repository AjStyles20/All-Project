// P007 dashboard. All text goes through textContent; nothing from the server is parsed as HTML.
const $ = (id) => document.getElementById(id);

function el(tag, text, cls) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (cls) node.className = cls;
  return node;
}

function say(text, kind = "") {
  $("status").replaceChildren(text ? el("p", text, kind) : "");
}

async function api(method, path, body) {
  const response = await fetch(path, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join("; ") : data.detail;
    throw new Error(detail || `Request failed (${response.status})`);
  }
  return data;
}

async function loadBalances() {
  const rows = await api("GET", "/api/students");
  if (!rows.length) { $("balances").replaceChildren(el("p", "No students yet.", "meta")); return; }
  const table = el("table");
  const head = el("tr");
  ["Student", "Group", "Balance"].forEach((h) => head.append(el("th", h)));
  table.append(el("thead"), el("tbody"));
  table.tHead.append(head);
  for (const r of rows) {
    const tr = el("tr");
    tr.append(el("td", r.student_id), el("td", r.group_label), el("td", String(r.balance)));
    table.tBodies[0].append(tr);
  }
  $("balances").replaceChildren(table);
}

function list(title, items) {
  if (!items.length) return null;
  const wrap = el("div");
  const ul = el("ul");
  items.forEach((i) => ul.append(el("li", i)));
  wrap.append(el("h4", title), ul);
  return wrap;
}

async function runAudit(event) {
  event.preventDefault();
  try {
    const report = await api("GET", `/api/audit?engine=${encodeURIComponent($("engine").value)}`);
    const out = [el("p", `Overall: ${report.state}`, "state " + report.state.toLowerCase().replaceAll(" ", "-"))];
    if (!report.findings.length) out.push(el("p", "Nothing for review.", "meta"));
    for (const f of report.findings) {
      const card = el("article", undefined, "finding");
      card.append(el("h3", `${f.state} — ${f.kind.replaceAll("_", " ").toLowerCase()} (${f.subject})`));
      if (f.comparison) card.append(el("p", f.comparison));
      [list("Observed", f.observations), list("Missing context", f.missing_context), list("Not claimed", f.non_claims)]
        .forEach((part) => part && card.append(part));
      out.push(card);
    }
    $("audit").replaceChildren(...out);
  } catch (error) {
    say(error.message, "error");
  }
}

async function loadDemo(event) {
  event.preventDefault();
  try {
    const result = await api("POST", "/api/demo", { scenario: $("scenario").value, seed: Number($("seed").value) });
    say(`Loaded ${result.students} students and ${result.transactions} transactions.`);
    await loadBalances();
  } catch (error) {
    say(error.message, "error");
  }
}

async function start() {
  const scenarios = await api("GET", "/api/scenarios");
  $("scenario").replaceChildren(...scenarios.map((s) => {
    const option = el("option", `${s.id} ${s.name}`);
    option.value = s.id;
    return option;
  }));
  $("demo-form").addEventListener("submit", loadDemo);
  $("audit-form").addEventListener("submit", runAudit);
  await loadBalances();
}

start().catch((error) => say(error.message, "error"));
