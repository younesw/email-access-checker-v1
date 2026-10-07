from src.validators.email_format import validate_email_format


def test_validate_email_format_success():
    result = validate_email_format("user@gmail.com")
    assert result["valid"] is True
    assert result["provider"] == "gmail"


def test_validate_email_format_fail():
    result = validate_email_format("bad-email")
    assert result["valid"] is False
