import requests
import json
# Endpoint URL
url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/dispatch'

data_to_insert = {
    "faturaUuid":"8d0ce067-e597-4796-8b0f-941335a7b877","belgeNumarasi":"","faturaTarihi":"05/06/2024","saat":"22:06:53",
    "paraBirimi":"TRY","dovzTLkur":"0","faturaTipi":"SATIS","hangiTip":"5000/30000","vknTckn":"11111111111","aliciUnvan":"",
    "aliciAdi":"test","aliciSoyadi":"ttt","binaAdi":"","binaNo":"","kapiNo":"","kasabaKoy":"","vergiDairesi":"","ulke":"Türkiye",
    "bulvarcaddesokak":"","irsaliyeNumarasi":"","irsaliyeTarihi":"","mahalleSemtIlce":"","sehir":" ","postaKodu":"","tel":"","fax":"",
    "eposta":"","websitesi":"","iadeTable":[],"vergiCesidi":" ",
    "malHizmetTable":[{"malHizmet":"x","miktar":0,"birim":"DAY","birimFiyat":"0","fiyat":"0","iskontoOrani":0,"iskontoTutari":"0",
                       "iskontoNedeni":"","malHizmetTutari":"0","vergiOrani":0,"kdvTutari":"0","vergininKdvTutari":"0","ozelMatrahTutari":"0",
                       "hesaplananotvtevkifatakatkisi":"0"}],
    "tip":"İskonto","matrah":"0","malhizmetToplamTutari":"0","toplamIskonto":"0",
    "hesaplanankdv":"0","vergilerToplami":"0","vergilerDahilToplamTutar":"0","odenecekTutar":"500","not":"",
    "siparisNumarasi":"","siparisTarihi":"","fisNo":"","fisTarihi":"","fisSaati":" ","fisTipi":" ","zRaporNo":"","okcSeriNo":""}

# Data to be sent
data = {
    'cmd': 'EARSIV_PORTAL_FATURA_OLUSTUR',
    'callid': '6b41511340cf4-15',
    'pageName': 'RG_BASITFATURA',
    'token': '7b8c1066ce2cf73c3010c822d35cea4a5a9bdb49a4582242eb0b8c76da435eb5bfd3b21f3df1d9e69c03a3dc352c027412818b61807f5be5d9ec0ef3390479a9',
    'jp': json.dumps(data_to_insert, indent = 4) 
}

# Set the headers as necessary
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# Send the POST request
response = requests.post(url, data=data, headers=headers)

# Print the response from server
print(response.text)
