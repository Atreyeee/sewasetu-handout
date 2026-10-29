from unittest.mock import Mock

from app.app import generate_acknowledgment, FPDF


def test_acknowledgment_does_not_draw_thousands_of_border_lines(monkeypatch):
    cursor = Mock()
    cursor.fetchone.return_value = (
        "SSP26123456",
        "Test Applicant",
        "9876543210",
        "1950-01-01",
        "Test Village",
        "Sonari",
        "1234567890",
        "SBIN0001234",
        "2026-10-01 10:00:00",
        "PENDING",
    )

    calls = {"count": 0}

    original_line = FPDF.line

    def counting_line(self, *args, **kwargs):
        calls["count"] += 1
        return original_line(self, *args, **kwargs)

    monkeypatch.setattr(FPDF, "line", counting_line)

    generate_acknowledgment(cursor, 1)

    assert calls["count"] <= 4