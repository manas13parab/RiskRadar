import re

from backend import config
from backend.security import default_student_password, hash_password, verify_password
from backend.utils import days_ago_str, today_str


def test_password_is_hashed_and_verifiable():
    hashed = hash_password("secret123")
    assert hashed != "secret123" and "secret123" not in hashed
    assert verify_password(hashed, "secret123") is True
    assert verify_password(hashed, "Secret123") is False


def test_same_password_gives_different_hashes():
    assert hash_password("abc12345") != hash_password("abc12345")


def test_default_student_password():
    assert default_student_password("Omar", "S1000") == "omar@1000"
    assert default_student_password("MARIA", "S1001") == "maria@1001"


def test_dates_use_the_configured_format():
    assert re.fullmatch(r"[A-Z][a-z]{2} \d{2}, \d{4}", today_str())
    assert today_str() == days_ago_str(0)
    assert days_ago_str(5) != today_str()
    assert config.DATE_FORMAT == "%b %d, %Y"
