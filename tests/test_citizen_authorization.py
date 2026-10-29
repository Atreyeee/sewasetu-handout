from unittest.mock import Mock

from app.app import app


def test_citizen_cannot_view_another_citizens_application(monkeypatch):
    client = app.test_client()

    fake_cursor = Mock()
    fake_cursor.fetchone.return_value = (
        "SSP26123456",
        "Other Citizen",
        "9999999999",
        "1950-01-01",
        "Village",
        "Sonari",
        "1234567890",
        "SBIN0001234",
        "PENDING",
        "2026-10-01 10:00:00",
        None,
    )

    fake_conn = Mock()
    fake_conn.cursor.return_value = fake_cursor

    monkeypatch.setattr("app.app.get_db", lambda: fake_conn)

    with client.session_transaction() as session:
        session["logged_in"] = True
        session["portal_mobile"] = "8888888888"

    response = client.get("/application/1")

    assert response.status_code in (403, 404)