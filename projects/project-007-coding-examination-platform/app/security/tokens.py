import hashlib
import secrets

def issue_token() -> tuple[str, str]:
    raw = secrets.token_urlsafe(32)
    return raw, token_digest(raw)

def token_digest(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()
