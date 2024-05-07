from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""# ChromeDriver'ın yolunu belirtin
driver = webdriver.Firefox()
driver.get('https://earsivportaltest.efatura.gov.tr/login.jsp')


# WebDriverWait nesnesi
wait = WebDriverWait(driver, 10)  # 10 saniye kadar bekleyecek maksimum

# Kullanıcı öneri butonuna tıkla
suggest_user_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formdiv"]/div[3]/div[1]/button[2]')))
suggest_user_button.click()

# Giriş butonuna tıkla
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formdiv"]/div[3]/div[1]/button[1]')))
login_button.click()

# Yeni sayfanın yüklenmesini bekle
wait.until(EC.url_changes('https://earsivportaltest.efatura.gov.tr/login.jsp'))

# Yeni sayfanın URL'sini al ve yazdır
current_url = driver.current_url
print(current_url)

# İşlemlerden sonra tarayıcıyı kapat
driver.quit()"""

from DesktopSelenium import DesktopSelenium
desktopSelenium = DesktopSelenium()

urlWithToken = desktopSelenium.connectTestAccount()
print(urlWithToken)
desktopSelenium.closeConnection()