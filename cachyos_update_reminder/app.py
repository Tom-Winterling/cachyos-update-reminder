import sys

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from cachyos_update_reminder.checker import check_updates


class UpdateCheckerThread(QThread):
    updates_ready = Signal(object)
    error_occurred = Signal(str)

    def run(self):
        try:
            updates = check_updates()
            self.updates_ready.emit(updates)
        except Exception as error:
            self.error_occurred.emit(str(error))


class UpdateReminderWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CachyOS Update Reminder")
        self.resize(600, 350)

        self.title_label = QLabel("CachyOS Update Reminder")
        self.title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        self.update_label = QLabel("Prüfe auf Updates...")
        self.update_label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 6px;
            }
            """
        )     

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(3)
        self.update_table.setHorizontalHeaderLabels(
            ["Paket", "Installiert", "Verfügbar"]
        )

        self.update_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.update_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.update_table.horizontalHeader().setStretchLastSection(True)

        self.check_button = QPushButton("Jetzt prüfen")
        self.check_button.setMinimumHeight(36)
        self.check_button.clicked.connect(self.check_for_updates)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(self.title_label)
        layout.addWidget(self.update_label)
        layout.addWidget(self.update_table)
        layout.addWidget(self.check_button)

        self.setLayout(layout)
        self.setStyleSheet(
            """
            QWidget {
                font-size: 14px;
            }

            QLabel {
                padding: 4px;
            }

            QTableWidget {
                border: 1px solid palette(mid);
                border-radius: 6px;
                gridline-color: palette(mid);
            }

            QHeaderView::section {
                padding: 6px;
                font-weight: bold;
            }

            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
            }
            """
        )

        self.check_for_updates()

    def check_for_updates(self):
        self.check_button.setEnabled(False)
        self.check_button.setText("Prüfe...")
        self.update_label.setText("⟳ Prüfe auf Updates...")
        

        self.checker_thread = UpdateCheckerThread()

        self.checker_thread.updates_ready.connect(
            self.update_results
        )

        self.checker_thread.error_occurred.connect(
            self.show_error
        )

        self.checker_thread.finished.connect(
            lambda: (
                self.check_button.setEnabled(True),
                self.check_button.setText("Jetzt prüfen"),
            )
        )

        self.checker_thread.start()

    def update_results(self, updates):
        count = len(updates)

        if count == 0:
            self.update_label.setText("✓ Keine Updates verfügbar")
        else:
            self.update_label.setText(
                f"● {count} Updates verfügbar"
        )

        self.update_table.setRowCount(0)

        for row, update in enumerate(updates):
            self.update_table.insertRow(row)

            self.update_table.setItem(
                row,
                0,
                QTableWidgetItem(update.name),
            )

            self.update_table.setItem(
                row,
                1,
                QTableWidgetItem(update.old_version),
            )

            self.update_table.setItem(
                row,
                2,
                QTableWidgetItem(update.new_version),
            )

        self.update_table.resizeColumnsToContents()

    def show_error(self, error):
        self.update_label.setText(
            f"Fehler beim Prüfen:\n{error}"
    )

        self.update_table.setRowCount(0)


def should_show_autostart_reminder():
    try:
        updates = check_updates()
        return bool(updates)
    except Exception:
        return False


def main():
    app = QApplication(sys.argv)

    autostart = "--autostart" in sys.argv

    if autostart and not should_show_autostart_reminder():
        sys.exit(0)

    window = UpdateReminderWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()