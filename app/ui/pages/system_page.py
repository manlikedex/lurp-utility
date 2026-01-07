import platform
import psutil

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer

from app.ui.widgets.cards import Card

# Try to import GPUtil for GPU stats
try:
    import GPUtil
except ImportError:
    GPUtil = None


def format_bytes(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} TB"


class SystemInfoPage(QWidget):
    """
    System Information Page
    - Shows static system info
    - Live CPU, RAM, GPU usage
    - Disk usage
    """

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # -------------------------------------------------------------
        # TITLE
        # -------------------------------------------------------------
        title = QLabel("System Information")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Live overview of CPU, GPU and memory usage.")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(subtitle)

        # -------------------------------------------------------------
        # STATIC SYSTEM INFO
        # -------------------------------------------------------------
        sys_card = Card()
        sys_layout = QVBoxLayout(sys_card)

        header = QLabel("Hardware Overview")
        header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        sys_layout.addWidget(header)

        os_lbl = QLabel(f"Operating System: {platform.system()} {platform.release()}")
        cpu_lbl = QLabel(f"Processor: {platform.processor() or 'Unknown CPU'}")
        machine_lbl = QLabel(f"Machine Name: {platform.node()}")

        for lbl in (os_lbl, cpu_lbl, machine_lbl):
            lbl.setStyleSheet("color: #cbd5e1; font-size: 14px;")
            sys_layout.addWidget(lbl)

        layout.addWidget(sys_card)

        # -------------------------------------------------------------
        # LIVE USAGE CARD
        # -------------------------------------------------------------
        usage_card = Card()
        usage_layout = QVBoxLayout(usage_card)

        usage_header = QLabel("Live Usage")
        usage_header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        usage_layout.addWidget(usage_header)

        # CPU
        self.cpu_bar = self._make_usage_row(usage_layout, "CPU Usage:")

        # RAM
        self.ram_bar = self._make_usage_row(usage_layout, "RAM Usage:")

        # GPU
        self.gpu_label = QLabel("GPU Usage:")
        self.gpu_label.setStyleSheet("color: #e5e7eb; font-size: 14px;")

        gpu_row = QHBoxLayout()
        gpu_row.addWidget(self.gpu_label)

        self.gpu_bar = QProgressBar()
        self.gpu_bar.setRange(0, 100)
        self.gpu_bar.setFormat("%p%")
        self.gpu_bar.setStyleSheet("""
            QProgressBar {
                background: #1e293b;
                border-radius: 6px;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #6366f1;
                border-radius: 6px;
            }
        """)

        gpu_row.addWidget(self.gpu_bar)
        usage_layout.addLayout(gpu_row)

        layout.addWidget(usage_card)

        # -------------------------------------------------------------
        # DISK USAGE
        # -------------------------------------------------------------
        disk_card = Card()
        disk_layout = QVBoxLayout(disk_card)

        disk_header = QLabel("Disk Usage")
        disk_header.setStyleSheet("font-size: 16px; color: white; font-weight: 600;")
        disk_layout.addWidget(disk_header)

        try:
            disk = psutil.disk_usage("C:\\")
            disk_lbl = QLabel(
                f"C: {format_bytes(disk.used)} / {format_bytes(disk.total)} "
                f"({disk.percent}%)"
            )
        except Exception:
            disk_lbl = QLabel("Disk information unavailable.")

        disk_lbl.setStyleSheet("color: #cbd5e1; font-size: 14px;")
        disk_layout.addWidget(disk_lbl)

        layout.addWidget(disk_card)
        layout.addStretch()

        # -------------------------------------------------------------
        # TIMER FOR LIVE STATS
        # -------------------------------------------------------------
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    # -------------------------------------------------------------
    # Helper: Create usage row
    # -------------------------------------------------------------
    def _make_usage_row(self, parent_layout, label_text):
        row = QHBoxLayout()

        label = QLabel(label_text)
        label.setStyleSheet("color: #e5e7eb; font-size: 14px;")
        row.addWidget(label)

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setFormat("%p%")
        bar.setStyleSheet("""
            QProgressBar {
                background: #1e293b;
                border-radius: 6px;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #f97316;
                border-radius: 6px;
            }
        """)

        row.addWidget(bar)
        parent_layout.addLayout(row)

        return bar

    # -------------------------------------------------------------
    # UPDATE LIVE STATS
    # -------------------------------------------------------------
    def update_stats(self):
        # CPU
        cpu_usage = psutil.cpu_percent(interval=0.1)
        self.cpu_bar.setValue(int(cpu_usage))

        # RAM
        ram = psutil.virtual_memory()
        self.ram_bar.setValue(int(ram.percent))

        # GPU
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    usage = int(gpu.load * 100)
                    self.gpu_bar.setValue(usage)
                    self.gpu_label.setText(f"GPU Usage ({gpu.name}):")
                else:
                    self.gpu_label.setText("GPU Usage: (no GPU detected)")
                    self.gpu_bar.setValue(0)
            except Exception:
                self.gpu_label.setText("GPU Usage: (error reading GPU)")
                self.gpu_bar.setValue(0)
        else:
            self.gpu_label.setText("GPU Usage: (GPUtil not installed)")
            self.gpu_bar.setValue(0)
