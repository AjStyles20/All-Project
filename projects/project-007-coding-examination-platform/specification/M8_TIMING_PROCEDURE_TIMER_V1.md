# P001 M8 Verification Timing Procedure — TIMER-v1

Status: constructed dry-run candidate.

Start timing when the complete verification question is presented and available to read. Stop when the respondent submits/finalizes the answer. If correction is permitted before final submission, timing continues through the correction.

Record elapsed wall-clock seconds as verification_seconds, actual question_count separately, and one LOW/MEDIUM/HIGH complexity category per administered question.

If timing fails after a question was administered, record verification_seconds as missing (None in software) and create a MISSING_TIMING deviation. Never substitute zero. Zero seconds is valid only when no verification occurred and question_count is zero.

Unexpected interruptions that materially affect elapsed time are protocol deviations. Preserve raw time if available and flag the affected time-burden analysis rather than silently editing it.

Use the same start/stop rule for B2 fixed-viva and B4 targeted verification. This standardizes timing; it does not make their question allocation equivalent.
