import smtplib
import socket
import time
from typing import Any, Dict


def smtp_login_check(email: str, password: str, host: str, port: int = 465, timeout: float = 5.0) -> Dict[str, Any]:
    started = time.time()
    try:
        server = smtplib.SMTP_SSL(host, port, timeout=timeout)
        server.login(email, password)
        server.close()
        elapsed = round(time.time() - started, 3)
        return {"success": True, "response_time": elapsed, "provider_status": "reachable"}
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPException, socket.timeout, OSError, ValueError) as exc:
        elapsed = round(time.time() - started, 3)
        return {"success": False, "response_time": elapsed, "provider_status": "error", "error": str(exc)}
