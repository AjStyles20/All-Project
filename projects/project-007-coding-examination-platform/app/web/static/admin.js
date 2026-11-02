// Administrator screens: research (FD-06, DR-015, DR-016) and users (FD-07).
import { api, el, say, show, when, words } from "./core.js";

const part = encodeURIComponent;
const ROLES = ["CANDIDATE", "EXAMINER", "ADMINISTRATOR", "INDEPENDENT_ASSESSOR"];

function textField(id, label, extra = {}, hint) {
  const input = el("input", { id, type: "text", ...extra });
  return { input, node: el("div", {}, el("label", { for: id, text: label }), input, hint ? el("p", { class: "meta", text: hint }) : null) };
}

export async function adminHome() {
  const exams = await api("GET", "/admin/examinations");
  show(el("section", {},
    el("h2", { text: "Research administration" }),
    exams.length ? exams.map((exam) => el("article", { class: "card" },
      el("h3", { text: exam.title }),
      el("p", { class: "meta" }, el("span", { class: "badge", text: exam.status })),
      el("div", { class: "actions" }, el("button", { type: "button", class: "primary", text: "Open research settings",
        "aria-label": `Open research settings for ${exam.title}`,
        onclick: () => { location.hash = `#/admin/exam/${part(exam.examination_id)}`; } })),
    )) : el("p", { class: "card", text: "There are no examinations yet." })));
}

function oneTimePasswordCard(username, password) {
  // Shown once: only the hash is stored, so it cannot be displayed again.
  return el("div", { class: "card banner", role: "alert" },
    el("h3", { text: `One-time password for ${username}` }),
    el("p", {}, el("code", { text: password })),
    el("p", { class: "meta", text: "Copy it now and give it to the user privately. It will not be shown again, and they must change it at first sign-in." }));
}

export async function usersView(banner) {
  const users = await api("GET", "/admin/users");
  const username = textField("new-user-name", "Username", { required: true, maxlength: 100, autocomplete: "off" });
  const display = textField("new-user-display", "Display name", { required: true, maxlength: 150, autocomplete: "off" });
  const roleBoxes = ROLES.map((role) => ({ role, box: el("input", { id: `new-role-${role}`, type: "checkbox" }) }));
  const reload = (next) => usersView(next);
  const act = async (run) => { try { await run(); } catch (error) { say(error.message, "error"); } };
  const editRoles = (user) => {
    const boxes = ROLES.map((role) => {
      const box = el("input", { id: `role-${user.user_id}-${role}`, type: "checkbox" });
      box.checked = user.roles.includes(role);
      return { role, box };
    });
    return el("details", {}, el("summary", { text: "Roles" }),
      boxes.map(({ role, box }) => el("label", { class: "check", for: box.id }, box, ` ${words(role)}`)),
      el("button", { type: "button", text: "Save roles", "aria-label": `Save roles for ${user.username}`, onclick: () => act(async () => {
        await api("PUT", `/admin/users/${part(user.user_id)}/roles`, { roles: boxes.filter((b) => b.box.checked).map((b) => b.role) });
        say("Roles saved. They apply from the user's next request.");
        reload();
      }) }));
  };
  show(el("section", {},
    el("h2", { text: "Users" }),
    banner || null,
    el("form", { class: "card", onsubmit: (event) => {
      event.preventDefault();
      act(async () => {
        const created = await api("POST", "/admin/users", { username: username.input.value, display_name: display.input.value,
          roles: roleBoxes.filter((r) => r.box.checked).map((r) => r.role) });
        say(`Account ${created.username} created.`);
        reload(oneTimePasswordCard(created.username, created.one_time_password));
      });
    } },
      el("h3", { text: "New user" }), username.node, display.node,
      el("fieldset", {}, el("legend", { text: "Roles" }),
        roleBoxes.map(({ role, box }) => el("label", { class: "check", for: box.id }, box, ` ${words(role)}`))),
      el("div", { class: "actions" }, el("button", { type: "submit", class: "primary", text: "Create user" }))),
    users.map((user) => el("article", { class: "card" },
      el("h3", { text: `${user.display_name} (${user.username})` }),
      el("p", { class: "meta", text: `${user.roles.map(words).join(", ")} · ${user.is_active ? "active" : "deactivated"}${user.must_change_password ? " · has not chosen a password yet" : ""}` }),
      editRoles(user),
      el("div", { class: "actions" },
        el("button", { type: "button", text: user.is_active ? "Deactivate" : "Reactivate",
          "aria-label": `${user.is_active ? "Deactivate" : "Reactivate"} ${user.username}`, onclick: () => act(async () => {
            await api("PATCH", `/admin/users/${part(user.user_id)}/active`, { active: !user.is_active });
            say(`${user.username} ${user.is_active ? "deactivated and signed out" : "reactivated"}.`);
            reload();
          }) }),
        el("button", { type: "button", text: "Clear sign-in lock", "aria-label": `Clear sign-in lock for ${user.username}`, onclick: () => act(async () => {
          const result = await api("POST", `/admin/users/${part(user.user_id)}/clear-login-lock`);
          say(result.cleared ? `Sign-in lock cleared for ${user.username}.` : `${user.username} had no sign-in lock.`);
        }) }),
        el("button", { type: "button", text: "Reset password", "aria-label": `Reset password for ${user.username}`, onclick: () => act(async () => {
          if (!confirm(`Reset the password for ${user.username}? They will be signed out.`)) return;
          const result = await api("POST", `/admin/users/${part(user.user_id)}/password-reset`);
          reload(oneTimePasswordCard(user.username, result.one_time_password));
        }) })),
    )),
  ));
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

export async function auditView() {
  const events = await api("GET", "/admin/audit");
  show(el("section", {},
    el("h2", { text: "Account audit trail" }),
    el("p", { class: "meta", text: "Newest first. Passwords are never recorded." }),
    el("div", { class: "card" }, events.length ? el("table", {},
      el("thead", {}, el("tr", {}, ["When", "Action", "Account", "By", "Detail"].map((h) => el("th", { text: h })))),
      el("tbody", {}, events.map((e) => el("tr", {},
        el("td", { text: when(e.occurred_at) }), el("td", { text: words(e.action) }), el("td", { text: e.target_username }),
        el("td", { text: e.actor_user_id || "system" }),
        el("td", { text: Object.entries(e.detail).map(([k, v]) => `${words(k)}: ${Array.isArray(v) ? v.join(", ") : v}`).join("; ") || "—" })))))
      : el("p", { class: "meta", text: "No account changes recorded yet." }))));
}
