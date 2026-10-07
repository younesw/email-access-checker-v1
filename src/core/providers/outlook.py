from typing import Any, Dict


def get_gmail_config() -> Dict[str, Any]:
    return {
        "provider": "gmail",
        "imap_host": "imap.gmail.com",
        "imap_port": 993,
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 465,
        "oauth_supported": True,
        "app_password_required": True,
        "notes": "Gmail often requires an app password or modern authentication if 2FA is enabled.",
    }
