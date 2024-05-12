from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DesktopSelenium():
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.loginUrl = "https://earsivportaltest.efatura.gov.tr/login.jsp"
        self.xpathMap = {
            'VKN/TCKN': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/fieldset/table/tr[1]/td[2]/input',
            'Ünvan': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/fieldset/table/tr[2]/td[2]/input',
            'Adi': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/fieldset/table/tr[3]/td[2]/input',
            'Soyadi': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/fieldset/table/tr[4]/td[2]/input',
            'Ülke': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/fieldset/table/tr[6]/td[2]/select',
            'Mal/Hizmet': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div[1]/fieldset/table/tr[1]/td[2]/input',
            'Miktar': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div[1]/fieldset/table/tr[2]/td[2]/input',
            'Birim': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div[1]/fieldset/table/tr[3]/td[2]/select',
            'Birim Fiyati': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div[1]/fieldset/table/tr[4]/td[2]/input',
            'İskonto Orani': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div[1]/fieldset/table/tr[5]/td[2]/input',
            'İskonto Tutari': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div[1]/fieldset/table/tr[6]/td[2]/input',
            'KDV Orani': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div[1]/fieldset/table/tr[8]/td[2]/select',
            'Ödenecek Tutar': '/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[4]/div/div/fieldset/div/div/div/div/table/tr[2]/td[2]/div/table/tr[2]/td[2]/input'
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
    
    def clickElements(self, wait, xpathValue):
        element = self.driver.find_element(By.XPATH, xpathValue)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpathValue)))
        element.click()
    
    def sendKeyElements(self, wait, xpathValue, sendKeys):
        element = wait.until(EC.visibility_of_element_located((By.XPATH, xpathValue)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.send_keys(sendKeys)

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

        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("VKN/TCKN"), sendKeys="11111111111")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Ünvan"), sendKeys="")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Adi"), sendKeys="Mehmet")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Soyadi"), sendKeys="Yilmaz")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Ülke"), sendKeys="Türkiye")

        self.clickElements(wait=wait, xpathValue='/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[3]/div/div/fieldset/div/div[3]/div/div/div/div[1]/div/div/input')
        self.clickElements(wait=wait, xpathValue='/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[3]/div/div/fieldset/div/div[2]/div/div/table/tbody/tr[1]/td[3]/div/input')

        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Mal/Hizmet"), sendKeys="Yazilim Hizmeti")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Miktar"), sendKeys="1")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Birim"), sendKeys="Adet")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Birim Fiyati"), sendKeys="100")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("İskonto Orani"), sendKeys="5")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("İskonto Tutari"), sendKeys="10")
        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("KDV Orani"), sendKeys="20")

        self.clickElements(wait=wait, xpathValue='/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div[2]/fieldset/table/tr/td[2]/div/input')

        self.sendKeyElements(wait=wait, xpathValue=self.xpathMap.get("Ödenecek Tutar"), sendKeys="500")

        self.clickElements(wait=wait, xpathValue='/html/body/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div[6]/div/div/div/div[1]/div/div/div/div/div/div/input')

    def closeConnection(self):
        self.driver.quit()

