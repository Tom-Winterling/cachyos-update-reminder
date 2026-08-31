from cachyos_update_reminder.checker import parse_updates
from cachyos_update_reminder.checker import check_updates, parse_updates


def test_parse_single_update():
    output = "firefox 154.0-1.1 -> 154.0.1-1.1"

    updates = parse_updates(output)

    assert len(updates) == 1
    assert updates[0].name == "firefox"
    assert updates[0].old_version == "154.0-1.1"
    assert updates[0].new_version == "154.0.1-1.1"

def test_parse_multiple_updates():
    output = """\
bubblewrap 0.11.2-1.1 -> 0.12.0-1.1
code 1.131.0-2.1 -> 1.134.0-1.1
firefox 154.0-1.1 -> 154.0.1-1.1
openssl 3.6.3-1.1 -> 3.6.4-1.1
"""

    updates = parse_updates(output)

    assert len(updates) == 4

    assert updates[0].name == "bubblewrap"
    assert updates[1].name == "code"
    assert updates[2].name == "firefox"
    assert updates[3].name == "openssl"    

def test_check_updates(monkeypatch):
    class FakeResult:
        returncode = 0
        stdout = "firefox 154.0-1.1 -> 154.0.1-1.1\n"
        stderr = ""

    def fake_run(*args, **kwargs):
        assert args[0] == ["checkupdates"]
        return FakeResult()

    monkeypatch.setattr(
        "cachyos_update_reminder.checker.subprocess.run",
        fake_run,
    )

    updates = check_updates()

    assert len(updates) == 1
    assert updates[0].name == "firefox"