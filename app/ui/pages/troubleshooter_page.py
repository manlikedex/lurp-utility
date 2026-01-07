import subprocess
import threading
import requests

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit
)

from app.ui.widgets.cards import Card
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton


class TroubleshooterPage(QWidget):
    """
    Troubleshooter:
    - Network reset / flush / test
    - Renew IP
    - Kill FiveM / Steam
    - Restart Explorer
    No cleaning tools.
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

        # Title
        title = QLabel("Troubleshooter")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Fix common network, process and connectivity issues instantly.")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(subtitle)

        # =========================================================
        # NETWORK FIX CARD
        # =========================================================
        net_card = Card()
        net_layout = QVBoxLayout(net_card)

        header = QLabel("Network Fix Tools")
        header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        net_layout.addWidget(header)

        row1 = QHBoxLayout()
        row1.setSpacing(12)

        btn_flush_dns = PrimaryButton("Flush DNS")
        btn_reset_net = SecondaryButton("Reset Network Stack")
        btn_renew_ip = SecondaryButton("Renew IP")
        btn_test_conn = SecondaryButton("Test Connection")

        btn_flush_dns.clicked.connect(lambda: self.run_async(self.flush_dns))
        btn_reset_net.clicked.connect(lambda: self.run_async(self.reset_network))
        btn_renew_ip.clicked.connect(lambda: self.run_async(self.renew_ip))
        btn_test_conn.clicked.connect(lambda: self.run_async(self.test_connection))

        row1.addWidget(btn_flush_dns)
        row1.addWidget(btn_reset_net)
        row1.addWidget(btn_renew_ip)
        row1.addWidget(btn_test_conn)

        net_layout.addLayout(row1)
        layout.addWidget(net_card)

        # =========================================================
        # PROCESS TOOLS
        # =========================================================
        proc_card = Card()
        proc_layout = QVBoxLayout(proc_card)

        header2 = QLabel("Process & Explorer Tools")
        header2.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        proc_layout.addWidget(header2)

        row2 = QHBoxLayout()
        row2.setSpacing(12)

        btn_kill_fivem = SecondaryButton("Kill FiveM")
        btn_kill_steam = SecondaryButton("Kill Steam")
        btn_restart_explorer = SecondaryButton("Restart Explorer")

        btn_kill_fivem.clicked.connect(
            lambda: self.run_async(lambda: self.kill_process("FiveM.exe"))
        )
        btn_kill_steam.clicked.connect(
            lambda: self.run_async(lambda: self.kill_process("steam.exe"))
        )
        btn_restart_explorer.clicked.connect(lambda: self.run_async(self.restart_explorer))

        row2.addWidget(btn_kill_fivem)
        row2.addWidget(btn_kill_steam)
        row2.addWidget(btn_restart_explorer)

        proc_layout.addLayout(row2)
        layout.addWidget(proc_card)

        # =========================================================
        # LOG OUTPUT
        # =========================================================
        log_card = Card()
        log_layout = QVBoxLayout(log_card)

        log_header = QLabel("Troubleshooting Log")
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

    # ---------------------------------------------------------
    # Thread wrapper (prevents UI freezing)
    # ---------------------------------------------------------
    def run_async(self, func):
        threading.Thread(target=func, daemon=True).start()

    # ---------------------------------------------------------
    # Log helper
    # ---------------------------------------------------------
    def log_msg(self, text: str):
        self.log.append(text)

    # ---------------------------------------------------------
    # NETWORK TOOLS
    # ---------------------------------------------------------
    def flush_dns(self):
        subprocess.run("ipconfig /flushdns", shell=True)
        self.log_msg("✔ DNS flushed successfully.")

    def reset_network(self):
        subprocess.run("netsh winsock reset", shell=True)
        subprocess.run("netsh int ip reset", shell=True)
        self.log_msg("✔ Network stack reset. (Restart recommended)")

    def renew_ip(self):
        self.log_msg("⏳ Releasing IP...")
        subprocess.run("ipconfig /release", shell=True)

        self.log_msg("⏳ Renewing IP...")
        subprocess.run("ipconfig /renew", shell=True)

        self.log_msg("✔ IP renewed.")

    def test_connection(self):
        self.log_msg("⏳ Testing internet connection...")
        try:
            requests.get("https://www.google.com", timeout=4)
            self.log_msg("✔ Internet connection OK.")
        except Exception:
            self.log_msg("✖ Internet unreachable.")

    # ---------------------------------------------------------
    # PROCESS TOOLS
    # ---------------------------------------------------------
    def kill_process(self, proc_name: str):
        subprocess.run(f"taskkill /F /IM {proc_name}", shell=True)
        self.log_msg(f"✔ Terminated: {proc_name} (if running).")

    def restart_explorer(self):
        self.log_msg("⏳ Restarting Windows Explorer...")
        subprocess.run("taskkill /F /IM explorer.exe", shell=True)
        subprocess.run("start explorer.exe", shell=True)
        self.log_msg("✔ Windows Explorer restarted.")
