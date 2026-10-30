// Administrator research screens (FD-06, DR-015, DR-016). The API has no administrator
// list of examinations yet, so an examination is opened by its id.
import { api, el, say, show, when, words } from "./core.js";

const part = encodeURIComponent;

function textField(id, label, extra = {}, hint) {
  const input = el("input", { id, type: "text", ...extra });
  return { input, node: el("div", {}, el("label", { for: id, text: label }), input, hint ? el("p", { class: "meta", text: hint }) : null) };
}

export function adminHome() {
  const exam = textField("admin-exam-id", "Examination id", { required: true, maxlength: 64 },
    "Ask the examiner: it is shown on their examination screen. There is no administrator list of examinations yet.");
  show(el("form", { class: "card", onsubmit: (event) => {
    event.preventDefault();
    location.hash = `#/admin/exam/${part(exam.input.value.trim())}`;
  } },
    el("h2", { text: "Research administration" }), exam.node,
    el("div", { class: "actions" }, el("button", { type: "submit", class: "primary", text: "Open" }))));
}

export async function adminExamView(examId) {
  const base = `/admin/research/examinations/${part(examId)}`;
  const [questions, links, records, withdrawals] = await Promise.all([
    api("GET", `${base}/questions`), api("GET", `${base}/links`), api("GET", `${base}/records`), api("GET", `${base}/withdrawals`)]);
  const titles = Object.fromEntries(questions.map((q) => [q.question_id, q.title]));
  const linked = new Set(links.map((l) => l.question_id));
  const unlinked = questions.filter((q) => !linked.has(q.question_id));
  const reload = () => adminExamView(examId);
  const question = { input: el("select", { id: "link-question" }, unlinked.map((q) => el("option", { value: q.question_id, text: q.title }))) };
  question.node = el("div", {}, el("label", { for: "link-question", text: "Question" }), question.input);
  const template = textField("link-template", "Template case id", { required: true, maxlength: 128 });
  const claims = textField("link-claims", "Claim ids (comma separated)", { required: true }, "Each must be a REQUIRED claim of the template case.");
  const ethics = textField("link-ethics", "Ethics approval reference", { required: true, maxlength: 200 },
    "Recorded, not verified. Enter it only once institutional approval really exists.");
  const identities = el("div", {});

  const action = (text, primary, run) => el("button", { type: "button", class: primary ? "primary" : undefined, text, onclick: async () => {
    try { await run(); } catch (error) { say(error.message, "error"); }
  } });

  show(el("section", {},
    el("h2", { text: "Research administration" }),
    el("p", { class: "meta", text: `Examination ${examId}` }),
    el("div", { class: "card" },
      el("h3", { text: "Research links" }),
      links.length ? el("table", {},
        el("thead", {}, el("tr", {}, ["Question", "Template", "Claims", "Ethics reference"].map((h) => el("th", { text: h })))),
        el("tbody", {}, links.map((l) => el("tr", {}, el("td", { text: titles[l.question_id] || l.question_id }), el("td", { text: l.template_case_id }),
          el("td", { text: l.claim_ids.join(", ") }), el("td", { text: l.ethics_reference }))))) : el("p", { class: "meta", text: "No links. Nothing can be bridged without one." }),
      !unlinked.length ? el("p", { class: "meta", text: "Every question of this examination already has a link." }) : el("form", { onsubmit: async (event) => {
        event.preventDefault();
        try {
          await api("POST", "/admin/research/links", { examination_id: examId, question_id: question.input.value.trim(),
            template_case_id: template.input.value.trim(), ethics_reference: ethics.input.value.trim(),
            claim_ids: claims.input.value.split(",").map((c) => c.trim()).filter(Boolean) });
          say("Research link created.");
          reload();
        } catch (error) { say(error.message, "error"); }
      } },
        question.node, template.node, claims.node, ethics.node,
        el("div", { class: "actions" }, el("button", { type: "submit", text: "Create link" })))),
    el("div", { class: "card" },
      el("h3", { text: "Evidence bridge" }),
      el("p", { class: "meta", text: "Copies only submitted answers of candidates currently opted in, after the examination is closed. Safe to run again." }),
      el("div", { class: "actions" },
        action("Run bridge", true, async () => {
          const s = await api("POST", `${base}/bridge`);
          say(`Bridged ${s.bridged}; no response ${s.no_response}; no contract ${s.no_contract}; already recorded ${s.already_recorded}; not opted in ${s.skipped_no_consent}.`);
          reload();
        }),
        action("Retry pending deletions", false, async () => {
          const r = await api("POST", `${base}/purge-withdrawn`);
          say(r.deletion_pending ? "Deletion is still pending: the research store is unavailable."
            : `Deleted ${r.cases_deleted} case(s); kept ${r.cases_retained_as_shell} empty case(s) referenced by analyses.`);
          reload();
        })),
      records.length ? el("table", {},
        el("thead", {}, el("tr", {}, ["Outcome", "Research case", "Policy version", "When"].map((h) => el("th", { text: h })))),
        el("tbody", {}, records.map((r) => el("tr", {}, el("td", { text: words(r.outcome) }), el("td", { text: r.research_case_id || "—" }),
          el("td", { text: r.policy_version || "—" }), el("td", { text: when(r.bridged_at) }))))) : el("p", { class: "meta", text: "Nothing bridged yet." })),
    el("div", { class: "card" },
      el("h3", { text: "Withdrawal log" }),
      withdrawals.length ? el("ul", {}, withdrawals.map((w) => el("li", { text: `${w.research_code}: ${w.cases_deleted} deleted, ${w.cases_retained_as_shell} kept as empty, ${when(w.completed_at)}` })))
        : el("p", { class: "meta", text: "No withdrawals processed." })),
    el("div", { class: "card" },
      el("h3", { text: "Code to person link" }),
      el("p", { class: "meta", text: "Sensitive. Shown only on request, and not loaded otherwise." }),
      el("div", { class: "actions" }, action("Show identities", false, async () => {
        const rows = await api("GET", `${base}/identities`);
        identities.replaceChildren(rows.length ? el("ul", {}, rows.map((r) => el("li", { text: `${r.research_code}: ${r.candidate_user_id}` })))
          : el("p", { class: "meta", text: "None." }));
      })), identities),
  ));
}
