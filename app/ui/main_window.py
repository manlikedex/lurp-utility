# app/ui/main_window.py
import os
import threading
import webbrowser

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QFrame, QMessageBox, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QTimer

from app.utils.paths import resource_path

# Version + updater
try:
    from app.utils.version import __version__
except Exception:
    __version__ = "0.0.0"

try:
    from app.utils.github_updater import check_github_update
except Exception:
    check_github_update = None

# Pages
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.cleaning_page import CleaningPage
from app.ui.pages.quicktools_page import QuickToolsPage
from app.ui.pages.system_page import SystemInfoPage
from app.ui.pages.troubleshooter_page import TroubleshooterPage
from app.ui.pages.changelog_page import ChangelogPage
from app.ui.pages.about_page import AboutPage


class MainWindow(QWidget):
    """
    LURP / NFRP Utility Suite Main Window
    - Professional sidebar layout (fills height)
    - All pages visible
    - Optional GitHub update check on launch
    """

    DISCORD_URL = "https://discord.gg/6zw4yZMn2w"

    # IMPORTANT: set these to your GitHub repo
    GITHUB_OWNER = "manlikedex"          
    GITHUB_REPO = "LURP-CacheClear"       

    def __init__(self, storage_info=None):
        super().__init__()
        self.storage_info = storage_info or {}

        self.setWindowTitle(f"LURP Utility Suite - Made by Dex (v{__version__})")
        self.setMinimumSize(1300, 750)

        # Window icon
        ico_path = resource_path("app/resources/nfrp_logo.ico")
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))

        self._page_buttons = {}  # name -> button

        self._build_ui()

        # Update check (non-blocking)
        QTimer.singleShot(900, self.start_update_check)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # =========================
        # SIDEBAR
        # =========================
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(300)

        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(18, 18, 18, 18)
        sb.setSpacing(12)

        # Logo
        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pix = QPixmap(resource_path("app/resources/nfrp_logo.png"))
        if not pix.isNull():
            logo.setPixmap(pix.scaled(
                190, 190,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        sb.addWidget(logo)

        # App name
        app_name = QLabel("LURP Utility Suite")
        app_name.setObjectName("SidebarLogoText")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb.addWidget(app_name)

        # Small sub text
        sub = QLabel("Cache Clear & Troubleshooting")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("color:#8f9bb3; font-size:12px;")
        sb.addWidget(sub)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("color:#1a2234;")
        sb.addWidget(div)

        # Navigation header
        nav_hdr = QLabel("NAVIGATION")
        nav_hdr.setObjectName("SidebarHeader")
        nav_hdr.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sb.addWidget(nav_hdr)

        # Nav container fills most of sidebar height
        nav_container = QFrame()
        nav_container.setStyleSheet("background: transparent;")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(8)

        # Pages stack
        self.pages = QStackedWidget()
        self.pages.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create page instances
        self.dashboard_page = DashboardPage(self.storage_info)
        self.cleaning_page = CleaningPage()
        self.quicktools_page = QuickToolsPage()
        self.system_page = SystemInfoPage()
        self.troubleshooter_page = TroubleshooterPage()
        self.changelog_page = ChangelogPage()
        self.about_page = AboutPage()

        # Add pages + sidebar buttons (order matters)
        self.safe_add_page(self.dashboard_page, "Dashboard")
        self.safe_add_page(self.cleaning_page, "Cleaning")
        self.safe_add_page(self.quicktools_page, "Quick Tools")
        self.safe_add_page(self.system_page, "System Info")
        self.safe_add_page(self.troubleshooter_page, "Troubleshooter")
        self.safe_add_page(self.changelog_page, "Changelog")
        self.safe_add_page(self.about_page, "About")

        nav_layout.addStretch(1)  # makes nav use vertical space nicely
        sb.addWidget(nav_container, 1)  # expand

        # Bottom actions (kept BELOW nav, never covered)
        discord_btn = QPushButton("Join LURP Discord")
        discord_btn.setObjectName("SidebarDanger")
        discord_btn.setFixedHeight(44)
        discord_btn.clicked.connect(lambda: webbrowser.open(self.DISCORD_URL))
        sb.addWidget(discord_btn)

        support = QLabel("Support & updates are handled in Discord.")
        support.setStyleSheet("color:#64748b; font-size:11px;")
        support.setWordWrap(True)
        support.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb.addWidget(support)

        # Put nav buttons into nav_container AFTER we created it
        # (so safe_add_page can attach)
        self._nav_layout = nav_layout

        # Rebuild nav buttons into nav layout in the correct order
        # (safe_add_page stored buttons in dict; we want same order as stack)
        self._render_nav_buttons_in_order()

        # =========================
        # MAIN AREA
        # =========================
        root.addWidget(sidebar)
        root.addWidget(self.pages)

        # Default page
        self.set_current_page_by_index(0)

    def _render_nav_buttons_in_order(self):
        # Remove any existing widgets in nav layout except the stretch
        # (We added stretch already; easiest is just insert before it.)
        # Insert buttons in the same order as pages in stack:
        ordered_names = [
            "Dashboard", "Cleaning", "Quick Tools",
            "System Info", "Troubleshooter", "Changelog", "About"
        ]
        # Insert before the stretch (which is last item)
        stretch_index = self._nav_layout.count() - 1
        for name in ordered_names:
            btn = self._page_buttons.get(name)
            if btn:
                self._nav_layout.insertWidget(stretch_index, btn)

    def _make_sidebar_button(self, text: str, index: int) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("SidebarButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(46)
        btn.clicked.connect(lambda: self.set_current_page_by_index(index))
        return btn

    def safe_add_page(self, widget: QWidget, name: str):
        """
        Adds a page to the stack and creates its sidebar button.
        """
        idx = self.pages.count()
        self.pages.addWidget(widget)

        btn = self._make_sidebar_button(name, idx)
        self._page_buttons[name] = btn
        print(f"[OK] Loaded page: {name}")

    def set_current_page_by_index(self, index: int):
        self.pages.setCurrentIndex(index)

        # uncheck all
        for b in self._page_buttons.values():
            b.setChecked(False)

        # check the matching button by stack index
        # (find by comparing button click index stored in lambda isn't accessible; so map by name order)
        name_by_index = [
            "Dashboard", "Cleaning", "Quick Tools",
            "System Info", "Troubleshooter", "Changelog", "About"
        ]
        if 0 <= index < len(name_by_index):
            nm = name_by_index[index]
            if nm in self._page_buttons:
                self._page_buttons[nm].setChecked(True)

    # ------------------------------------------------------------------
    # Update checker (GitHub Releases)
    # ------------------------------------------------------------------
    def start_update_check(self):
        if not check_github_update:
            return

        owner = (self.GITHUB_OWNER or "").strip()
        repo = (self.GITHUB_REPO or "").strip()
        if owner in ("", "YOURNAME") or repo in ("", "YOURREPO"):
            # Not configured yet
            return

        def worker():
            try:
                has_update, latest_tag, url = check_github_update(owner, repo, __version__)
                if not has_update:
                    return

                def show_popup():
                    box = QMessageBox(self)
                    box.setWindowTitle("Update Available")
                    box.setIcon(QMessageBox.Icon.Information)
                    box.setText(
                        "A new update is available for LURP Cache Clear Utility.\n\n"
                        f"Installed: {__version__}\n"
                        f"Latest: {latest_tag}\n\n"
                        "Press OK to open the GitHub download page."
                    )
                    box.exec()
                    if url:
                        webbrowser.open(url)

                QTimer.singleShot(0, show_popup)
            except Exception:
                # ignore offline / rate-limit etc
                pass

        threading.Thread(target=worker, daemon=True).start()
