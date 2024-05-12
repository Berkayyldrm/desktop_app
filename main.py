from DesktopSelenium import DesktopSelenium
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QTableWidgetItem
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
import sys
from PyQt6.QtWidgets import QFileDialog, QLabel, QPushButton
import pandas as pd
from DisplayInvoices import DisplayInvoices
ui_path = "./ui/"
#logo_file = "path/to/your/logo.png"  # Logo dosyasının yolu

class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        loadUi(f"{ui_path}main.ui", self)
        self.setupUI()
        self.desktopSelenium = DesktopSelenium()
        self.data = None
        self.loginValidation = False

    def setupUI(self):
        self.openFileButton = self.findChild(QPushButton, 'filePathButton') 
        self.filePathLabel = QLabel("Dosya yolu burada görünecek", self)
        self.openFileButton.clicked.connect(self.openFileDialog)
        self.loginButton.clicked.connect(self.loginFunction)
        self.filePathBrowser.textChanged.connect(self.excelOperations)
        self.createInvoiceButton.clicked.connect(self.createInvoice)
        self.displayInvoicesButton.clicked.connect(self.displayInvoicesScreen)
    
    def loginFunction(self):
        self.username = self.usernameLineEdit.text()
        self.password = self.passwordLineEdit.text()
        if self.username == "test" and self.password == "test":
            urlWithToken = self.desktopSelenium.connectTestAccount()
            self.loginValidation = True
            print(urlWithToken)
            #self.desktopSelenium.closeConnection()

    def createInvoice(self):
        if isinstance(self.data, pd.DataFrame) and self.loginValidation:
            self.desktopSelenium.createInvoice()
        else:
            print("Veri Ekleyiniz.")

    def openFileDialog(self):
        self.filePath, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Tüm Dosyalar (*);;Metin Dosyaları (*.txt)")
        if self.filePath:
            self.filePathBrowser.setText(self.filePath)

    def excelOperations(self):
        self.data = pd.read_excel(self.filePath) 
        print(self.data)
        #data_short = data[[""]]
        self.mainDataTable.setRowCount(len(self.data))
        self.mainDataTable.setColumnCount(len(self.data.columns))
        self.mainDataTable.setHorizontalHeaderLabels(self.data.columns)

        for i in range(len(self.data)):
            for j in range(len(self.data.columns)):
                self.mainDataTable.setItem(i, j, QTableWidgetItem(str(self.data.iloc[i, j])))

    def displayInvoicesScreen(self):
        self.second_window = DisplayInvoices()
        self.second_window.show()

app = QApplication(sys.argv)
mainwindow = Main()
#app_icon = QIcon(logo_file)
#app.setWindowIcon(app_icon)
widget = QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedSize(1500, 1500)  # Eğer boyutu sabit olarak ayarlamak isterseniz
widget.show()
app.exec()