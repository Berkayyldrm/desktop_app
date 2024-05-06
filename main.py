from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
import sys
from PyQt6.QtWidgets import QFileDialog, QLabel, QPushButton

ui_path = "./ui/"
#logo_file = "path/to/your/logo.png"  # Logo dosyasının yolu

class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        loadUi(f"{ui_path}main.ui", self)
        self.setupUI()

    def setupUI(self):
        
        self.openFileButton = self.findChild(QPushButton, 'filePathButton')  # QPushButton adını UI dosyanızdaki ile değiştirin
        self.filePathLabel = QLabel("Dosya yolu burada görünecek", self)
        self.openFileButton.clicked.connect(self.openFileDialog)

    def openFileDialog(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Tüm Dosyalar (*);;Metin Dosyaları (*.txt)")
        print(filePath)
        if filePath:
            self.filePathBrowser.setText(filePath)

app = QApplication(sys.argv)
mainwindow = Main()
#app_icon = QIcon(logo_file)
#app.setWindowIcon(app_icon)
widget = QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedSize(1500, 1500)  # Eğer boyutu sabit olarak ayarlamak isterseniz
widget.show()
app.exec()