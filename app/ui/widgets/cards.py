from PyQt6.QtWidgets import QFrame


class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Card")
