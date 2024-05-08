from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DesktopSelenium():
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.loginUrl = "https://earsivportaltest.efatura.gov.tr/login.jsp"
        self.xpathMap = {'VKN/TCKN': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/fieldset/table/tr[1]/td[2]/input',
                    'Ülke': '//*[@id="gen__1746"]',
                    'Mal/Hizmet': '//*[@id="gen__1831"]',
                    'Miktar': '',
                    'Birim': '',
                    'Birim Fiyatı': '',
                    'İskonto Oranı': '',
                    'İskonto Tutarı': '',
                    'KDV Oranı': '',
                    'KDV Tutarı': '',
                    'Ödenecek Tutar': ''
                    }   
        
    def connectTestAccount(self):
        self.driver.get(self.loginUrl)
        wait = WebDriverWait(self.driver, 10)  # 10 saniye kadar bekleyecek maksimum
        suggestUserButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formdiv"]/div[3]/div[1]/button[2]')))
        suggestUserButton.click()
        loginButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formdiv"]/div[3]/div[1]/button[1]')))
        loginButton.click()
        wait.until(EC.url_changes(self.loginUrl))

        current_url = self.driver.current_url
        return current_url
    
    def createInvoice(self):
        wait = WebDriverWait(self.driver, 10)  # 10 saniye kadar bekleyecek maksimum
        selectModule = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gen__1006"]')))
        selectModule.click()
        selectModule2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gen__1006"]/option[2]')))
        selectModule2.click()
        selectModule3 = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div/ul/li[2]/a')))
        selectModule3.click()
        selectModule4 = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div/ul/li[2]/ul/li[5]/a')))
        selectModule4.click()
        input_element = wait.find_element(By.XPATH, self.xpathMap.get("VKN/TCKN"))
        input_element.send_keys('test')
        
    def closeConnection(self):
        self.driver.quit()

