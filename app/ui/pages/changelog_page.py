import os

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTextBrowser, QMessageBox
)

from app.ui.widgets.cards import Card
from app.ui.widgets.buttons import PrimaryButton


class ChangelogPage(QWidget):
    """
    Displays changelog from a local text file instead of pulling from Itch.io.
    
    File location:
        app/resources/changelog.txt
    """

    CHANGELOG_FILE = "app/resources/changelog.txt"

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel("Changelog")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel("All updates and improvements to the LURP Utility Suite.")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(subtitle)

        # Refresh button
        refresh_btn = PrimaryButton("Reload Changelog")
        refresh_btn.clicked.connect(self.load_changelog)
        layout.addWidget(refresh_btn)

        # Card for text
        card = Card()
        card_layout = QVBoxLayout(card)

        self.browser = QTextBrowser()
        self.browser.setStyleSheet("""
            QTextBrowser {
                background-color: #0b1120;
                color: #cbd5e1;
                padding: 10px;
                font-size: 14px;
                border: none;
            }
        """)
        card_layout.addWidget(self.browser)

        layout.addWidget(card)
        layout.addStretch()

        # Load changelog on startup
        self.load_changelog()

    # ----------------------------------------
    # Load changelog file contents
    # ----------------------------------------
    def load_changelog(self):
        try:
            # File does not exist?
            if not os.path.exists(self.CHANGELOG_FILE):
                self.browser.setText(
                    "No changelog file found.\n\n"
                    f"Expected file:\n{self.CHANGELOG_FILE}\n\n"
                    "Please create the changelog.txt file."
                )
                return

            # Load file text
            with open(self.CHANGELOG_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                self.browser.setText("Changelog file is empty.")
            else:
                self.browser.setText(content)

        except Exception as e:
            self.show_error(f"Failed to load changelog:\n\n{e}")

    # ----------------------------------------
    # Error popup
    # ----------------------------------------
    def show_error(self, message: str):
        msg = QMessageBox()
        msg.setWindowTitle("Changelog Error")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()
