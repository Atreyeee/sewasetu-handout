from unittest.mock import Mock

from app.app import app


def test_pending_citizen_can_open_correction_page(monkeypatch):
    client = app.test_client()

    fake_cursor = Mock()
    fake_cursor.fetchone.return_value = (
        "SSP26123456",
        "Original Name",
        "9876543210",
        "1950-01-01",
        "Male",
        "Married",
        "",
        "",
        "Village",
        "Sonari",
        "1234567890",
        "SBIN0001234",
        "PENDING",
    )

    fake_conn = Mock()
    fake_conn.cursor.return_value = fake_cursor

    monkeypatch.setattr("app.app.get_db", lambda: fake_conn)

    with client.session_transaction() as session:
        session["logged_in"] = True
        session["portal_mobile"] = "9876543210"

    response = client.get("/application/1/edit")

    assert response.status_code == 200