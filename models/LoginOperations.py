import requests
import json
import uuid

class LoginOperations:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    @staticmethod
    def createBasicUUID():
        random_uuid = uuid.uuid4()
        uuid_str = str(random_uuid).replace('-', '')
        formatted_uuid = uuid_str[:13] + '-1'
        return formatted_uuid

    def loginRequestSender(self, userId, password):
        url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/assos-login'
        data = {
            'assoscmd': 'login',
            'rtype': 'json',
            'userid': userId,
            'sifre': password,
            'parola': password
        }
        """data = {
            'assoscmd': 'anologin',
            'rtype': 'json',
            'userid': userId,
            'sifre': password,
            'sifre2': password,
            'parola': '1'
        }"""
        try:
            response = requests.post(url, data=data, headers=self.headers)
            return response
        except requests.RequestException as e:
            raise ValueError("Error in login request")
    
    def login(self, userId, password):
        response = self.loginRequestSender(userId, password)
        if response.status_code == 200:
            response_json = response.json()
            if 'token' in response_json:
                token = response_json.get('token')
                return token
            else:
                return False
        else:
            return False
        
    def getLoginUserInfo(self, token):
        data = {
            'cmd': 'EARSIV_PORTAL_KULLANICI_ID_GETIR',
            'callid': self.createBasicUUID(),
            'pageName': 'TEST_WELCOME',
            'token': token,
            'jp': {}
        }
        url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/dispatch'
        try:
            response = requests.post(url, data=data, headers=self.headers)
        except requests.RequestException as e:
            raise ValueError("Error in login info")
        if response.status_code == 200:
            response_json = response.json()
            if 'data' in response_json:
                userId = response_json.get('data').get("userId")
                userName = response_json.get('data').get("userName")
                return userId, userName
            else:
                return False, False
        else:
            return False, False
    
    def logout(self, token):
        url = 'https://earsivportaltest.efatura.gov.tr/earsiv-services/assos-login'
        data = {
            'assoscmd': 'logout',
            'rtype': 'json',
            'token': token
        }
        try:
            response = requests.post(url, data=data, headers=self.headers)
        except requests.RequestException as e:
            raise ValueError("Error in login info")
        
        if response.status_code == 200:
            response_json = response.json()
            if 'data' in response_json:
                tokenRemoveFlag = True
                return tokenRemoveFlag
            else:
                return False
        else:
            return False