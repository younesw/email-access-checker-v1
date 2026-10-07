from __future__ import annotations

import time
from typing import Any, Dict, List, Iterable

from src.core.providers.gmail import get_gmail_config
from src.core.providers.imap import imap_login_check
from src.core.providers.outlook import get_outlook_config
from src.core.providers.smtp import smtp_login_check
from src.utils.config import get_settings
from src.utils.encryption import mask_secret
from src.utils.logging import get_logger
from src.validators.email_format import validate_email_format
from src.validators.security_checker import summarize_security

logger = get_logger(__name__)


def detect_provider(email: str) -> str:
    normalized = (email or "").lower().strip()
    if "@" not in normalized:
        return "unknown"
    domain = normalized.split("@", 1)[1]
    if domain.endswith("gmail.com"):
        return "gmail"
    if domain.endswith(("outlook.com", "hotmail.com", "live.com", "msn.com")):
        return "outlook"
    if domain.endswith(("yahoo.com", "yahoo.co.uk")):
        return "yahoo"
    if domain.endswith(("protonmail.com", "proton.me")):
        return "protonmail"
    return "custom"


def check_email(email: str, password: str) -> Dict[str, Any]:
    started = time.monotonic()
    validation = validate_email_format(email)
    provider = detect_provider(email)
    masked_password = mask_secret(password)
    logger.info("Checking account for %s provider=%s", mask_secret(email), provider)

    result: Dict[str, Any] = {
        "email": validation.get("normalized_email") or email.strip().lower(),
        "provider": provider,
        "is_valid_format": False,
        "is_authenticated": False,
        "is_accessible": False,
        "status": "invalid",
        "error": "",
        "details": {
            "unread_count": 0,
            "total_messages": 0,
            "smtp_working": False,
            "imap_working": False,
            "2fa_enabled": False,
            "storage_used": 0,
            "last_login": None,
            "account_type": "unknown",
            "response_time": 0.0,
            "provider_status": "not_tested",
        },
    }

    if not validation.get("valid"):
        result["error"] = validation.get("error", "Invalid email format")
        result["status"] = "invalid"
        result["details"]["response_time"] = round(time.monotonic() - started, 3)
        logger.warning("Invalid email check attempted for %s", mask_secret(email))
        return result

    result["is_valid_format"] = True
    result["provider"] = validation.get("provider") or provider

    if not password:
        result["error"] = "Password is required."
        result["status"] = "error"
        result["details"]["response_time"] = round(time.monotonic() - started, 3)
        return result

    try:
        config = get_gmail_config() if provider == "gmail" else get_outlook_config() if provider == "outlook" else {"imap_host": "custom.imap.example", "imap_port": 993, "smtp_host": "custom.smtp.example", "smtp_port": 465}
        domain = (email or "").split("@")[-1].lower()
        imap_host = config.get("imap_host", f"imap.{domain}")
        smtp_host = config.get("smtp_host", f"smtp.{domain}")

        imap_result = imap_login_check(email, password, imap_host, int(config.get("imap_port", 993)), timeout=get_settings().request_timeout_seconds)
        smtp_result = smtp_login_check(email, password, smtp_host, int(config.get("smtp_port", 465)), timeout=get_settings().request_timeout_seconds)

        result["details"]["imap_working"] = bool(imap_result.get("success"))
        result["details"]["smtp_working"] = bool(smtp_result.get("success"))
        result["details"]["response_time"] = round(max(imap_result.get("response_time", 0.0), smtp_result.get("response_time", 0.0)), 3)
        result["details"]["provider_status"] = "reachable" if imap_result.get("success") or smtp_result.get("success") else "error"

        if not imap_result.get("success") and not smtp_result.get("success"):
            result["status"] = "error"
            result["error"] = smtp_result.get("error") or imap_result.get("error") or "Unable to validate credentials or connection."
            result["details"]["2fa_enabled"] = "password" in str(result["error"]).lower() or "2fa" in str(result["error"]).lower()
            return result

        result["is_authenticated"] = True
        result["is_accessible"] = True
        result["status"] = "active"
        result["details"]["account_type"] = "mail_account"
        result["details"]["2fa_enabled"] = False
        result["details"]["security"] = summarize_security(provider, smtp_result.get("success"), imap_result.get("success"))
        result["details"]["provider_status"] = "active"

    except Exception as exc:
        logger.exception("Unexpected error while checking email %s", mask_secret(email))
        result["status"] = "error"
        result["error"] = f"Unexpected problem during validation: {exc}"
        result["details"]["provider_status"] = "error"

    result["details"]["response_time"] = round(time.monotonic() - started, 3)
    if password:
        result["password_redacted"] = True
    return result


def batch_check(accounts: Iterable[Dict[str, str]], max_workers: int | None = None, rate_limit_per_minute: int | None = None) -> Dict[str, Any]:
    from src.batch.processor import batch_check as processor_batch_check

    return processor_batch_check(
        list(accounts),
        max_workers=max_workers or get_settings().max_workers,
        rate_limit_per_minute=rate_limit_per_minute or get_settings().rate_limit_per_minute,
    )
