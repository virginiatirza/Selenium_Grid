from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
from datetime import datetime

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

## Find all rows in the table
rows = driver.find_elements(By.XPATH, "//tbody/tr")

# Get the current date
# current_date = datetime.now().strftime("%Y-%m-%d")
# print(current_date)

current_date = '2024-03-01'
# Iterate through each row
for row in rows:
    # Extract data from each column in the row
    columns = row.find_elements(By.XPATH, "td")
    file_name = columns[0].text
    file_date = columns[1].text

    # if file_date == current_date:
    #     # Extract the button element from the row
    #     download_button = row.find_element(By.XPATH, ".//button[contains(@onclick, 'DownloadData')]")

    #     # Scroll the page to make the button visible
    #     driver.execute_script("arguments[0].scrollIntoView(true);", download_button)

    #     # Wait for the button to be clickable
    #     wait = WebDriverWait(driver, 10)
    #     download_button = wait.until(EC.element_to_be_clickable((By.XPATH, ".//button[contains(@onclick, 'DownloadData')]")))

    #     # Use JavaScript to click the button
    #     driver.execute_script("arguments[0].click();", download_button)
    #     print(f"File {file_name} download triggered for date {file_date}.")
    # else:
    #     print(f"Skipping file {file_name} as dates do not match.")

    if file_date == current_date:
        # Locate the button in the row with the current date
        download_button_xpath = f"//td[text()='{current_date}']/following-sibling::td//button[contains(@onclick, 'DownloadData')]"

        # Wait for the button to be clickable
        wait = WebDriverWait(driver, 10)
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, download_button_xpath)))

        # Use JavaScript to click the button
        driver.execute_script("arguments[0].click();", download_button)
        print(f"Download button clicked for the current date {current_date}.")
    else:
        print(f"Skipping file {file_name} as dates do not match.")       

ProfileLogOut = driver.find_element(By.XPATH,"//img[@class='user-image']")
ProfileLogOut.click()

LogOut = driver.find_element(By.XPATH,"//a[normalize-space()='Sign out']")
LogOut.click()

time.sleep(5)
