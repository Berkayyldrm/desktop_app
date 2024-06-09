import pandas as pd
from PyQt6.QtWidgets import QMessageBox
class DataValidator:
    def __init__(self, dataframe, parent=None):
        self.df = dataframe
        self.parent = parent  # This should be the main window or relevant QWidget

    def validate(self):
        results = {}
        validations = {
            'ALICI': lambda x: isinstance(x, str) or pd.isna(x),
            'ALICI SOYADI': lambda x: isinstance(x, str) or pd.isna(x),
            'ALICI ÜNVAN': lambda x: isinstance(x, str) or pd.isna(x),
            'VKN/TCKN': lambda x: isinstance(x, int) or isinstance(x, str),
            'VERGİ DAİRESİ': lambda x: isinstance(x, str), #boş olabilir
            'FATURA ADRESİ': lambda x: isinstance(x, str), # boş olamaz
            'ÜRÜN ADI': lambda x: isinstance(x, str), # boş olamaz
            'BİRİM': lambda x: pd.isna(x) or isinstance(x, str), # boş olamaz
            'MİKTAR': lambda x: isinstance(x, int) or isinstance(x, float), # boş olamaz
            'BİRİM FİYATI': lambda x: isinstance(x, int) or isinstance(x, float), # boş olamaz
            'İSKONTO ORANI': lambda x: isinstance(x, int) or isinstance(x, float),# boş olabilir boş ise default 0
            'İSKONTO TUTARI': lambda x: isinstance(x, int) or isinstance(x, float), # boş olabilir boş ise default 0
            'SATIŞ TUTARI(KDV HARİÇ)': lambda x: isinstance(x, int) or isinstance(x, float), #boş olaamaz
            'KDV ORANI': lambda x: isinstance(x, int) or isinstance(x, float), #boş olaamaz 1 10 20
            'KDV TUTARI': lambda x: isinstance(x, int) or isinstance(x, float), # GEREK YOK
            'FATURALANACAK TUTAR': lambda x: isinstance(x, int) or isinstance(x, float) # GEREK YOK
        }
        failed_columns = []
        for column, validate_func in validations.items():
            if not self.df[column].apply(validate_func).all():
                failed_columns.append(column)

        # Complex row-based validation rules
        def row_based_validation(row):
            if (pd.isna(row['ALICI']) or row['ALICI'].strip() == '') and (pd.isna(row['ALICI SOYADI']) or row['ALICI SOYADI'].strip() == ''):
                if pd.isna(row['ALICI ÜNVAN']) or row['ALICI ÜNVAN'].strip() == '':
                    return False
            if pd.isna(row['ALICI ÜNVAN']) or row['ALICI ÜNVAN'].strip() == '':
                if (pd.isna(row['ALICI']) or row['ALICI'].strip() == '') and (pd.isna(row['ALICI SOYADI']) or row['ALICI SOYADI'].strip() == ''):
                    return False
            return True

        invalid_rows = self.df.apply(row_based_validation, axis=1)
        if not invalid_rows.all():
            failed_rows = invalid_rows[invalid_rows == False].index.tolist()
            warning_msg = f"Row-based validation failed for rows: {failed_rows}"
            QMessageBox.warning(self.parent, "Validation Error", warning_msg, QMessageBox.StandardButton.Ok)
            return False
        return True