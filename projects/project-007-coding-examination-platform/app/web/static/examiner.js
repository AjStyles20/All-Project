// Examiner screens: examinations, questions, candidates, contract, marking, release.
// Every rule is enforced by the server; refusals are shown to the examiner as they arrive.
import { api, capabilityText, el, say, show, when, words } from "./core.js";

const go = (hash) => { location.hash = hash; };
const part = encodeURIComponent;

// Next lifecycle steps offered as buttons; the server's transition matrix remains the authority.
const NEXT_STEPS = {
  DRAFT: [["SCHEDULED", "Schedule (locks the rules)"]],
  SCHEDULED: [["ACTIVE", "Open the examination"], ["DRAFT", "Return to draft"]],
  ACTIVE: [["CLOSED", "Close (submits open sessions)"]],
  CLOSED: [["ARCHIVED", "Archive (freezes marks)"]],
  ARCHIVED: [],
};

function field(label, input, hint) {
  return el("div", {}, el("label", { for: input.id, text: label }), input,
    hint ? el("p", { class: "meta", text: hint }) : null);
}

function textInput(id, value = "", extra = {}) {
  const input = el("input", { id, type: "text", ...extra });
  input.value = value ?? "";
  return input;
}

function selectInput(id, options, value) {
  const select = el("select", { id }, options.map(([v, text]) => el("option", { value: v, text })));
  if (value !== undefined && value !== null) select.value = value;
  return select;
}

function dateInput(id, iso) {
  const input = el("input", { id, type: "datetime-local" });
  if (iso) {
    // API times are naive UTC; the control shows the examiner's local time.
    const date = new Date(iso + "Z");
    input.value = new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  }
  return input;
}

const dateValue = (input) => (input.value ? new Date(input.value).toISOString() : null);

async function attempt(action, success) {
  try {
    const result = await action();
    if (success) say(success);
    return result ?? true;
  } catch (error) {
    say(error.message, "error");
    return null;
  }
}

function backTo(hash, text) {
  return el("button", { type: "button", text, onclick: () => go(hash) });
}

// ---------- home: examinations and question bank ----------

export async function examinerHome() {
  const [exams, questions] = await Promise.all([api("GET", "/examiner/examinations"), api("GET", "/examiner/questions")]);
  const title = textInput("new-exam-title", "", { required: true, maxlength: 200 });
  const description = el("textarea", { id: "new-exam-description", class: "short" });
  const starts = dateInput("new-exam-starts");
  const ends = dateInput("new-exam-ends");
  const qTitle = textInput("new-q-title", "", { required: true, maxlength: 200 });
  const qPrompt = el("textarea", { id: "new-q-prompt", class: "short", required: true });
  const qLanguage = textInput("new-q-language", "python", { required: true, maxlength: 50 });
  const qMax = textInput("new-q-max", "10", { required: true, inputmode: "numeric" });

  show(el("section", {},
    el("h2", { text: "My examinations" }),
    exams.length ? exams.map((exam) => el("article", { class: "card" },
      el("h3", { text: exam.title }),
      el("p", { class: "meta" }, el("span", { class: "badge", text: exam.status })),
      el("p", { class: "meta", text: `Opens ${when(exam.starts_at)} · Ends ${when(exam.ends_at)}` }),
      el("div", { class: "actions" }, el("button", { type: "button", class: "primary", text: "Manage",
        onclick: () => go(`#/examiner/exam/${part(exam.examination_id)}`) })),
    )) : el("p", { class: "card", text: "You have no examinations yet." }),
    el("form", { class: "card", onsubmit: async (event) => {
      event.preventDefault();
      const created = await attempt(() => api("POST", "/examiner/examinations", {
        title: title.value, description: description.value, starts_at: dateValue(starts), ends_at: dateValue(ends) }));
      if (created) go(`#/examiner/exam/${part(created.examination_id)}`);
    } },
      el("h3", { text: "New examination" }),
      field("Title", title), field("Description (optional)", description),
      field("Opens (optional)", starts), field("Ends (optional)", ends),
      el("div", { class: "actions" }, el("button", { type: "submit", class: "primary", text: "Create" }))),
    el("h2", { text: "My questions" }),
    questions.length ? el("div", { class: "card" }, el("table", {},
      el("thead", {}, el("tr", {}, el("th", { text: "Title" }), el("th", { text: "Language" }), el("th", { text: "Max score" }))),
      el("tbody", {}, questions.map((q) => el("tr", {}, el("td", { text: q.title }), el("td", { text: q.language }), el("td", { text: q.max_score }))))))
      : el("p", { class: "card", text: "You have no questions yet." }),
    el("form", { class: "card", onsubmit: async (event) => {
      event.preventDefault();
      const created = await attempt(() => api("POST", "/examiner/questions", {
        title: qTitle.value, prompt: qPrompt.value, language: qLanguage.value, max_score: Number(qMax.value) }), "Question created.");
      if (created) examinerHome();
    } },
      el("h3", { text: "New question" }),
      field("Title", qTitle), field("Prompt", qPrompt), field("Language", qLanguage), field("Max score", qMax),
      el("div", { class: "actions" }, el("button", { type: "submit", class: "primary", text: "Create question" }))),
  ));
}

// ---------- one examination ----------

export async function examView(examId) {
  const base = `/examiner/examinations/${part(examId)}`;
  const [exam, questions, assignments] = await Promise.all([
    api("GET", base), api("GET", "/examiner/questions"), api("GET", `${base}/assignments`)]);
  const reload = () => examView(examId);
  const isDraft = exam.status === "DRAFT";

  const steps = NEXT_STEPS[exam.status].map(([target, text]) => el("button", {
    type: "button", class: "primary", text,
    onclick: async () => {
      if (await attempt(() => api("POST", `${base}/transition`, { target_status: target }), `Examination is now ${words(target)}.`)) reload();
    },
  }));

  const title = textInput("exam-title", exam.title, { required: true, maxlength: 200, readonly: !isDraft });
  const description = el("textarea", { id: "exam-description", class: "short", readonly: !isDraft });
  description.value = exam.description;
  const starts = dateInput("exam-starts", exam.starts_at);
  const ends = dateInput("exam-ends", exam.ends_at);
  starts.disabled = ends.disabled = !isDraft;

  const attached = new Set(exam.questions.map((q) => q.question_id));
  const available = questions.filter((q) => !attached.has(q.question_id));
  const questionPick = selectInput("attach-question", available.map((q) => [q.question_id, q.title]));
  const order = textInput("attach-order", String(exam.questions.length + 1), { inputmode: "numeric" });
  const weight = textInput("attach-weight", "1", { inputmode: "numeric" });
  const candidate = textInput("assign-candidate", "", { required: true, maxlength: 64 });

  show(el("section", {},
    el("h2", { text: exam.title }),
    el("div", { class: "card" },
      el("p", {}, "Status: ", el("span", { class: "badge", text: exam.status })),
      el("p", { class: "meta", text: `Examination id (for research administration): ${exam.examination_id}` }),
      el("div", { class: "actions" }, steps,
        el("button", { type: "button", text: "Rules (contract)", onclick: () => go(`#/examiner/exam/${part(examId)}/contract`) }),
        el("button", { type: "button", text: "Sessions and marking", onclick: () => go(`#/examiner/exam/${part(examId)}/sessions`) }),
        backTo("#/examiner", "Back"))),
    el("form", { class: "card", onsubmit: async (event) => {
      event.preventDefault();
      if (await attempt(() => api("PATCH", base, { title: title.value, description: description.value,
        starts_at: dateValue(starts), ends_at: dateValue(ends) }), "Details saved.")) reload();
    } },
      el("h3", { text: "Details" }),
      isDraft ? null : el("p", { class: "meta", text: "Details can only be changed while the examination is a draft." }),
      field("Title", title), field("Description", description), field("Opens", starts), field("Ends", ends),
      isDraft ? el("div", { class: "actions" }, el("button", { type: "submit", text: "Save details" })) : null),
    el("div", { class: "card" },
      el("h3", { text: "Questions" }),
      exam.questions.length ? el("table", {},
        el("thead", {}, el("tr", {}, ["Order", "Title", "Max", "Weight", ""].map((h) => el("th", { text: h })))),
        el("tbody", {}, exam.questions.map((q) => el("tr", {},
          el("td", { text: q.display_order }), el("td", { text: q.title }), el("td", { text: q.max_score }), el("td", { text: q.score_weight }),
          el("td", {}, isDraft ? el("button", { type: "button", text: "Remove", "aria-label": `Remove ${q.title}`, onclick: async () => {
            if (await attempt(() => api("DELETE", `${base}/questions/${part(q.question_id)}`), "Question removed.")) reload();
          } }) : null))))) : el("p", { class: "meta", text: "No questions attached. An examination needs at least one before scheduling." }),
      isDraft && available.length ? el("form", { onsubmit: async (event) => {
        event.preventDefault();
        if (await attempt(() => api("POST", `${base}/questions`, { question_id: questionPick.value,
          display_order: Number(order.value), score_weight: Number(weight.value) }), "Question attached.")) reload();
      } },
        field("Add question", questionPick), field("Display order", order), field("Weight", weight),
        el("div", { class: "actions" }, el("button", { type: "submit", text: "Attach" }))) : null),
    el("div", { class: "card" },
      el("h3", { text: "Candidates" }),
      assignments.length ? el("ul", {}, assignments.map((a) => el("li", { text: a.candidate_user_id })))
        : el("p", { class: "meta", text: "No candidates assigned." }),
      ["CLOSED", "ARCHIVED"].includes(exam.status) ? null : el("form", { onsubmit: async (event) => {
        event.preventDefault();
        if (await attempt(() => api("POST", `${base}/assignments`, { candidate_user_id: candidate.value }), "Candidate assigned.")) reload();
      } },
        field("Assign by user id", candidate, "There is no user directory yet, so enter the candidate's user id."),
        el("div", { class: "actions" }, el("button", { type: "submit", text: "Assign" })))),
  ));
}

// ---------- contract ----------

function capabilityEditor(schema, current) {
  const rows = Object.entries(schema.capabilities).map(([key, values]) => {
    const saved = current ? current[key] : undefined;
    const savedValue = typeof saved === "string" ? saved : saved && saved.value;
    const select = selectInput(`cap-${key}`, values.map((v) => [v, words(v)]), savedValue || (values.includes("DENY") ? "DENY" : values[0]));
    const detail = textInput(`cap-${key}-detail`);
    const detailLabel = el("label", { for: detail.id, class: "meta" });
    const detailField = () => schema.detail_fields[select.value];
    if (saved && typeof saved === "object") {
      const stored = saved[schema.detail_fields[saved.value]];
      detail.value = Array.isArray(stored) ? stored.join(", ") : stored;
    }
    const wrap = el("div", {}, detailLabel, detail);
    const refresh = () => {
      const name = detailField();
      wrap.hidden = !name;
      detailLabel.textContent = name === "limits" ? "Describe the limits" : `${words(name || "")} (comma separated)`;
    };
    select.addEventListener("change", refresh);
    refresh();
    return {
      row: el("tr", {}, el("th", { scope: "row" }, el("label", { for: select.id, text: words(key) })), el("td", {}, select, wrap)),
      read: () => {
        const name = detailField();
        if (!name) return [key, select.value];
        const text = detail.value.trim();
        return [key, { value: select.value, [name]: name === "limits" ? text : text.split(",").map((s) => s.trim()).filter(Boolean) }];
      },
    };
  });
  return { table: el("table", {}, el("tbody", {}, rows.map((r) => r.row))), read: () => Object.fromEntries(rows.map((r) => r.read())) };
}

export async function contractView(examId) {
  const base = `/examiner/examinations/${part(examId)}`;
  const [exam, versions, exceptions, assignments, schema] = await Promise.all([
    api("GET", base), api("GET", `${base}/contract`), api("GET", `${base}/contract/exceptions`),
    api("GET", `${base}/assignments`), api("GET", "/examiner/contract-schema")]);
  const reload = () => contractView(examId);
  const latest = versions[versions.length - 1];
  const editable = exam.status === "DRAFT";
  const amendable = ["SCHEDULED", "ACTIVE"].includes(exam.status);

  const editor = capabilityEditor(schema, latest && latest.capabilities);
  const mode = selectInput("contract-mode", schema.integrity_modes.map((m) => [m, words(m)]), latest ? latest.integrity_mode : schema.default_integrity_mode);
  const justification = el("textarea", { id: "contract-justification", class: "short" });
  justification.value = (latest && latest.remote_proctoring_justification) || "";
  const reason = el("textarea", { id: "contract-reason", class: "short" });
  const needsReason = amendable || (editable && latest && latest.status !== "DRAFT") || (editable && latest && latest.supersedes_version);

  const candidate = selectInput("exception-candidate", assignments.map((a) => [a.candidate_user_id, a.candidate_user_id]));
  const category = selectInput("exception-reason", schema.exception_reasons.map((r) => [r, words(r)]));
  const minutes = textInput("exception-minutes", "0", { inputmode: "numeric" });
  const overrideKey = selectInput("exception-capability", [["", "None"], ...Object.keys(schema.capabilities).map((k) => [k, words(k)])]);
  const overrideValue = selectInput("exception-value", []);
  const overrideWrap = el("div", { hidden: true }, field("Allow as", overrideValue, "Values needing extra detail can only be set through the API."));
  overrideKey.addEventListener("change", () => {
    const simple = (schema.capabilities[overrideKey.value] || []).filter((v) => !schema.detail_fields[v]);
    overrideValue.replaceChildren(...simple.map((v) => el("option", { value: v, text: words(v) })));
    overrideWrap.hidden = !overrideKey.value;
  });

  const body = () => ({ capabilities: editor.read(), integrity_mode: mode.value,
    remote_proctoring_justification: justification.value || null, amendment_reason: reason.value || null });

  show(el("section", {},
    el("h2", { text: `Rules: ${exam.title}` }),
    el("p", { class: "banner", text: "These rules are declared, not enforced by software." }),
    el("div", { class: "card" },
      el("h3", { text: "Versions" }),
      versions.length ? el("table", {},
        el("thead", {}, el("tr", {}, ["Version", "Status", "Locked", "Reason"].map((h) => el("th", { text: h })))),
        el("tbody", {}, versions.map((v) => el("tr", {},
          el("td", { text: v.version }), el("td", { text: words(v.status) }), el("td", { text: when(v.bound_at) }), el("td", { text: v.amendment_reason || "—" })))))
        : el("p", { class: "meta", text: "No contract yet. An examination needs one before scheduling." }),
      el("div", { class: "actions" }, backTo(`#/examiner/exam/${part(examId)}`, "Back"))),
    editable || amendable ? el("form", { class: "card", onsubmit: async (event) => {
      event.preventDefault();
      const saved = amendable
        ? await attempt(() => api("POST", `${base}/contract/amendments`, body()), "Amendment locked as a new version.")
        : await attempt(() => api("PUT", `${base}/contract`, body()), "Draft saved. It locks when you schedule.");
      if (saved) reload();
    } },
      el("h3", { text: amendable ? "Amend (creates a new locked version)" : "Draft" }),
      field("Integrity mode", mode),
      field("Remote-proctoring justification", justification, "Required only for remote proctored."),
      editor.table,
      needsReason ? field("Reason for this change", reason, "Required: candidates may already have seen the earlier version.") : null,
      el("div", { class: "actions" }, el("button", { type: "submit", class: "primary", text: amendable ? "Lock amendment" : "Save draft" })))
      : el("p", { class: "card", text: "This examination is finished, so its contract can no longer change." }),
    el("div", { class: "card" },
      el("h3", { text: "Candidate exceptions" }),
      exceptions.length ? el("table", {},
        el("thead", {}, el("tr", {}, ["Candidate", "Extra time", "Capabilities", "Reason"].map((h) => el("th", { text: h })))),
        el("tbody", {}, exceptions.map((e) => el("tr", {},
          el("td", { text: e.candidate_user_id }), el("td", { text: `${e.extra_time_minutes} min` }),
          el("td", { text: Object.entries(e.capability_overrides).map(([k, v]) => `${words(k)}: ${capabilityText(v)}`).join(", ") || "—" }),
          el("td", { text: words(e.reason_category) }))))) : el("p", { class: "meta", text: "None." }),
      amendable && assignments.length ? el("form", { onsubmit: async (event) => {
        event.preventDefault();
        const overrides = overrideKey.value ? { [overrideKey.value]: overrideValue.value } : {};
        if (await attempt(() => api("POST", `${base}/contract/exceptions`, { candidate_user_id: candidate.value,
          reason_category: category.value, capability_overrides: overrides, extra_time_minutes: Number(minutes.value) }), "Exception granted.")) reload();
      } },
        field("Candidate", candidate), field("Reason category", category, "Category only: detailed reasons are deliberately not stored."),
        field("Extra minutes", minutes), field("Capability exception", overrideKey), overrideWrap,
        el("div", { class: "actions" }, el("button", { type: "submit", text: "Grant exception" })))
        : el("p", { class: "meta", text: "Exceptions can be granted while the examination is scheduled or open, to assigned candidates." })),
  ));
}

// ---------- sessions, marking, release ----------

export async function sessionsView(examId) {
  const base = `/examiner/examinations/${part(examId)}`;
  const sessions = await api("GET", `${base}/sessions`);
  show(el("section", {},
    el("h2", { text: "Sessions and marking" }),
    el("div", { class: "card" },
      sessions.length ? el("table", {},
        el("thead", {}, el("tr", {}, ["Candidate", "Status", "Marked", "Raw", "Weighted", ""].map((h) => el("th", { text: h })))),
        el("tbody", {}, sessions.map((s) => el("tr", {},
          el("td", { text: s.candidate_user_id }),
          el("td", { text: words(s.status) + (s.submission_mode === "AUTO_ON_CLOSE" ? " (automatic)" : "") }),
          el("td", { text: `${s.marked_questions} / ${s.total_questions}` }),
          el("td", { text: `${s.raw_score} / ${s.raw_max}` }),
          el("td", { text: s.weighted_percent === null ? "not fully marked" : `${s.weighted_percent}%` }),
          el("td", {}, el("button", { type: "button", text: "Review", "aria-label": `Review ${s.candidate_user_id}`, onclick: () => go(`#/examiner/session/${part(s.session_id)}`) }))))))
        : el("p", { class: "meta", text: "No candidate has started yet." }),
      el("div", { class: "actions" },
        el("button", { type: "button", class: "primary", text: "Release results", onclick: async () => {
          if (!confirm("Release results to candidates? Marks are locked afterwards.")) return;
          const released = await attempt(() => api("POST", `${base}/release`));
          if (released) say(`Results released ${when(released.released_at)}. Marks are now locked.`);
        } }),
        backTo(`#/examiner/exam/${part(examId)}`, "Back"))),
  ));
}

export async function reviewView(sessionId) {
  const review = await api("GET", `/examiner/sessions/${part(sessionId)}`);
  const locked = Boolean(review.release);
  const cards = review.questions.map((q) => {
    const score = textInput(`score-${q.question_id}`, q.mark ? String(q.mark.score) : "", { inputmode: "numeric", required: true, readonly: locked });
    const comment = el("textarea", { id: `comment-${q.question_id}`, class: "short", readonly: locked });
    comment.value = q.mark ? q.mark.comment : "";
    const answer = el("textarea", { id: `answer-${q.question_id}`, readonly: true });
    answer.value = q.response ? q.response.content : "";
    return el("form", { class: "card", onsubmit: async (event) => {
      event.preventDefault();
      if (await attempt(() => api("PUT", `/examiner/sessions/${part(sessionId)}/marks/${part(q.question_id)}`,
        { score: Number(score.value), comment: comment.value }), "Mark saved.")) reviewView(sessionId);
    } },
      el("h3", { text: `${q.display_order}. ${q.title}` }),
      el("p", { text: q.prompt }),
      q.response
        ? el("p", { class: "meta", text: `Saved ${when(q.response.saved_at)} (revision ${q.response.revision})` })
        : el("p", { class: "meta", text: "No answer was saved." }),
      el("label", { for: answer.id, text: `Answer to question ${q.display_order}` }), answer,
      field(`Score out of ${q.max_score} (weight ${q.score_weight})`, score),
      field("Comment (shown to the candidate after release)", comment),
      q.mark_history.length > 1 ? el("details", {}, el("summary", { text: "Earlier marks" }),
        el("ul", {}, q.mark_history.map((m) => el("li", { text: `${m.score} by ${m.marked_by_user_id}, ${when(m.marked_at)}${m.comment ? `: ${m.comment}` : ""}` })))) : null,
      locked ? null : el("div", { class: "actions" }, el("button", { type: "submit", class: "primary", text: "Save mark" })));
  });
  show(el("section", {},
    el("h2", { text: `Review: ${review.candidate_user_id}` }),
    el("p", { class: "deadline" }, el("strong", { text: words(review.status) }),
      review.submitted_at ? ` · Submitted ${when(review.submitted_at)}${review.submission_mode === "AUTO_ON_CLOSE" ? " (automatically, when the examination closed)" : ""}` : "",
      locked ? ` · Results released ${when(review.release.released_at)}; marks are locked` : ""),
    cards,
    el("div", { class: "actions" }, backTo(`#/examiner/exam/${part(review.examination_id)}/sessions`, "Back to sessions")),
  ));
}
