from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.uic import loadUi

ui_path = "./ui/"

class DisplayInvoices(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(f"{ui_path}displayInvoices.ui", self)
        self.setupUI()

    def setupUI(self):
        pass