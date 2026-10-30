// Candidate screens: examinations, rules, research consent, session with autosave, result.
import { api, capabilityText, el, say, show, when } from "./core.js";

const AUTOSAVE_DELAY_MS = 1500;
const RETRY_DELAY_MS = 5000;

export async function examsView() {
  const exams = await api("GET", "/candidate/examinations");
  const cards = exams.map((exam) => el("article", { class: "card" },
    el("h3", { text: exam.title }),
    el("p", { class: "meta" }, el("span", { class: "badge", text: exam.status })),
    el("p", { class: "meta", text: `Opens ${when(exam.starts_at)} · Ends ${when(exam.ends_at)}` }),
    el("div", { class: "actions" },
      el("button", { type: "button", text: "Rules", onclick: () => (location.hash = `#/exam/${exam.examination_id}/rules`) }),
      el("button", { type: "button", text: "Research participation", onclick: () => (location.hash = `#/exam/${exam.examination_id}/research`) }),
      exam.status === "ACTIVE"
        ? el("button", { type: "button", class: "primary", text: "Start or resume", onclick: () => startOrResume(exam.examination_id) })
        : null,
      ["CLOSED", "ARCHIVED", "ACTIVE"].includes(exam.status)
        ? el("button", { type: "button", text: "My result", onclick: () => (location.hash = `#/exam/${exam.examination_id}/result`) })
        : null,
    ),
  ));
  show(el("section", {}, el("h2", { text: "My examinations" }),
    cards.length ? cards : el("p", { class: "card", text: "You have no assigned examinations." })));
}

async function startOrResume(examId) {
  try {
    const session = await api("POST", `/candidate/examinations/${encodeURIComponent(examId)}/session`);
    location.hash = `#/session/${session.session_id}`;
  } catch (error) {
    say(error.message, "error");
  }
}

export async function rulesView(examId) {
  const contract = await api("GET", `/candidate/examinations/${encodeURIComponent(examId)}/contract`);
  const rows = Object.entries(contract.capabilities).map(([key, value]) =>
    el("tr", {}, el("th", { scope: "row", text: key.replace(/_/g, " ") }), el("td", { text: capabilityText(value) })));
  const exceptions = contract.my_exceptions.map((exception) => el("li", {
    text: [
      exception.extra_time_minutes ? `${exception.extra_time_minutes} extra minutes` : null,
      ...Object.entries(exception.capability_overrides).map(([key, value]) => `${key.replace(/_/g, " ")}: ${capabilityText(value)}`),
    ].filter(Boolean).join(" · "),
  }));
  show(el("section", { class: "card" },
    el("h2", { text: "Examination rules" }),
    el("p", { class: "banner", text: "These rules are declared, not enforced by software. Follow them as instructed by your examiner." }),
    el("p", { class: "meta", text: `Integrity mode: ${contract.integrity_mode.replace(/_/g, " ").toLowerCase()} · Version ${contract.version}` }),
    el("table", {}, el("caption", { class: "meta", text: "What you may use" }), el("tbody", {}, rows)),
    exceptions.length ? el("div", {}, el("h3", { text: "Your approved adjustments" }), el("ul", {}, exceptions)) : null,
    el("div", { class: "actions" }, el("button", { type: "button", text: "Back", onclick: () => (location.hash = "#/exams") })),
  ));
}

export async function researchView(examId) {
  const path = `/candidate/examinations/${encodeURIComponent(examId)}/research`;
  const info = await api("GET", path);
  const back = el("button", { type: "button", text: "Back", onclick: () => (location.hash = "#/exams") });
  if (!info.study_linked) {
    show(el("section", { class: "card" }, el("h2", { text: "Research participation" }),
      el("p", { text: "No research study is linked to this examination." }), el("div", { class: "actions" }, back)));
    return;
  }
  const status = info.consent === "OPTED_IN" ? "You have agreed to take part."
    : info.consent === "WITHDRAWN" ? "You have withdrawn." : "You have not decided yet.";
  const choose = async (optIn) => {
    try {
      const result = await api("PUT", path, { opt_in: optIn });
      if (!optIn && result.deletion_pending) say("Withdrawal recorded. Deletion of copied data is pending and will be completed by an administrator.");
      else if (!optIn) say(`Withdrawal recorded. ${result.research_cases_deleted} copied research record(s) deleted.`);
      else say("Thank you. Your participation is recorded.");
      researchView(examId);
    } catch (error) {
      say(error.message, "error");
    }
  };
  show(el("section", { class: "card" },
    el("h2", { text: "Research participation" }),
    el("p", { text: "Taking part is optional and does not affect your marks." }),
    el("p", { text: info.collected }),
    el("p", { class: "meta", text: `Ethics approval reference: ${info.ethics_references.join(", ")}` }),
    el("p", { class: "status", text: status }),
    el("div", { class: "actions" },
      el("button", { type: "button", class: "primary", text: "I agree to take part", disabled: info.consent === "OPTED_IN", onclick: () => choose(true) }),
      el("button", { type: "button", text: "Withdraw", disabled: info.consent !== "OPTED_IN", onclick: () => choose(false) }),
      back),
  ));
}

// ---------- examination session (NFR-08: always show save and submission state) ----------

let leaveGuard = null;

export function clearLeaveGuard() {
  if (leaveGuard) { window.removeEventListener("beforeunload", leaveGuard); leaveGuard = null; }
}

export async function sessionView(sessionId) {
  const view = await api("GET", `/candidate/sessions/${encodeURIComponent(sessionId)}`);
  const submitted = view.status === "SUBMITTED";
  const savers = [];

  const deadlineText = el("span");
  const updateDeadline = () => {
    if (!view.examination.my_ends_at) { deadlineText.textContent = "No end time set."; return; }
    const end = new Date(view.examination.my_ends_at + "Z");
    const minutes = Math.round((end - Date.now()) / 60000);
    deadlineText.textContent = `Ends ${when(view.examination.my_ends_at)}` +
      (minutes > 0 ? ` (about ${minutes} min left)` : " (time is up: you can still submit what you saved)");
  };
  updateDeadline();
  const timer = setInterval(updateDeadline, 30000);

  const questionCards = view.questions.map((question) => {
    const saver = makeSaver(sessionId, question, submitted);
    savers.push(saver);
    return saver.card;
  });

  const submitButton = el("button", {
    type: "button", class: "primary", text: submitted ? "Submitted" : "Submit examination", disabled: submitted,
    onclick: async () => {
      if (!confirm("Submit now? You will not be able to change your answers afterwards.")) return;
      submitButton.disabled = true;
      try {
        await Promise.all(savers.map((saver) => saver.flush()));
        if (savers.some((saver) => saver.hasUnsaved())) {
          say("Some answers are not saved. Resolve the messages above before submitting.", "error");
          submitButton.disabled = false;
          return;
        }
        await api("POST", `/candidate/sessions/${encodeURIComponent(sessionId)}/submit`);
        say("Your examination is submitted.");
        sessionView(sessionId);
      } catch (error) {
        say(error.message, "error");
        submitButton.disabled = false;
      }
    },
  });

  leaveGuard = (event) => {
    if (savers.some((saver) => saver.hasUnsaved())) { event.preventDefault(); event.returnValue = ""; }
  };
  window.addEventListener("beforeunload", leaveGuard);
  window.addEventListener("hashchange", () => clearInterval(timer), { once: true });

  show(el("section", {},
    el("h2", { text: view.examination.title }),
    el("div", { class: "deadline", role: "timer", "aria-live": "off" },
      el("strong", { text: submitted ? `Submitted ${when(view.submitted_at)}` + (view.submission_mode === "AUTO_ON_CLOSE" ? " (automatically, when the examination closed)" : "") : "In progress · " }),
      submitted ? null : deadlineText),
    questionCards,
    el("div", { class: "actions" }, submitButton,
      el("button", { type: "button", text: "Back to my examinations", onclick: () => (location.hash = "#/exams") })),
  ));
}

function makeSaver(sessionId, question, readOnly) {
  const id = `answer-${question.question_id}`;
  let revision = question.response ? question.response.revision : 0;
  let timer = null;
  let inFlight = null;
  let dirty = false;
  let conflict = false;

  const status = el("p", { class: "status", id: `${id}-status`, "aria-live": "polite" });
  const setStatus = (state, text) => { status.dataset.state = state; status.textContent = text; };
  const area = el("textarea", { id, "aria-describedby": `${id}-status`, readonly: readOnly, spellcheck: "false" });
  area.value = question.response ? question.response.content : "";
  if (question.response) setStatus("saved", `Saved ${when(question.response.saved_at)} (revision ${revision})`);
  else setStatus("pending", readOnly ? "No answer saved." : "Not saved yet.");

  const save = async () => {
    if (!dirty || conflict) return;
    dirty = false;
    setStatus("saving", "Saving…");
    try {
      // base_revision makes the server refuse to overwrite a newer save (e.g. another tab).
      const saved = await api("PUT", `/candidate/sessions/${encodeURIComponent(sessionId)}/responses/${encodeURIComponent(question.question_id)}`,
        { content: area.value, base_revision: revision });
      revision = saved.revision;
      setStatus("saved", `Saved ${when(saved.saved_at)} (revision ${revision})`);
    } catch (error) {
      dirty = true;
      if (error.status === 409 && /newer save/i.test(error.message)) {
        conflict = true;
        setStatus("conflict", "Not saved: a newer version was saved elsewhere. Copy your text, then reload this page.");
      } else if (error.status === 409 || error.status === 422) {
        setStatus("error", `Not saved: ${error.message}`);
      } else {
        setStatus("error", "Not saved: connection problem. Retrying…");
        clearTimeout(timer);
        timer = setTimeout(() => { inFlight = save(); }, RETRY_DELAY_MS);
      }
    }
  };

  if (!readOnly) {
    area.addEventListener("input", () => {
      dirty = true;
      setStatus("pending", "Unsaved changes…");
      clearTimeout(timer);
      timer = setTimeout(() => { inFlight = save(); }, AUTOSAVE_DELAY_MS);
    });
    area.addEventListener("blur", () => { clearTimeout(timer); inFlight = save(); });
  }

  const card = el("article", { class: "card" },
    el("h3", { text: `${question.display_order}. ${question.title}` }),
    el("p", { text: question.prompt }),
    el("p", { class: "meta", text: `Language: ${question.language}` }),
    // Distinct accessible names, so a screen reader announces which question this box is for.
    el("label", { for: id, text: `Your answer to question ${question.display_order}` }), area, status);

  return {
    card,
    hasUnsaved: () => dirty,
    flush: async () => { clearTimeout(timer); if (inFlight) await inFlight; await save(); },
  };
}

export async function resultView(examId) {
  const back = el("button", { type: "button", text: "Back", onclick: () => (location.hash = "#/exams") });
  let session;
  try {
    session = await api("GET", `/candidate/examinations/${encodeURIComponent(examId)}/session`);
  } catch (error) {
    show(el("section", { class: "card" }, el("h2", { text: "My result" }), el("p", { text: error.message }), el("div", { class: "actions" }, back)));
    return;
  }
  try {
    const result = await api("GET", `/candidate/sessions/${encodeURIComponent(session.session_id)}/result`);
    const rows = result.questions.map((q) => el("tr", {},
      el("th", { scope: "row", text: q.title }), el("td", { text: `${q.score} / ${q.max_score}` }), el("td", { text: q.comment || "—" })));
    show(el("section", { class: "card" },
      el("h2", { text: "My result" }),
      el("p", { class: "meta", text: `Released ${when(result.released_at)}` }),
      el("p", {}, el("strong", { text: `${result.weighted_percent}%` }), ` (${result.raw_score} / ${result.raw_max} marks)`),
      el("table", {}, el("thead", {}, el("tr", {}, el("th", { text: "Question" }), el("th", { text: "Score" }), el("th", { text: "Comment" }))), el("tbody", {}, rows)),
      el("div", { class: "actions" }, back)));
  } catch (error) {
    const text = error.status === 409 ? "Your result has not been released yet." : error.message;
    show(el("section", { class: "card" }, el("h2", { text: "My result" }), el("p", { text }), el("div", { class: "actions" }, back)));
  }
}

