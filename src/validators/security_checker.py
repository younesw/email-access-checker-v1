import re
from typing import Any, Dict

from email_validator import EmailNotValidError, validate_email

EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$")


def validate_email_format(email: str) -> Dict[str, Any]:
    normalized = (email or "").strip().lower()
    if not normalized:
        return {"valid": False, "provider": None, "error": "Email is required."}

    try:
        validated = validate_email(normalized, check_deliverability=False)
        candidate = validated.email
    except EmailNotValidError as exc:
        return {"valid": False, "provider": None, "error": f"Invalid email format: {exc}"}

    domain = candidate.split("@")[-1].lower()
    provider = None
    if domain.endswith("gmail.com"):
        provider = "gmail"
    elif domain.endswith("outlook.com") or domain.endswith("hotmail.com") or domain.endswith("live.com") or domain.endswith("msn.com"):
        provider = "outlook"
    elif domain.endswith("yahoo.com") or domain.endswith("yahoo.co.uk"):
        provider = "yahoo"
    elif domain.endswith("protonmail.com") or domain.endswith("proton.me"):
        provider = "protonmail"
    elif "." in domain:
        provider = "custom"

    return {"valid": bool(EMAIL_RE.match(candidate)), "provider": provider, "normalized_email": candidate, "domain": domain}
