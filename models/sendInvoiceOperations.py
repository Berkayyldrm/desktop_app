import requests
import json

class sendInvoiceOperations:
    def __init__(self):
        self.url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/dispatch'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.invoice_template = {
                "faturaUuid":"",
                "belgeNumarasi":"",
                "faturaTarihi":"05/06/2024",
                "saat":"22:06:53",
                "paraBirimi":"TRY",
                "dovzTLkur":"0",
                "faturaTipi":"SATIS",
                "hangiTip":"5000/30000",
                "vknTckn":"11111111111",
                "aliciUnvan":"",
                "aliciAdi":"test",
                "aliciSoyadi":"ttt",
                "binaAdi":"",
                "binaNo":"",
                "kapiNo":"",
                "kasabaKoy":"",
                "vergiDairesi":"",
                "ulke":"Türkiye",
                "bulvarcaddesokak":"",
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
                "malHizmetTable":[{"malHizmet":"x",
                                   "miktar":0,
                                   "birim":"DAY",
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
                                   "hesaplananotvtevkifatakatkisi":"0"}],
                "tip":"İskonto",
                "matrah":"0",
                "malhizmetToplamTutari":"0",
                "toplamIskonto":"0",
                "hesaplanankdv":"0",
                "vergilerToplami":"0",
                "vergilerDahilToplamTutar":"0",
                "odenecekTutar":"500",
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

    def sendInvoice(self, token, invoice_data):
        data = {
            'cmd': 'EARSIV_PORTAL_FATURA_OLUSTUR',
            'callid': '2137eacd32633-9',
            'pageName': 'RG_BASITFATURA',
            'token': token,
            'jp': json.dumps(invoice_data, indent=4)
        }

        response = requests.post(self.url, data=data, headers=self.headers)
        return response.text

    def create_invoice_data(self, row):
        # Merge row with the template, row values will override template values
        invoice_data = {**self.invoice_template, **row.to_dict()}
        return invoice_data