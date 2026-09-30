from unittest.mock import patch

from cachyos_update_reminder.app import should_show_autostart_reminder


def test_autostart_with_updates():
    with patch(
        "cachyos_update_reminder.app.check_updates",
        return_value=["update"],
    ):
        assert should_show_autostart_reminder() is True


def test_autostart_without_updates():
    with patch(
        "cachyos_update_reminder.app.check_updates",
        return_value=[],
    ):
        assert should_show_autostart_reminder() is False


def test_autostart_with_error():
    with patch(
        "cachyos_update_reminder.app.check_updates",
        side_effect=Exception("Testfehler"),
    ):
        assert should_show_autostart_reminder() is False