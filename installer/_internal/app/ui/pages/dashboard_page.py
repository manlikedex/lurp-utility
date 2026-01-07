from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt

from app.ui.widgets.cards import Card
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton


def format_bytes(num: int):
    """Convert bytes → human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024
    return f"{num:.2f} TB"


class DashboardPage(QWidget):
    """
    MAIN DASHBOARD PAGE
    Shows:
    - Quick Actions (Scan / Clean)
    - Storage Summary (from splash pre-scan)
    - Scan & Cleaning Log
    """

    def __init__(self, storage_info):
        super().__init__()

        self.storage_info = storage_info or {}
        self.build_ui()

    # -------------------------------------------------------
    # BUILD UI
    # -------------------------------------------------------
    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # ---------------------------------------------
        # PAGE TITLE
        # ---------------------------------------------
        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Scan and clean your FiveM-related cache before hopping into RP.")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(subtitle)

        # ---------------------------------------------
        # QUICK ACTIONS CARD
        # ---------------------------------------------
        quick_card = Card()
        quick_layout = QVBoxLayout(quick_card)

        quick_header = QLabel("Quick Actions")
        quick_header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        quick_layout.addWidget(quick_header)

        quick_sub = QLabel(
            "Run a full scan to see how much space can be freed, then clean everything instantly."
        )
        quick_sub.setStyleSheet("color: #9ba5b7; font-size: 13px;")
        quick_layout.addWidget(quick_sub)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.scan_all_btn = PrimaryButton("Scan All")
        self.clean_all_btn = SecondaryButton("Clean Everything")

        self.scan_all_btn.clicked.connect(self.scan_all)
        self.clean_all_btn.clicked.connect(self.clean_everything)

        btn_row.addWidget(self.scan_all_btn)
        btn_row.addWidget(self.clean_all_btn)
        quick_layout.addLayout(btn_row)

        layout.addWidget(quick_card)

        # ---------------------------------------------
        # STORAGE SUMMARY
        # ---------------------------------------------
        storage_card = Card()
        storage_layout = QVBoxLayout(storage_card)

        header = QLabel("Storage Summary")
        header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        storage_layout.addWidget(header)

        if self.storage_info:
            for name, size in self.storage_info.items():
                if name == "Total":
                    continue
                row = QLabel(f"{name}: {format_bytes(size)}")
                row.setStyleSheet("color: #cbd5e1; font-size: 14px;")
                storage_layout.addWidget(row)

            total = self.storage_info.get("Total", 0)
            total_label = QLabel(
                f"<b>Total Recoverable Space:</b> {format_bytes(total)}"
            )
            total_label.setStyleSheet(
                "color: #38bdf8; font-size: 16px; margin-top: 6px;"
            )
            storage_layout.addWidget(total_label)
        else:
            empty_msg = QLabel("No storage data loaded (run a scan).")
            empty_msg.setStyleSheet("color: #7a8699; font-size: 14px;")
            storage_layout.addWidget(empty_msg)

        layout.addWidget(storage_card)

        # ---------------------------------------------
        # SCAN LOG OUTPUT
        # ---------------------------------------------
        log_card = Card()
        log_layout = QVBoxLayout(log_card)

        log_header = QLabel("Scan & Cleaning Log")
        log_header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        log_layout.addWidget(log_header)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(260)
        self.log_box.setStyleSheet("""
            QTextEdit {
                background-color: #0b1120;
                color: #d0d8e8;
                border: none;
                font-size: 13px;
            }
        """)
        log_layout.addWidget(self.log_box)

        layout.addWidget(log_card)
        layout.addStretch()

    # -------------------------------------------------------
    # ACTION HANDLERS
    # (Hook these into your real cleaning system later)
    # -------------------------------------------------------

    def scan_all(self):
        self.log_box.append("🔍 Scanning FiveM Cache...")
        self.log_box.append("🔍 Scanning GTA Shader Cache...")
        self.log_box.append("🔍 Scanning Windows Temp...")
        self.log_box.append("✔ Scan complete!\n")

    def clean_everything(self):
        self.log_box.append("🧹 Cleaning FiveM Cache...")
        self.log_box.append("🧹 Cleaning Shader Cache...")
        self.log_box.append("🧹 Cleaning Temp Files...")
        self.log_box.append("✔ Cleanup complete!\n")
