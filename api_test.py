import requests
import json
import uuid

def createBasicUUID():
    random_uuid = uuid.uuid4()
    uuid_str = str(random_uuid).replace('-', '')
    formatted_uuid = uuid_str[:13] + '-1'
    return formatted_uuid

def createUUID():
    random_uuid = uuid.uuid4()
    formatted_uuid = str(random_uuid)
    return formatted_uuid

# Endpoint URL
url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/assos-login'
#url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/assos-login'
# Data to be sent
data = {
    'assoscmd': 'login',
    'rtype': 'json',
    'userid': '33333305',
    'sifre': '1',
    'parola': '1'
}
"""data = {
    'assoscmd': 'anologin',
    'rtype': 'json',
    'userid': '1',
    'sifre': '1',
    'sifre2': '1',
    'parola': '1'
}"""

# Set the headers as necessary
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# Send the POST request
response = requests.post(url, data=data, headers=headers)
print(response)
# Print the response from server
print(response.json())


token = response.json().get("token")
print(token)



print("########################")

data = {
    'cmd': 'EARSIV_PORTAL_KULLANICI_ID_GETIR',
    'callid': createBasicUUID(),
    'pageName': 'TEST_WELCOME',
    'token': token,
    'jp': {}
}

# Send the POST request
url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/dispatch'
response = requests.post(url, data=data, headers=headers)
print(response)
# Print the response from server
print(response.text)



print("#############")
"""url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/assos-login'

# Data to be sent
data = {
    'assoscmd': 'logout',
    'rtype': 'json',
    'token': token
}

# Set the headers as necessary
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# Send the POST request
response = requests.post(url, data=data, headers=headers)
print(response)
# Print the response from server
print(response.json())"""

print("#############")
url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/dispatch'
headers = {
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
print(createUUID())
invoice_template = {
    "faturaUuid":createUUID(),
    "belgeNumarasi":"",
    "faturaTarihi":"08/06/2024",
    "saat":"22:06:53",
    "paraBirimi":"TRY",
    "dovzTLkur":"0",
    "faturaTipi":"SATIS",
    "hangiTip":"5000/30000",
    "vknTckn":"11111111111",
    "aliciUnvan":"",
    "aliciAdi":"test",
    "aliciSoyadi":"RAMPES",
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

data = {
            'cmd': 'EARSIV_PORTAL_FATURA_OLUSTUR',
            'callid': createBasicUUID(),
            'pageName': 'RG_BASITFATURA',
            'token': token,
            'jp': json.dumps(invoice_template, indent=4)
        }
print(data)
import json
with open('data200.json', 'w') as f:
    json.dump(data, f, indent=4)
#44b18e59-21ee-4475-aca8-b41af0056e0f

response = requests.post(url, data=data, headers=headers)
print(response)
# Print the response from server
print(response.text)


print("################################")

"""url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/dispatch'

data_to_insert = {"baslangic":"01/06/2024","bitis":"09/06/2024","hangiTip":"5000/30000"}

data = {
    'cmd': 'EARSIV_PORTAL_TASLAKLARI_GETIR',
    'callid': createBasicUUID(),
    'pageName': 'RG_BASITTASLAKLAR',
    'token': token,
    'jp': json.dumps(data_to_insert, indent = 4) 
}

# Set the headers as necessary
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# Send the POST request
response = requests.post(url, data=data, headers=headers)

print(response)
# Print the response from server
print(response.text)"""