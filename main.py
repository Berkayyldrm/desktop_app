from DesktopSelenium import DesktopSelenium
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QTableWidgetItem
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
import sys
from PyQt6.QtWidgets import QFileDialog, QLabel, QPushButton
import pandas as pd

ui_path = "./ui/"
#logo_file = "path/to/your/logo.png"  # Logo dosyasının yolu

class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        loadUi(f"{ui_path}main.ui", self)
        self.setupUI()
        self.desktopSelenium = DesktopSelenium()

    def setupUI(self):
        self.openFileButton = self.findChild(QPushButton, 'filePathButton') 
        self.filePathLabel = QLabel("Dosya yolu burada görünecek", self)
        self.openFileButton.clicked.connect(self.openFileDialog)
        self.loginButton.clicked.connect(self.loginFunction)
        self.filePathBrowser.textChanged.connect(self.excelOperations)
    
    def loginFunction(self):
        self.username = self.usernameLineEdit.text()
        self.password = self.passwordLineEdit.text()
        if self.username == "test" and self.password == "test":
            urlWithToken = self.desktopSelenium.connectTestAccount()
            print(urlWithToken)
            self.desktopSelenium.closeConnection()

    def openFileDialog(self):
        self.filePath, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Tüm Dosyalar (*);;Metin Dosyaları (*.txt)")
        if self.filePath:
            self.filePathBrowser.setText(self.filePath)

    def excelOperations(self):
        data = pd.read_excel(self.filePath) 
        print(data)
        data_short = data[[""]]
        self.mainDataTable.setRowCount(len(data))
        self.mainDataTable.setColumnCount(len(data.columns))
        self.mainDataTable.setHorizontalHeaderLabels(data.columns)

        for i in range(len(data)):
            for j in range(len(data.columns)):
                self.mainDataTable.setItem(i, j, QTableWidgetItem(str(data.iloc[i, j])))

app = QApplication(sys.argv)
mainwindow = Main()
#app_icon = QIcon(logo_file)
#app.setWindowIcon(app_icon)
widget = QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedSize(1500, 1500)  # Eğer boyutu sabit olarak ayarlamak isterseniz
widget.show()
app.exec()