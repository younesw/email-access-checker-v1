from src.batch.processor import batch_check


def test_batch_check_success(monkeypatch):
    def fake_check_email(email: str, password: str):
        return {"email": email, "status": "active", "provider": "gmail", "details": {"2fa_enabled": False}}

    monkeypatch.setattr("src.batch.processor.check_email", fake_check_email)
    payload = [{"email": "a@gmail.com", "password": "123"}, {"email": "b@gmail.com", "password": "456"}]
    result = batch_check(payload, max_workers=2, rate_limit_per_minute=100)
    assert result["summary"]["total"] == 2
    assert result["summary"]["success"] == 2
