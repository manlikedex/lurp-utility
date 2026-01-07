

from PyQt6.QtCore import Qt, QPropertyAnimation, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar



from app.utils.updater import check_for_updates, CURRENT_VERSION
from app.utils.systeminfo import get_storage_analysis
from app.ui.widgets.update_dialog import UpdateDialog


class SplashScreen(QWidget):
    finished = pyqtSignal(object)  # emits storage_info

    def __init__(self):
        super().__init__()

        # Window setup
        self.setFixedSize(600, 350)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(0.0)
        self.setStyleSheet("background-color: #050816; border-radius: 18px;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        logo = QLabel()
        pix = QPixmap("app/resources/LURP_logo.png").scaled(
            130, 130,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        logo.setPixmap(pix)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        # Title
        title = QLabel("LURP Cache Clear Utility")
        title.setStyleSheet("color: white; font-size: 26px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        self.sub = QLabel("Starting...")
        self.sub.setStyleSheet("color: #94a3b8; font-size: 14px; margin-bottom: 10px;")
        self.sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sub)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setFixedWidth(400)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #0b1120;
                border-radius: 10px;
                height: 14px;
            }
            QProgressBar::chunk {
                background-color: #0ea5e9;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.progress)

        self.setLayout(layout)

        # Start fade-in
        self.fade_in()

        # Start the startup sequence after a tiny delay
        QTimer.singleShot(300, self.run_startup_sequence)

    def fade_in(self):
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(700)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.start()
        self.anim_in = anim

    def run_startup_sequence(self):
        # Step 1: Check updates
        self.sub.setText("Checking for updates...")
        self.progress.setValue(25)
        update_available, latest_version = check_for_updates()

        self.update_info = (update_available, latest_version)

        # Step 2: Scan storage
        self.sub.setText("Scanning storage and cache...")
        self.progress.setValue(60)
        self.storage_info = get_storage_analysis()

        # Step 3: Finalizing
        self.sub.setText("Finalizing startup...")
        self.progress.setValue(100)

        # Tiny pause then fade out
        QTimer.singleShot(400, self.fade_out)

    def fade_out(self):
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(700)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.finished.connect(self.finish_splash)
        anim.start()
        self.anim_out = anim

    def finish_splash(self):
        # Safe: all on main thread
        available, newest = self.update_info
        if available:
            dlg = UpdateDialog(CURRENT_VERSION, newest)
            dlg.exec()

        self.finished.emit(self.storage_info)
        self.close()
