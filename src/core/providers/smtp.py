import imaplib
import socket
import time
from typing import Any, Dict


def imap_login_check(email: str, password: str, host: str, port: int = 993, timeout: float = 5.0) -> Dict[str, Any]:
    started = time.time()
    try:
        client = imaplib.IMAP4_SSL(host, port, timeout=timeout)
        client.login(email, password)
        status, data = client.list()
        if status != "OK":
            raise RuntimeError("IMAP LIST failed.")
        client.logout()
        elapsed = round(time.time() - started, 3)
        return {"success": True, "response_time": elapsed, "provider_status": "reachable"}
    except (imaplib.IMAP4.error, socket.timeout, OSError, ValueError) as exc:
        elapsed = round(time.time() - started, 3)
        return {"success": False, "response_time": elapsed, "provider_status": "error", "error": str(exc)}
