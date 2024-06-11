from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
import sys
from PyQt6.QtWidgets import QFileDialog, QLabel, QPushButton
import pandas as pd
from DisplayInvoices import DisplayInvoices
ui_path = "./ui/"
#logo_file = "path/to/your/logo.png"  # Logo dosyasının yolu
from models.DataValidator import DataValidator
from models.InvoiceSenderOperations import InvoiceSenderOperations
from models.LoginOperations import LoginOperations
from PyQt6.QtWidgets import QMessageBox
from models.CustomMessageBox import FailedMessageBox
import numpy as np
class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        loadUi(f"{ui_path}main.ui", self)
        self.setupUI()
        self.loginOperations = LoginOperations()
        self.InvoiceSenderOperations = InvoiceSenderOperations()
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
        self.filePathName.textChanged.connect(self.excelOperations)
        self.createInvoiceButton.clicked.connect(self.createInvoice)
        self.displayInvoicesButton.clicked.connect(self.displayInvoicesScreen)
    
    def loginFunction(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        token, response = self.loginOperations.login(username, password)
        if token:
            self.token = token
            self.userId, self.userName = self.loginOperations.getLoginUserInfo(self.token)
            self.loginValidation = True
            QMessageBox.information(None, "Login Succesfully", f"Giriş yapıldı. {self.userId}, {self.userName}", QMessageBox.StandardButton.Ok)
        else:
            print(response.text)
            QMessageBox.warning(None, "Login Error", "Kullanıcı adı veya şifre hatalı. Veya sistemsel bir hata bulunuyor.", QMessageBox.StandardButton.Ok)
        
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

    def groupedInvoiceOperation(self, df):
        def custom_agg(x):
            if len(x) == 1:
                result = x.iloc[0]
            else:
                result = x.tolist()
            
            if isinstance(result, np.integer):
                return int(result)
            
            if isinstance(result, list):
                return [int(item) if isinstance(item, np.integer) else item for item in result]

            return result
            
        custom_agg_columns = ['ÜRÜN ADI', 'BİRİM', 'MİKTAR', 'BİRİM FİYATI', 'İSKONTO ORANI', 'İSKONTO TUTARI', 'SATIŞ TUTARI(KDV HARİÇ)', 'KDV ORANI', 'KDV TUTARI']
        other_agg_columns = {"ALICI": "first", "ALICI SOYADI": "first", "ALICI ÜNVAN": "first", 
                             "VERGİ DAİRESİ": "first", "FATURA ADRESİ": "first", "FATURALANACAK TUTAR": "sum"}
        agg_dict = {col: custom_agg for col in custom_agg_columns}
        agg_dict.update(other_agg_columns)

        groupedDf = df.groupby('VKN/TCKN').agg(agg_dict).reset_index()

        return groupedDf       

    def createInvoice(self):
        if self.invoiceTypeComboBox.currentText() == "Her Satır Ayrı Fatura":
            invoiceData = self.data
        else:
            invoiceData = self.groupedInvoiceOperation(df=self.data)

        failedInvoices = []
        if isinstance(invoiceData, pd.DataFrame) and self.loginValidation:
            for index, row in invoiceData.iterrows():
                response = self.InvoiceSenderOperations.createInvoice(data=row, token=self.token)
                self.progressBar.setValue(int((index + 1) / len(invoiceData) * 100))
                if response == True:
                    pass
                else:
                    failedInvoices.append(index)

        else:
            QMessageBox.information(None, "Fatura Oluşturulamadı", "Veri Ekleyiniz Ve/Veya Giriş Yapınız.", QMessageBox.StandardButton.Ok)
        
        if not failedInvoices:
            QMessageBox.information(None, "Fatura Oluşturuldu", "Fatura Oluşturma İşlemi Başarıyla Gerçekleşti.", QMessageBox.StandardButton.Ok)
            self.progressBar.setValue(0)
        else:
            FailedMessageBox(failedInvoices=failedInvoices, data=invoiceData).exec()
            self.progressBar.setValue(0)

    def openFileDialog(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", "", 
                                                "Excel Files (*.xls *.xlsx);;All Files (*)")
        if filePath:
            if not (filePath.endswith('.xls') or filePath.endswith('.xlsx')):
                QMessageBox.warning(self, "Dosya Formatı Hatası", "Excel Dosyası Seçin", QMessageBox.StandardButton.Ok)
            else:
                validationFlag = DataValidator(pd.read_excel(filePath)).validate()
                if validationFlag:
                    self.filePath = filePath
                    self.filePathName.setText(self.filePath)            

    def excelOperations(self):
        self.data = pd.read_excel(self.filePath)
        self.data = self.data.fillna("")
        self.rowCountText.setText(str(len(self.data))) 
        dataShort = self.data[["ALICI", "ALICI SOYADI", "ALICI ÜNVAN", "VKN/TCKN", "ÜRÜN ADI", "SATIŞ TUTARI(KDV HARİÇ)"]]
        self.mainDataTable.setRowCount(len(dataShort))
        self.mainDataTable.setColumnCount(len(dataShort.columns))
        self.mainDataTable.setHorizontalHeaderLabels(dataShort.columns)
        self.mainDataTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Adjust specific column by index

        for i in range(len(dataShort)):
            for j in range(len(dataShort.columns)):
                value = dataShort.iloc[i, j]
                if pd.isna(value):
                    self.mainDataTable.setItem(i, j, QTableWidgetItem(""))
                else:
                    self.mainDataTable.setItem(i, j, QTableWidgetItem(str(value)))

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