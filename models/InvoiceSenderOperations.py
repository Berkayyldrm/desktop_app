import requests
import json
from datetime import datetime
import uuid
"""
{
"malHizmet":"x",
"miktar":0,
"birim":"",
"birimFiyat":"0",
"fiyat":"0",
"iskontoOrani":0,
"iskontoTutari":"0",
"iskontoNedeni":"",
"malHizmetTutari":"0",
"vergiOrani":0,
"kdvTutari":"0",
"vergininKdvTutari":"0",
"ozelMatrahTutari":"0",
"hesaplananotvtevkifatakatkisi":"0"
}
"""
class InvoiceSenderOperations:
    def __init__(self):
        self.url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/dispatch'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.invoice_template = {
                "faturaUuid":"",
                "belgeNumarasi":"",
                "faturaTarihi":"",
                "saat":"",
                "paraBirimi":"TRY",
                "dovzTLkur":"0",
                "faturaTipi":"SATIS",
                "hangiTip":"5000/30000",
                "vknTckn":"",
                "aliciUnvan":"",
                "aliciAdi":"",
                "aliciSoyadi":"",
                "binaAdi":"",
                "binaNo":"",
                "kapiNo":"",
                "kasabaKoy":"",
                "vergiDairesi":"",
                "ulke":"Türkiye",
                "bulvarcaddesokak":"", #Adres için sadece bu kulanılıyor.
                "irsaliyeNumarasi":"",
                "irsaliyeTarihi":"",
                "mahalleSemtIlce":"",
                "sehir":" ",
                "postaKodu":"",
                "tel":"",
                "fax":"",
                "eposta":"",
                "websitesi":"",
                "iadeTable":[],
                "vergiCesidi":" ",
                "malHizmetTable":[],
                "tip":"İskonto",
                "matrah":"0",
                "malhizmetToplamTutari":"0",
                "toplamIskonto":"0",
                "hesaplanankdv":"0",
                "vergilerToplami":"0",
                "vergilerDahilToplamTutar":"0",
                "odenecekTutar":"",
                "not":"",
                "siparisNumarasi":"",
                "siparisTarihi":"",
                "fisNo":"",
                "fisTarihi":"",
                "fisSaati":" ",
                "fisTipi":" ",
                "zRaporNo":"",
                "okcSeriNo":""
                }
        self.malHizmetTableTemplate = {
            "malHizmet":"x",
            "miktar":0,
            "birim":"",
            "birimFiyat":"0",
            "fiyat":"0",
            "iskontoOrani":0,
            "iskontoTutari":"0",
            "iskontoNedeni":"",
            "malHizmetTutari":"0",
            "vergiOrani":0,
            "kdvTutari":"0",
            "vergininKdvTutari":"0",
            "ozelMatrahTutari":"0",
            "hesaplananotvtevkifatakatkisi":"0"
            }
        
    def createBasicUUID(self):
        random_uuid = uuid.uuid4()
        uuid_str = str(random_uuid).replace('-', '')
        formatted_uuid = uuid_str[:13] + '-1'
        return formatted_uuid

    def createUUID(self):
        random_uuid = uuid.uuid4()
        formatted_uuid = str(random_uuid)
        return formatted_uuid

    def sendInvoiceRequest(self, token, invoice_data):
        data = {
            'cmd': 'EARSIV_PORTAL_FATURA_OLUSTUR',
            'callid': self.createBasicUUID(),
            'pageName': 'RG_BASITFATURA',
            'token': token,
            'jp': json.dumps(invoice_data, indent=4)
        }
        
        with open('dataerr.json', 'w') as f:
            json.dump(data, f)
        response = requests.post(self.url, data=data, headers=self.headers)
        return response.text
    
    def createInvoice(self, data, token):
        updatedInvoice = self.invoice_template.copy()
        updatedMalHizmetTableTemplate = self.malHizmetTableTemplate.copy()

        now = datetime.now()
        updatedInvoice["faturaUuid"] = self.createUUID()
        updatedInvoice["faturaTarihi"] = now.strftime("%d/%m/%Y")
        updatedInvoice["saat"] = now.strftime("%H:%M:%S")

        updatedInvoice["vknTckn"] = data.get("VKN/TCKN")
        updatedInvoice["aliciUnvan"] = data.get("ALICI ÜNVAN")
        updatedInvoice["aliciAdi"] = data.get("ALICI")
        updatedInvoice["aliciSoyadi"] = data.get("ALICI SOYADI")

        updatedInvoice["vergiDairesi"] = data.get("VERGİ DAİRESİ")
        updatedInvoice["bulvarcaddesokak"] = data.get("FATURA ADRESİ")

        malHizmetTableCount = 1
        updatedMalHizmetTableTemplate["malHizmet"] = data.get("ÜRÜN ADI")
        updatedMalHizmetTableTemplate["miktar"] = data.get("MİKTAR")
        updatedMalHizmetTableTemplate["birimFiyat"] = data.get("BİRİM FİYATI")
        updatedMalHizmetTableTemplate["iskontoOrani"] = data.get("İSKONTO ORANI")
        updatedMalHizmetTableTemplate["iskontoTutari"] = data.get("İSKONTO TUTARI")
        updatedMalHizmetTableTemplate["malHizmetTutari"] = data.get("SATIŞ TUTARI(KDV HARİÇ)")
        updatedMalHizmetTableTemplate["vergiOrani"] = data.get("KDV ORANI")
        updatedMalHizmetTableTemplate["kdvTutari"] = data.get("KDV TUTARI")

        updatedInvoice["malHizmetTable"].append(updatedMalHizmetTableTemplate)

        updatedInvoice["odenecekTutar"] = data.get("FATURALANACAK TUTAR")

        responseText = self.sendInvoiceRequest(invoice_data=updatedInvoice, token=token)
        return responseText


