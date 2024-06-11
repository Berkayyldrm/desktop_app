from PyQt6.QtWidgets import QMessageBox, QApplication, QPushButton

class FailedMessageBox(QMessageBox):
    def __init__(self, failedInvoices, data, parent=None):
        super().__init__(parent)
        self.failedInvoices = failedInvoices
        self.data = data
        self.setWindowTitle("Bazı Faturaları Oluştururken Hata oluştu.")
        self.setText(f"Bazı Faturaları Oluştururken Hata oluştu.{self.failedInvoices}. Bunları excele kaydetmek ister misiniz?")
        self.setIcon(QMessageBox.Icon.Question)

        # Adding custom button
        self.save_button = self.addButton("Save", QMessageBox.ButtonRole.AcceptRole)
        self.cancel_button = self.addButton(QMessageBox.StandardButton.Cancel)
        
        # Connect the Save button to a function
        self.save_button.clicked.connect(self.on_save_clicked)

    def on_save_clicked(self):
        selectedData = self.data.loc[self.failedInvoices]
        selectedData.to_excel('HataliFaturalar.xlsx', index=False)
        print("Save function is executed")
        