import pytest

from providers import PROVIDERS, validate_registry


def test_real_registry_is_valid():
    validate_registry(PROVIDERS)


def test_broken_registry_lists_every_problem():
    broken = {
        "ok": {"base_url": "https://x", "api_key_env": "X_KEY"},
        "no_key": {"base_url": "https://y"},
        "empty": {},
    }
    with pytest.raises(ValueError) as exc:
        validate_registry(broken)

    msg = str(exc.value)
    assert "no_key: missing 'api_key_env'" in msg
    assert "empty: missing 'base_url'" in msg
    assert "empty: missing 'api_key_env'" in msg
    assert "ok:" not in msg
