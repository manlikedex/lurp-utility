# app/ui/main_window.py

import sys
import webbrowser
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

from app.utils.paths import resource_path

# Import pages
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.cleaning_page import CleaningPage
from app.ui.pages.quicktools_page import QuickToolsPage
from app.ui.pages.system_page import SystemInfoPage
from app.ui.pages.troubleshooter_page import TroubleshooterPage
from app.ui.pages.changelog_page import ChangelogPage
from app.ui.pages.about_page import AboutPage


class MainWindow(QWidget):
    def __init__(self, storage_info):
        super().__init__()

        # Window settings
        self.setWindowTitle("LURP Utility Suite - Made by Dex")
        self.setMinimumSize(1300, 750)
        self.setWindowIcon(QIcon(resource_path("app/resources/LURP_logo.ico")))

        # Root layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ======================================================================
        # SIDEBAR
        # ======================================================================
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(280)

        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(24, 30, 24, 30)
        sb_layout.setSpacing(22)

        # -----------------------------
        # LOGO + TITLE
        # -----------------------------
        logo_container = QVBoxLayout()
        logo_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_container.setSpacing(8)

        logo = QLabel()
        pix = QPixmap(resource_path("app/resources/LURP_logo.png"))
        if not pix.isNull():
            logo.setPixmap(
                pix.scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio,
                           Qt.TransformationMode.SmoothTransformation)
            )
        logo_container.addWidget(logo)

        title = QLabel("LURP Utility Suite")
        title.setObjectName("SidebarAppName")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_container.addWidget(title)

        sb_layout.addLayout(logo_container)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #1a2234;")
        sb_layout.addWidget(divider)

        # NAV text
        nav_header = QLabel("NAVIGATION")
        nav_header.setObjectName("SidebarSection")
        sb_layout.addWidget(nav_header)

        # -----------------------------
        # NAVIGATION LIST
        # -----------------------------
        self.nav = QListWidget()
        self.nav.setObjectName("SidebarList")
        self.nav.setSpacing(6)
        self.nav.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        nav_items = [
            "🏠  Dashboard",
            "🧹  Cleaning Tools",
            "⚡  Quick Tools",
            "💻  System Info",
            "🛠  Troubleshooter",
            "📝  Changelog",
            "ℹ️  About"
        ]

        for label in nav_items:
            item = QListWidgetItem(label)
            item.setSizeHint(QSize(220, 46))  # make nav items larger
            self.nav.addItem(item)

        # Navigation fills space but leaves room for Discord button
        sb_layout.addWidget(self.nav, stretch=1)

        # Reserved space so Discord button NEVER gets covered
        bottom_spacer = QFrame()
        bottom_spacer.setFixedHeight(50)
        sb_layout.addWidget(bottom_spacer)

        # -----------------------------
        # DISCORD BUTTON
        # -----------------------------
        discord_btn = QPushButton("Join Discord")
        discord_btn.setObjectName("SidebarDiscordBtn")
        discord_btn.setFixedHeight(46)
        discord_btn.clicked.connect(lambda: webbrowser.open("https://discord.gg/6zw4yZMn2w"))
        sb_layout.addWidget(discord_btn)

        note = QLabel("Support & updates available\ninside Discord.")
        note.setObjectName("SidebarNote")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb_layout.addWidget(note)

        # ======================================================================
        # MAIN CONTENT PAGES
        # ======================================================================
        self.pages = QStackedWidget()

        self.page_list = [
            DashboardPage(storage_info),
            CleaningPage(),
            QuickToolsPage(),
            SystemInfoPage(),
            TroubleshooterPage(),
            ChangelogPage(),
            AboutPage()
        ]

        for page in self.page_list:
            self.pages.addWidget(page)

        # Connect navigation to page changing
        self.nav.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.nav.setCurrentRow(0)

        # Add sidebar and pages to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)
