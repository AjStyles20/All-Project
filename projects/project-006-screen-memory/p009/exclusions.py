"""Windows that are never captured (docs/PRIVACY_SECURITY_MODEL.md §2.4).

Checked before an image is taken. Matching is case-insensitive; title words match whole
words or phrases so that, for example, "Login" matches but "Blogging" does not.
"""
import re

EXCLUDED_PROGRAMS = {
    "keepass.exe", "keepassxc.exe", "1password.exe", "bitwarden.exe", "lastpass.exe", "dashlane.exe",
    "credentialuibroker.exe", "securityhealthhost.exe", "securityhealthsystray.exe", "consent.exe",
    "logonui.exe", "lockapp.exe",
}

EXCLUDED_TITLE_WORDS = (
    "inprivate", "incognito", "private browsing", "password", "passwords", "sign in", "sign-in", "log in",
    "login", "bank", "banking", "paypal", "credit card",
)


def _pattern(words):
    return re.compile(r"(?<![a-z0-9])(" + "|".join(re.escape(w) for w in words) + r")(?![a-z0-9])", re.IGNORECASE)


class Exclusions:
    def __init__(self, extra_programs=(), extra_title_words=()):
        self.programs = EXCLUDED_PROGRAMS | {p.lower() for p in extra_programs}
        self.title_pattern = _pattern(EXCLUDED_TITLE_WORDS + tuple(w.lower() for w in extra_title_words))

    def excluded(self, program: str, title: str) -> bool:
        return program.lower() in self.programs or bool(self.title_pattern.search(title or ""))
