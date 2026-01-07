import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import webbrowser


class AboutPage(QWidget):
    """
    Simple about page with logo, version, and credits.
    """

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("About")
        title.setStyleSheet("font-size: 26px; color: white; font-weight: 600;")
        layout.addWidget(title)

        # Subtitle
        sub = QLabel("Information about this tool and its developer.")
        sub.setStyleSheet("font-size: 14px; color: #94a3b8;")
        layout.addWidget(sub)

        # Logo Area
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logo_path = os.path.join(base_dir, "resources", "LURP_logo.png")

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
            logo.setPixmap(pix)

        layout.addWidget(logo)

        # App Info
        info = QLabel(
            "<b>LURP Cache Clear Utility</b><br>"
            "Version 1.2.0<br><br>"
            "Created by <b>ManLikeDex</b> for LURP community members.<br>"
            "This tool helps improve FiveM performance and stability.<br><br>"
            "Discord Support Available Below:"
        )
        info.setStyleSheet("color: #cbd5e1; font-size: 14px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)
        layout.addWidget(info)

        # Discord Button
        btn = QPushButton("Join LURP Discord")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #5865F2;
                border-radius: 20px;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
        """)

        btn.clicked.connect(
            lambda: webbrowser.open("https://discord.gg/6zw4yZMn2w")
        )

        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)
