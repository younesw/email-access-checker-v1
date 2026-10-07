from typing import Any, Dict


def get_outlook_config() -> Dict[str, Any]:
    return {
        "provider": "outlook",
        "imap_host": "outlook.office365.com",
        "imap_port": 993,
        "smtp_host": "smtp.office365.com",
        "smtp_port": 587,
        "oauth_supported": True,
        "app_password_required": False,
        "notes": "Microsoft 365 accounts may use OAuth2 or app-specific auth flows.",
    }
