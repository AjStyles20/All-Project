// Scenarios, personas and questions written for this project. Communication practice only:
// nothing here assesses or treats anxiety or any other condition (Pass 001-003 boundary).

export const DEMEANOURS = {
  supportive: { label: "supportive", followUpChance: 0.15, interruptChance: 0.1 },
  neutral: { label: "neutral", followUpChance: 0.3, interruptChance: 0.25 },
  skeptical: { label: "sceptical", followUpChance: 0.7, interruptChance: 0.4 },
  impatient: { label: "impatient", followUpChance: 0.5, interruptChance: 0.7 },
};

export const SCENARIOS = [
  {
    id: "project-defence",
    name: "Final-year project defence",
    talkSeconds: 90,
    answerSeconds: 60,
    personas: [
      { id: "okafor", name: "Dr Okafor", role: "Supervisor", demeanour: "supportive", focus: ["requirements", "design", "testing"] },
      { id: "lindqvist", name: "Prof. Lindqvist", role: "External examiner", demeanour: "skeptical", focus: ["evidence", "evaluation", "limitations"] },
      { id: "mensah", name: "Ms Mensah", role: "Industry assessor", demeanour: "impatient", focus: ["users", "cost", "deployment"] },
    ],
    questions: {
      okafor: ["Which requirement was hardest to meet, and how did you meet it?", "How did you test the part you are most proud of?"],
      lindqvist: ["What evidence shows your system works better than the simplest alternative?", "What is the biggest limitation of your evaluation?",
                  "If your results are wrong, what would be the most likely reason?"],
      mensah: ["Who would actually use this, and why would they switch?", "What would it cost to run for a thousand users?"],
    },
    followUps: {
      skeptical: ["You haven't given a number. Do you have one?", "How do you know that isn't just chance?"],
      impatient: ["In one sentence, please.", "We're short on time. What's the key point?"],
      neutral: ["Can you give an example?"],
      supportive: ["Could you expand on that a little?"],
    },
    interruptions: ["Sorry to cut in: where does the data come from?", "Wait, can you go back to the previous point?",
                    "Quick question before you continue: is that already built?"],
  },
  {
    id: "job-interview",
    name: "Job interview panel",
    talkSeconds: 60,
    answerSeconds: 75,
    personas: [
      { id: "reyes", name: "Ana Reyes", role: "Hiring manager", demeanour: "neutral", focus: ["team", "delivery", "ownership"] },
      { id: "brandt", name: "Tom Brandt", role: "Senior engineer", demeanour: "skeptical", focus: ["technical", "trade-offs", "debugging"] },
    ],
    questions: {
      reyes: ["Tell us about a time a project went off track. What did you do?", "Why this role, and why now?"],
      brandt: ["Describe a bug you could not find for a long time. How did you finally find it?",
               "Tell us about a technical decision you would make differently today."],
    },
    followUps: {
      skeptical: ["What exactly was your part, as opposed to the team's?", "What did you measure to know it worked?"],
      impatient: ["Briefly, please."],
      neutral: ["What did you learn from it?"],
      supportive: ["Take your time. What happened next?"],
    },
    interruptions: ["Sorry, just to check: was that your decision or your manager's?", "Can I stop you there? How big was the team?"],
  },
  {
    id: "pitch",
    name: "Two-minute pitch to investors",
    talkSeconds: 120,
    answerSeconds: 45,
    personas: [
      { id: "achieng", name: "Achieng", role: "Angel investor", demeanour: "impatient", focus: ["market", "traction", "money"] },
      { id: "dubois", name: "Claire Dubois", role: "Fund partner", demeanour: "skeptical", focus: ["competition", "risk", "team"] },
    ],
    questions: {
      achieng: ["How many paying customers do you have today?", "What will you spend the money on first?"],
      dubois: ["Who is your strongest competitor, and why do you win?", "What has to be true for this to fail?"],
    },
    followUps: {
      skeptical: ["That sounds like an assumption. What's the evidence?"],
      impatient: ["Numbers, please.", "Skip to the ask."],
      neutral: ["Go on."],
      supportive: ["Interesting. Say more."],
    },
    interruptions: ["Hold on: is that revenue or sign-ups?", "Sorry, who is paying for this?"],
  },
];

export const FILLERS = ["um", "uh", "erm", "er", "like", "you know", "basically", "sort of", "kind of", "i mean"];

// Observable skill areas (Pass 002 §9). These describe practice targets, not personal traits.
export const SKILLS = {
  start: "Starting answers promptly",
  structure: "Keeping answers within time",
  relevance: "Staying on the question",
  fillers: "Fewer filler words",
  recovery: "Getting back on track after an interruption",
  pushback: "Handling sceptical follow-ups",
};

// Which pressures to add when practising each skill area.
export const DRILLS = {
  start: { name: "Rapid questions", stressors: ["rapid"], tip: "Pause briefly, then lead with your answer in one sentence." },
  structure: { name: "Strict time limit", stressors: ["strict-time"], tip: "Point, reason, example. Then stop." },
  relevance: { name: "Unexpected questions", stressors: ["unexpected"], tip: "Repeat the key words of the question in your first sentence." },
  fillers: { name: "Slow, deliberate answers", stressors: [], tip: "Replace fillers with a short silent pause." },
  recovery: { name: "Frequent interruptions", stressors: ["interrupt"], tip: "Answer the interruption briefly, then say 'Back to my point:' and continue." },
  pushback: { name: "Sceptical panel", stressors: ["skeptical"], tip: "Acknowledge, give one piece of evidence, state the limit." },
};
