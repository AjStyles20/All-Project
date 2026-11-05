"""PGAIC mastery kernel: attempts, assistance, mastery states and Knowledge Issues.

Task outcome and mastery are separate variables (Pass 017 §9). Help above L2 makes success
"assisted"; only an unassisted verification attempt, after earlier evidence, can make
mastery INDEPENDENT, and a later unassisted failure reopens it. Accessibility support is
stored apart from cognitive help and never lowers mastery (PGAIC-R04).
"""
import itertools
from dataclasses import dataclass, field

from p002.domain import Assistance, IssueState, Mastery, PolicyError

LIGHT_HELP_MAX = Assistance.L2_CONCEPTUAL_CUE   # up to a cue: assisted evidence, may be provisional
VERIFY_MAX = Assistance.L0_NONE                 # verification attempts must be unassisted


@dataclass
class Attempt:
    id: str
    learner: str
    concept: str
    task: str
    correct: bool
    assistance: Assistance
    accommodation: str | None = None
    verification: bool = False
    reasoning_ok: bool | None = None   # None when reasoning was not collected
    escalations: list = field(default_factory=list)


@dataclass
class State:
    mastery: Mastery = Mastery.UNKNOWN
    reasons: list = field(default_factory=list)
    evidence: list = field(default_factory=list)


@dataclass
class Issue:
    id: str
    learner: str
    concept: str
    description: str
    state: IssueState = IssueState.OPEN
    history: list = field(default_factory=list)
    reopen_count: int = 0


class MasteryKernel:
    def __init__(self, contract=True):
        # contract=False is baseline B3: an ordinary adaptive tutor that counts correct
        # answers as mastery whatever help was given.
        self.contract = contract
        self.attempts, self.states, self.issues = {}, {}, {}
        self._ids = itertools.count(1)

    def state(self, learner, concept) -> State:
        return self.states.setdefault((learner, concept), State())

    def escalate(self, attempt_help: list, to: Assistance, reason: str):
        """Help may only go up one level at a time, with a recorded reason (PGAIC-R02)."""
        current = attempt_help[-1][0] if attempt_help else Assistance.L0_NONE
        if to < current:
            raise PolicyError("Help can only be increased during an attempt.")
        if to > current + 1:
            raise PolicyError("Help goes up one level at a time.")
        if not reason:
            raise PolicyError("Each increase in help needs a reason.")
        attempt_help.append((Assistance(to), reason))

    def record(self, learner, concept, task, correct, help_steps=(), accommodation=None,
               verification=False, reasoning_ok=None) -> Attempt:
        level = max([Assistance(h[0]) for h in help_steps], default=Assistance.L0_NONE)
        if verification and level > VERIFY_MAX:
            raise PolicyError("A verification attempt must be done without help.")
        a = Attempt(f"T{next(self._ids)}", learner, concept, task, bool(correct), level, accommodation,
                    verification, reasoning_ok, list(help_steps))
        self.attempts[a.id] = a
        self._update(a)
        self.on_mastery_change(learner, concept)
        return a

    def _update(self, a: Attempt):
        s = self.state(a.learner, a.concept)
        s.evidence.append(a.id)
        if not self.contract:
            # B3: three correct answers in a row is "mastered", help or not.
            recent = [self.attempts[i].correct for i in s.evidence if self.attempts[i].concept == a.concept][-3:]
            s.mastery = Mastery.INDEPENDENT if len(recent) == 3 and all(recent) else Mastery.PROVISIONAL
            s.reasons = ["counted correct answers"]
            return
        near_miss = a.correct and a.reasoning_ok is False
        help_note = f"help level L{int(a.assistance)}" + (f", accommodation: {a.accommodation}" if a.accommodation else "")
        if a.verification:
            if a.correct and not near_miss and s.mastery in (Mastery.PROVISIONAL, Mastery.VERIFYING,
                                                             Mastery.ASSISTED_SUCCESS, Mastery.REOPENED, Mastery.INDEPENDENT):
                s.mastery, s.reasons = Mastery.INDEPENDENT, [f"{a.id}: correct without help in a verification check"]
            elif a.correct and not near_miss:
                s.mastery, s.reasons = Mastery.PROVISIONAL, [f"{a.id}: correct check, but no earlier evidence yet"]
            else:
                was = s.mastery
                s.mastery = Mastery.REOPENED if was in (Mastery.INDEPENDENT, Mastery.PROVISIONAL, Mastery.VERIFYING,
                                                        Mastery.ASSISTED_SUCCESS) else Mastery.UNKNOWN
                s.reasons = [f"{a.id}: verification without help {'had faulty reasoning' if near_miss else 'failed'}"
                             + (f" (was {was.value})" if was is not Mastery.UNKNOWN else "")]
            return
        if near_miss:
            s.mastery = Mastery.VERIFYING
            s.reasons = [f"{a.id}: right answer with faulty reasoning (near miss); needs a check without help"]
        elif a.correct and a.assistance > LIGHT_HELP_MAX:
            if s.mastery is not Mastery.INDEPENDENT:
                s.mastery = Mastery.ASSISTED_SUCCESS
            s.reasons = [f"{a.id}: correct with {help_note}: task success, not independent mastery"]
        elif a.correct and a.assistance > Assistance.L0_NONE:
            if s.mastery is not Mastery.INDEPENDENT:
                s.mastery = Mastery.PROVISIONAL
            s.reasons = [f"{a.id}: correct with light help ({help_note}); provisional until checked without help"]
        elif a.correct:
            if s.mastery is not Mastery.INDEPENDENT:
                s.mastery = Mastery.VERIFYING
            s.reasons = [f"{a.id}: correct without help; a later check without help confirms it"]
        else:
            if s.mastery is Mastery.INDEPENDENT:
                s.mastery = Mastery.REOPENED
            s.reasons = [f"{a.id}: incorrect with {help_note}"]

    def needs_verification(self, learner, concept) -> bool:
        return self.contract and self.state(learner, concept).mastery in (
            Mastery.ASSISTED_SUCCESS, Mastery.PROVISIONAL, Mastery.VERIFYING, Mastery.REOPENED)

    # ---------- Knowledge Issues ----------

    def open_issue(self, learner, concept, description) -> Issue:
        i = Issue(f"K{next(self._ids)}", learner, concept, description)
        i.history.append("opened")
        self.issues[i.id] = i
        return i

    def move_issue(self, issue_id, to: IssueState, note=""):
        i = self.issues[issue_id]
        allowed = {IssueState.OPEN: {IssueState.WORKING}, IssueState.WORKING: {IssueState.VERIFYING},
                   IssueState.VERIFYING: {IssueState.RESOLVED, IssueState.WORKING},
                   IssueState.RESOLVED: {IssueState.REOPENED}, IssueState.REOPENED: {IssueState.WORKING}}
        if to not in allowed[i.state]:
            raise PolicyError(f"An issue cannot go from {i.state.value} to {to.value}.")
        if to is IssueState.RESOLVED and self.state(i.learner, i.concept).mastery is not Mastery.INDEPENDENT:
            raise PolicyError("Resolving needs independent evidence, not just an explanation (C03).")
        if to is IssueState.REOPENED:
            i.reopen_count += 1
        i.state = to
        i.history.append(f"{to.value}: {note}" if note else to.value)

    def on_mastery_change(self, learner, concept):
        """Reopen resolved issues for this concept when mastery is reopened (B10)."""
        if self.state(learner, concept).mastery is Mastery.REOPENED:
            for i in self.issues.values():
                if i.learner == learner and i.concept == concept and i.state is IssueState.RESOLVED:
                    self.move_issue(i.id, IssueState.REOPENED, "later check without help failed")
