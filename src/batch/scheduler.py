import concurrent.futures
import time
from dataclasses import dataclass
from threading import Lock
from typing import Any, Dict, Iterable, List

from src.core.email_checker import check_email


@dataclass
class RateLimiter:
    calls_per_minute: int = 60
    _interval: float = 60.0
    _lock: Lock = Lock()
    _last_access: float = 0.0
    _count: int = 0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            if self._count >= self.calls_per_minute:
                elapsed = now - self._last_access
                if elapsed < self._interval:
                    time.sleep(self._interval - elapsed)
                self._count = 0
                self._last_access = time.monotonic()
            else:
                self._last_access = now
            self._count += 1


def batch_check(accounts: Iterable[Dict[str, str]], max_workers: int = 6, rate_limit_per_minute: int = 60) -> Dict[str, Any]:
    items = list(accounts)
    limiter = RateLimiter(calls_per_minute=rate_limit_per_minute)
    results: List[Dict[str, Any]] = []

    def worker(account: Dict[str, str]) -> Dict[str, Any]:
        limiter.wait()
        email = account.get("email") or account.get("Email")
        password = account.get("password") or account.get("Password")
        if not email or not password:
            return {"email": email, "status": "error", "error": "Missing email or password."}
        result = check_email(email, password)
        result["submitted_at"] = time.time()
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, item) for item in items]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    summary = {
        "total": len(results),
        "success": sum(1 for r in results if r.get("status") == "active"),
        "failed": sum(1 for r in results if r.get("status") not in {"active", "invalid"}),
        "invalid": sum(1 for r in results if r.get("status") == "invalid"),
    }
    return {"results": results, "summary": summary, "processed_at": time.time()}
