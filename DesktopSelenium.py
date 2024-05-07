from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DesktopSelenium():
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.loginUrl = "https://earsivportaltest.efatura.gov.tr/login.jsp"
        
    def connectTestAccount(self):
        self.driver.get(self.loginUrl)
        wait = WebDriverWait(self.driver, 10)  # 10 saniye kadar bekleyecek maksimum
        suggest_user_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formdiv"]/div[3]/div[1]/button[2]')))
        suggest_user_button.click()
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formdiv"]/div[3]/div[1]/button[1]')))
        login_button.click()
        wait.until(EC.url_changes(self.loginUrl))

        current_url = self.driver.current_url
        return current_url
    
    def closeConnection(self):
        self.driver.quit()

