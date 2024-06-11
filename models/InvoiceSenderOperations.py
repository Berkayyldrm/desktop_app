import requests
import json
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

PORTAL_TYPE = os.environ.get("PORTAL_TYPE")

class InvoiceSenderOperations:
    def __init__(self):
        self.baseUrl = ""
        if PORTAL_TYPE == "Test":
            self.baseUrl = "https://earsivportaltest.efatura.gov.tr"
        elif PORTAL_TYPE == "Prod":
            self.baseUrl = "https://earsivportal.efatura.gov.tr"
        self.url = f'{self.baseUrl}/earsiv-services/dispatch'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        
        
    def createTemplates(self):
        invoice_template = {
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
        malHizmetTableTemplate = {
            "malHizmet":"",
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
        return invoice_template, malHizmetTableTemplate
    
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
        
        try:
            response = requests.post(self.url, data=data, headers=self.headers)
        except requests.RequestException as e:
            raise ValueError("Error Sending Invoice")
        return response
    
    def createInvoice(self, data, token):
        invoice_template, malHizmetTableTemplate = self.createTemplates()
        updatedInvoice = invoice_template

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

        if not isinstance(data.get("ÜRÜN ADI"), list):
            updatedMalHizmetTableTemplate = malHizmetTableTemplate.copy()
            updatedMalHizmetTableTemplate["malHizmet"] = data.get("ÜRÜN ADI")
            updatedMalHizmetTableTemplate["miktar"] = data.get("MİKTAR")
            updatedMalHizmetTableTemplate["birimFiyat"] = data.get("BİRİM FİYATI")
            updatedMalHizmetTableTemplate["iskontoOrani"] = data.get("İSKONTO ORANI")
            updatedMalHizmetTableTemplate["iskontoTutari"] = data.get("İSKONTO TUTARI")
            updatedMalHizmetTableTemplate["malHizmetTutari"] = data.get("SATIŞ TUTARI(KDV HARİÇ)")
            updatedMalHizmetTableTemplate["vergiOrani"] = data.get("KDV ORANI")
            updatedMalHizmetTableTemplate["kdvTutari"] = data.get("KDV TUTARI")
            updatedInvoice["malHizmetTable"].append(updatedMalHizmetTableTemplate)

        elif isinstance(data.get("ÜRÜN ADI"), list):
            for i in range(len(data.get("ÜRÜN ADI"))):
                updatedMalHizmetTableTemplate = malHizmetTableTemplate.copy()
                updatedMalHizmetTableTemplate["malHizmet"] = data.get("ÜRÜN ADI")[i]
                updatedMalHizmetTableTemplate["miktar"] = data.get("MİKTAR")[i]
                updatedMalHizmetTableTemplate["birimFiyat"] = data.get("BİRİM FİYATI")[i]
                updatedMalHizmetTableTemplate["iskontoOrani"] = data.get("İSKONTO ORANI")[i]
                updatedMalHizmetTableTemplate["iskontoTutari"] = data.get("İSKONTO TUTARI")[i]
                updatedMalHizmetTableTemplate["malHizmetTutari"] = data.get("SATIŞ TUTARI(KDV HARİÇ)")[i]
                updatedMalHizmetTableTemplate["vergiOrani"] = data.get("KDV ORANI")[i]
                updatedMalHizmetTableTemplate["kdvTutari"] = data.get("KDV TUTARI")[i]
                updatedInvoice["malHizmetTable"].append(updatedMalHizmetTableTemplate)

        updatedInvoice["odenecekTutar"] = data.get("FATURALANACAK TUTAR")
        
        response = self.sendInvoiceRequest(invoice_data=updatedInvoice, token=token)

        if response.status_code == 200:
            response_json = response.json()
            if 'data' in response_json:
                if response_json["data"] == "Faturanız başarıyla oluşturulmuştur. Düzenlenen Belgeler menüsünden faturanıza ulaşabilirsiniz.":
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False