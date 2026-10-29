from app.app import sanitize


def test_indian_language_name_is_not_truncated():
    name = "অসমীয়া নাম"

    assert sanitize(name, maxlen=20) == name