# app/ui/pages/quicktools_page.py

import os
import webbrowser

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit
)

from app.ui.widgets.cards import Card
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton


class QuickToolsPage(QWidget):
    """
    Quick Tools:
    - Open common folders (FiveM, logs, temp)
    - Launch FiveM / Steam
    - Open Discord / Itch.io links
    No duplicated cleaning / troubleshooting processes.
    """

    def __init__(self):
        super().__init__()
        self.build_ui()

    # ---------------------------------------------------------
    # BUILD UI
    # ---------------------------------------------------------
    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Title + subtitle
        title = QLabel("Quick Tools")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Fast access to folders, launchers and useful links.")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(subtitle)

        # ============================================================== #
        # IMPORTANT FOLDERS
        # ============================================================== #
        folder_card = Card()
        folder_layout = QVBoxLayout(folder_card)

        header1 = QLabel("Important Folders")
        header1.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        folder_layout.addWidget(header1)

        row1 = QHBoxLayout()

        buttons = [
            ("Open FiveM Folder", r"%localappdata%\FiveM\FiveM.app"),
            ("Open FiveM Logs", r"%localappdata%\FiveM\FiveM.app\logs"),
            ("Open Temp Folder", r"%temp%")
        ]

        for text, path in buttons:
            btn = SecondaryButton(text)
            btn.clicked.connect(lambda _, p=path: self.open_folder(p))
            row1.addWidget(btn)

        folder_layout.addLayout(row1)
        layout.addWidget(folder_card)

        # ============================================================== #
        # PROGRAM LAUNCHERS
        # ============================================================== #
        launch_card = Card()
        launch_layout = QVBoxLayout(launch_card)

        header2 = QLabel("Launchers")
        header2.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        launch_layout.addWidget(header2)

        row2 = QHBoxLayout()

        programs = [
            ("Launch FiveM", "FiveM.exe"),
            ("Launch Steam", "steam.exe")
        ]

        for text, exe in programs:
            btn = PrimaryButton(text)
            btn.clicked.connect(lambda _, e=exe: self.launch_exe(e))
            row2.addWidget(btn)

        launch_layout.addLayout(row2)
        layout.addWidget(launch_card)

        # ============================================================== #
        # USEFUL LINKS
        # ============================================================== #
        links_card = Card()
        links_layout = QVBoxLayout(links_card)

        header3 = QLabel("Useful Links")
        header3.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        links_layout.addWidget(header3)

        row3 = QHBoxLayout()

        links = [
            ("LURP Discord", "https://discord.gg/6zw4yZMn2w"),
            ("Itch.io Page", "https://manlikedex.itch.io/LURP-cache-clear-utility-tool")
        ]

        for text, url in links:
            btn = SecondaryButton(text)
            btn.clicked.connect(lambda _, u=url: webbrowser.open(u))
            row3.addWidget(btn)

        links_layout.addLayout(row3)
        layout.addWidget(links_card)

        # ============================================================== #
        # LOGGING AREA
        # ============================================================== #
        log_card = Card()
        log_layout = QVBoxLayout(log_card)

        log_header = QLabel("Quick Tools Log")
        log_header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        log_layout.addWidget(log_header)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(200)
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

    # ---------------------------------------------------------
    # LOGGING
    # ---------------------------------------------------------
    def log_msg(self, msg: str):
        self.log.append(msg)

    # ---------------------------------------------------------
    # ACTION HANDLERS
    # ---------------------------------------------------------
    def open_folder(self, path: str):
        resolved = os.path.expandvars(path)

        if os.path.exists(resolved):
            try:
                os.startfile(resolved)
                self.log_msg(f"📁 Opened folder: {resolved}")
            except Exception as e:
                self.log_msg(f"⚠ Could not open folder: {resolved}\n{e}")
        else:
            self.log_msg(f"❌ Folder not found: {resolved}")

    def launch_exe(self, exe_name: str):
        try:
            os.startfile(exe_name)
            self.log_msg(f"🚀 Launched: {exe_name}")
        except Exception:
            self.log_msg(f"❌ Could not launch: {exe_name}")
