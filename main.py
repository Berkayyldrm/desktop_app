from DesktopSelenium import DesktopSelenium
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
import sys
from PyQt6.QtWidgets import QFileDialog, QLabel, QPushButton
import pandas as pd
from DisplayInvoices import DisplayInvoices
ui_path = "./ui/"
#logo_file = "path/to/your/logo.png"  # Logo dosyasının yolu
from models.DataValidator import DataValidator
from models.sendInvoiceOperations import sendInvoiceOperations
from models.LoginOperations import LoginOperations
from PyQt6.QtWidgets import QMessageBox

class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        loadUi(f"{ui_path}main.ui", self)
        self.setupUI()
        self.desktopSelenium = DesktopSelenium()
        self.loginOperations = LoginOperations()
        self.data = None
        self.loginValidation = False
        self.userId = None
        self.userName = None
        self.token = None

    def setupUI(self):
        self.openFileButton = self.findChild(QPushButton, 'filePathButton') 
        self.filePathLabel = QLabel("Dosya yolu burada görünecek", self)
        self.openFileButton.clicked.connect(self.openFileDialog)
        self.loginButton.clicked.connect(self.loginFunction)
        self.logoutButton.clicked.connect(self.logoutFunction)
        self.filePathBrowser.textChanged.connect(self.excelOperations)
        self.createInvoiceButton.clicked.connect(self.createInvoice)
        self.displayInvoicesButton.clicked.connect(self.displayInvoicesScreen)
    
    def loginFunction(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        token = self.loginOperations.login(username, password)
        if token:
            self.token = token
            self.userId, self.userName = self.loginOperations.getLoginUserInfo(self.token)
            self.loginValidation = True
            QMessageBox.information(None, "Login Succesfully", f"Giriş yapıldı. {self.userId}, {self.userName}", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.warning(None, "Login Error", "Kullanıcı adı veya şifre hatalı.", QMessageBox.StandardButton.Ok)
        
    def logoutFunction(self):
        if self.loginValidation == True:
            tokenRemoveFlag = self.userId, self.userName = self.loginOperations.getLoginUserInfo(self.token)
            if tokenRemoveFlag:
                QMessageBox.information(None, "Logout Succesfully", f"Çıkış yapıldı. {self.userId}, {self.userName}", QMessageBox.StandardButton.Ok)
                self.userId = None
                self.userName = None
                self.token = None
                self.loginValidation = False
        else:
            QMessageBox.information(None, "Logout Unsuccesful", f"Daha önceden giriş yapılmadı.", QMessageBox.StandardButton.Ok)
        
    def createInvoice(self):
        if isinstance(self.data, pd.DataFrame) and self.loginValidation:
            self.desktopSelenium.createInvoice()
        else:
            print("Veri Ekleyiniz Ve Giriş Yapınız")

    def openFileDialog(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", "", 
                                                "Excel Files (*.xls *.xlsx);;All Files (*)")
        if filePath:
            if not (filePath.endswith('.xls') or filePath.endswith('.xlsx')):
                QMessageBox.warning(self, "Dosya Formatı Hatası", "Excel Dosyası Seçin", QMessageBox.StandardButton.Ok)
            else:
                validationFlag = DataValidator(pd.read_excel(filePath)).validate()
                print(validationFlag)
                if validationFlag:
                    self.filePath = filePath
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