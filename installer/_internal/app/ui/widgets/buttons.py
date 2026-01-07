from PyQt6.QtWidgets import QPushButton


class SidebarButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setObjectName("SidebarButton")
        self.setCheckable(True)


class PrimaryButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setObjectName("PrimaryButton")


class SecondaryButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setObjectName("SecondaryButton")
