from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
import webbrowser
from app.utils.updater import DOWNLOAD_URL


class UpdateDialog(QDialog):
    def __init__(self, current_version, latest_version):
        super().__init__()

        self.setWindowTitle("Update Available")
        self.setFixedSize(400, 220)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 15px;
            }
            QPushButton {
                background-color: #1e293b;
                color: white;
                padding: 10px 18px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
            QPushButton#updateBtn {
                background-color: #0ea5e9;
            }
            QPushButton#updateBtn:hover {
                background-color: #0284c7;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel(f"<b>New Version Available</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(title)

        info = QLabel(
            f"Current Version: {current_version}\n"
            f"Latest Version: {latest_version}\n\n"
            "Would you like to download the latest update?"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        btn_layout = QHBoxLayout()

        update_btn = QPushButton("Download Update")
        update_btn.setObjectName("updateBtn")
        update_btn.clicked.connect(lambda: webbrowser.open(DOWNLOAD_URL))
        btn_layout.addWidget(update_btn)

        skip_btn = QPushButton("Skip")
        skip_btn.clicked.connect(self.close)
        btn_layout.addWidget(skip_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)
