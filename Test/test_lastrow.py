from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

grid_url = "http://192.168.56.1:4444/wd/hub"

capabilities = DesiredCapabilities.CHROME.copy()

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

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# pagination = driver.find_element(By.ID, "tblReport_paginate")

# next_button = pagination.find_element(By.CLASS_NAME, "next")

# while True:rr
#     try:
#         actions = ActionChains(driver)
#         actions.move_to_element(next_button).perform()

#         driver.execute_script("arguments[0].click();", next_button)

#     except Exception as e:
#         print(f"Error clicking 'Next' button: {e}")
#         break

# Find the pagination element
pagination = driver.find_element(By.ID, "tblReport_paginate")

# Get the "Next" button within the pagination
next_button = pagination.find_element(By.CLASS_NAME, "next")

while True:
    try:
        # Scroll the page to make the button visible
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

        # Use JavaScript to click the "Next" button
        driver.execute_script("arguments[0].click();", next_button)

        # You may want to wait for the table to load or perform any other necessary actions here

    except:
        print(f"Error clicking 'Next' button:")
        break

# time.sleep(5)

rows = driver.find_elements(By.XPATH, "//tbody/tr")

last_row = rows[-1]

download_button = last_row.find_element(By.XPATH, ".//button[contains(@onclick, 'DownloadData')]")

actions = ActionChains(driver)
actions.move_to_element(download_button).perform()

overlay_element = driver.find_element(By.XPATH, "//a[@class='dropdown-toggle']")
wait.until_not(EC.staleness_of(overlay_element))

driver.execute_script("arguments[0].click();", download_button)

time.sleep(3)

ProfileLogOut = driver.find_element(By.XPATH,"//img[@class='user-image']")
ProfileLogOut.click()

LogOut = driver.find_element(By.XPATH,"//a[normalize-space()='Sign out']")
LogOut.click()

time.sleep(3)

print(driver.title)

driver.quit()