from pathlib import Path
import importlib.util


def load_scheduler():
    path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "scripts"
        / "deemed_approval.py"
    )

    spec = importlib.util.spec_from_file_location(
        "deemed_approval",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_deemed_approval_scheduler_loads_existing_app_config():
    scheduler = load_scheduler()

    assert scheduler.SLA_DAYS == 15
    assert scheduler.CONFIG_PATH.endswith("config/app.ini")


def test_overdue_cutoff_is_15_days():
    scheduler = load_scheduler()

    from datetime import datetime

    now = datetime(2026, 10, 29, 12, 0, 0)

    assert scheduler.get_cutoff(now) == datetime(
        2026, 10, 14, 12, 0, 0
    )