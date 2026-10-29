from unittest.mock import Mock

from app.app import app

from unittest.mock import Mock
from app.app import app


def test_citizen_cannot_view_another_citizens_application(monkeypatch):
    client = app.test_client()

    fake_cursor = Mock()

    # Simulate PostgreSQL returning no row because the
    # application does not belong to the logged-in citizen.
    fake_cursor.fetchone.return_value = None

    fake_conn = Mock()
    fake_conn.cursor.return_value = fake_cursor

    monkeypatch.setattr(
        "app.app.get_db",
        lambda: fake_conn
    )

    with client.session_transaction() as session:
        session["logged_in"] = True
        session["portal_mobile"] = "8888888888"

    response = client.get("/application/1")

    assert response.status_code == 404

    execute_call = fake_cursor.execute.call_args

    assert execute_call is not None

    sql = execute_call.args[0]
    params = execute_call.args[1]

    assert "WHERE id = %s AND mobile = %s" in sql
    assert params == (1, "8888888888")
def test_citizen_cannot_download_another_citizens_acknowledgment(
    monkeypatch,
    tmp_path,
):
    client = app.test_client()

    fake_cursor = Mock()
    fake_cursor.fetchone.return_value = None

    fake_conn = Mock()
    fake_conn.cursor.return_value = fake_cursor

    monkeypatch.setattr(
        "app.app.get_db",
        lambda: fake_conn
    )

    with client.session_transaction() as session:
        session["logged_in"] = True
        session["portal_mobile"] = "8888888888"

    response = client.get("/ack/1.pdf")

    assert response.status_code in (403, 404)