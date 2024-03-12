from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import time
from datetime import datetime

# Set the hub URL
grid_url = "http://192.168.56.1:4444/wd/hub"

# Define desired capabilities for Chrome
capabilities = DesiredCapabilities.CHROME.copy()

# Create a remote webdriver instance
driver = webdriver.Remote(command_executor=grid_url, desired_capabilities=capabilities)

baseURL = "https://data.idx.co.id"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(baseURL)
driver.implicitly_wait(5)
driver.maximize_window()       
wait = WebDriverWait(driver, 10)

LoginProfile = driver.find_element(By.XPATH,"//img[@class='user-image']")
LoginProfile.click()

BtnSignIn = driver.find_element(By.XPATH,"//a[normalize-space()='Sign In']")
BtnSignIn.click()

FieldEmail = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='txtUserName']")))
FieldEmail.send_keys("autoreport_adm@sat.co.id")

FieldPass = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='txtPassword']")))
FieldPass.send_keys("Autoadm234ho#")

BtnLogin = driver.find_element(By.XPATH,"//button[normalize-space()='Sign In']")
BtnLogin.click()

MenuIDXData = driver.find_element(By.XPATH,"//span[normalize-space()='IDX Data']")
MenuIDXData.click()

PilihFolder = driver.find_element(By.XPATH, '//a[@href="javascript:GetFileList(\'idx-equity-eod-basic\');"]')

PilihFolder.click()

PilihDataDaily = driver.find_element(By.XPATH,'//a[@href="javascript:GetFileList(\'data-daily\');"]')
PilihDataDaily.click()

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

PageTerakhir = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='2']")))
PageTerakhir.click()

time.sleep(5)

rows = driver.find_elements(By.XPATH, "//tbody/tr")

current_date = '2024-03-01'

for row in rows:
    columns = row.find_elements(By.XPATH, "td")
    file_name = columns[0].text
    file_date = columns[1].text

    if file_date == current_date:
        download_button_xpath = f"//td[text()='{current_date}']/following-sibling::td//button[contains(@onclick, 'DownloadData')]"

        wait = WebDriverWait(driver, 10)
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, download_button_xpath)))

        driver.execute_script("arguments[0].click();", download_button)
        print(f"Download button clicked for the current date {current_date}.")
    else:
        print(f"Skipping file {file_name} as dates do not match.")       

ProfileLogOut = driver.find_element(By.XPATH,"//img[@class='user-image']")
ProfileLogOut.click()

LogOut = driver.find_element(By.XPATH,"//a[normalize-space()='Sign out']")
LogOut.click()

time.sleep(5)
