import requests
import json
# Endpoint URL
url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/dispatch'

data_to_insert = {"baslangic":"08/06/2024","bitis":"08/06/2024","hangiTip":"5000/30000"}

# Data to be sent
data = {
    'cmd': 'EARSIV_PORTAL_TASLAKLARI_GETIR',
    'callid': '2a91866586e24-7',
    'pageName': 'RG_BASITTASLAKLAR',
    'token': 'db71ccaadc695887da20e944e581eb9e94074b7e2f6f53eeae2288790ee808e51a940084665f87c03affe74cca97af246b3a39040604b3ce0f26f191260cb20b',
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
