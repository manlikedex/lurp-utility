import sys
from PyQt6.QtWidgets import QApplication

from app.ui.splash import SplashScreen
from app.ui.main_window import MainWindow


# Keep references so windows do not get garbage collected
main_window_ref = None
splash_screen_ref = None


def open_main_window(storage_info):
    """
    Called when the splash screen finishes scanning.
    """
    global main_window_ref, splash_screen_ref

    if splash_screen_ref is not None:
        splash_screen_ref.close()

    main_window_ref = MainWindow(storage_info)
    main_window_ref.show()


def main():
    app = QApplication(sys.argv)

    global splash_screen_ref
    splash_screen_ref = SplashScreen()
    splash_screen_ref.finished.connect(open_main_window)
    splash_screen_ref.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
