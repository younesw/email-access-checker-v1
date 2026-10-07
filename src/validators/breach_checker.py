from typing import Any, Dict


def summarize_security(provider: str | None, smtp_working: bool, imap_working: bool, tfa_hint: str | None = None) -> Dict[str, Any]:
    security = {
        "provider": provider,
        "smtp_working": smtp_working,
        "imap_working": imap_working,
        "tfa_recommended": True,
        "notes": [],
    }

    if provider == "gmail":
        security["notes"].append("Google may require an app password when 2FA is enabled.")
    elif provider == "outlook":
        security["notes"].append("Microsoft accounts often require app-password or modern auth support.")
    elif provider == "yahoo":
        security["notes"].append("Yahoo may require app passwords or account-specific settings.")
    elif provider == "protonmail":
        security["notes"].append("ProtonMail may require secure bridge or app-specific credentials.")
    elif provider == "custom":
        security["notes"].append("Custom IMAP providers may require authenticated SMTP settings and TLS configuration.")

    if tfa_hint:
        security["notes"].append(tfa_hint)

    if not smtp_working and not imap_working:
        security["notes"].append("No working mail protocol was confirmed for this account.")

    return security
