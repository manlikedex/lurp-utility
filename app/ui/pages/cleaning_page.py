import os
import shutil
import threading

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt

from app.ui.widgets.cards import Card
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton
from app.utils.systeminfo import folder_size


def format_bytes(num: int):
    """Convert bytes → readable size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024
    return f"{num:.2f} TB"


class CleaningPage(QWidget):
    """
    Full Cleaning Page (FiveM cache, logs, shaders, Windows temp)
    PRO — No conflicts with Troubleshooter.
    """

    def __init__(self):
        super().__init__()

        # All paths handled here
        self.paths = {
            "FiveM Cache": r"%localappdata%\FiveM\FiveM.app\data\cache",
            "FiveM Logs": r"%localappdata%\FiveM\FiveM.app\logs",
            "GTA V Shader Cache": r"%localappdata%\Rockstar Games\GTA V\Shaders",
            "Windows Temp": r"%temp%",
        }

        self.labels = {}
        self.build_ui()
        self.refresh_sizes_async()

    # -------------------------------------------------------------
    # BUILD UI
    # -------------------------------------------------------------
    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        title = QLabel("Cleaning Tools")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Clean FiveM caches, logs, shader cache and Windows temp safely.")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(subtitle)

        # -------------------------------------------------------------
        # SIZE SUMMARY CARD
        # -------------------------------------------------------------
        summary_card = Card()
        summary_layout = QVBoxLayout(summary_card)

        header = QLabel("Cache Overview")
        header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        summary_layout.addWidget(header)

        for name in self.paths.keys():
            lbl = QLabel(f"{name}: scanning…")
            lbl.setStyleSheet("color: #cbd5e1; font-size: 14px;")
            summary_layout.addWidget(lbl)
            self.labels[name] = lbl

        self.total_label = QLabel("Total Recoverable Space: scanning…")
        self.total_label.setStyleSheet("color: #38bdf8; font-size: 15px;")
        summary_layout.addWidget(self.total_label)

        layout.addWidget(summary_card)

        # -------------------------------------------------------------
        # ACTION BUTTONS
        # -------------------------------------------------------------
        actions_card = Card()
        actions_layout = QVBoxLayout(actions_card)

        action_header = QLabel("Actions")
        action_header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        actions_layout.addWidget(action_header)

        row = QHBoxLayout()
        clean_btn = PrimaryButton("Clean All")
        rescan_btn = SecondaryButton("Rescan Sizes")

        clean_btn.clicked.connect(self.clean_all_async)
        rescan_btn.clicked.connect(self.refresh_sizes_async)

        row.addWidget(clean_btn)
        row.addWidget(rescan_btn)
        actions_layout.addLayout(row)

        layout.addWidget(actions_card)

        # -------------------------------------------------------------
        # LOG OUTPUT
        # -------------------------------------------------------------
        log_card = Card()
        log_layout = QVBoxLayout(log_card)

        log_header = QLabel("Cleaning Log")
        log_header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        log_layout.addWidget(log_header)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(260)
        self.log.setStyleSheet("""
            QTextEdit {
                background-color: #0b1120;
                color: #d0d8e8;
                border: none;
                font-size: 13px;
            }
        """)

        log_layout.addWidget(self.log)
        layout.addWidget(log_card)

        layout.addStretch()

    # -------------------------------------------------------------
    # THREAD-SAFE UI LOGGING
    # -------------------------------------------------------------
    def log_msg(self, msg: str):
        self.log.append(msg)

    # -------------------------------------------------------------
    # ASYNC SIZE SCAN
    # -------------------------------------------------------------
    def refresh_sizes_async(self):
        threading.Thread(target=self.refresh_sizes, daemon=True).start()

    def refresh_sizes(self):
        total = 0

        for name, path in self.paths.items():
            expanded = os.path.expandvars(path)

            if os.path.exists(expanded):
                try:
                    size = folder_size(expanded)
                    total += size
                    text = f"{name}: {format_bytes(size)}"
                except Exception:
                    text = f"{name}: error scanning"
            else:
                text = f"{name}: not found"

            self.labels[name].setText(text)

        self.total_label.setText(f"Total Recoverable Space: {format_bytes(total)}")

    # -------------------------------------------------------------
    # ASYNC CLEAN ALL
    # -------------------------------------------------------------
    def clean_all_async(self):
        threading.Thread(target=self.clean_all, daemon=True).start()

    def clean_all(self):
        self.log_msg("🧹 Starting cleanup…")

        for name, path in self.paths.items():
            expanded = os.path.expandvars(path)

            if not os.path.exists(expanded):
                self.log_msg(f"{name}: path not found, skipping.")
                continue

            removed = 0
            for root, dirs, files in os.walk(expanded):
                for f in files:
                    try:
                        os.remove(os.path.join(root, f))
                        removed += 1
                    except Exception:
                        pass

            self.log_msg(f"{name}: removed {removed} files.")

        self.log_msg("✔ Cleanup complete.\n")
        self.refresh_sizes_async()
