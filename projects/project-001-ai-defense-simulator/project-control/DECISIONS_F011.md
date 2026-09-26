# Feature 011 Decision Note

## Decision
Integrate existing verified capabilities into a coherent rehearsal workflow without adding authentication, public deployment, objective grading, new provider privileges, or additional AI modalities.

## Authority
A2 significant implementation/UI integration within the already approved Project 001 architecture and scope.

## Rationale
The backend capabilities for grounded questioning, qualitative evaluation, bounded multi-turn follow-up, speech input, and reviewer speech output already exist. The highest-value next step is product integration and truthful terminal-state handling rather than adding another modality.

## Security consequence
Session/question association must be independently verified server-side, and a completed/exhausted session must not create another question even if a client tampers with navigation or invokes the follow-up endpoint directly.
