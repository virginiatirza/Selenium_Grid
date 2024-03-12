from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytest
from datetime import datetime
from selenium.webdriver.chrome.options import Options

options = Options()

grid_url = "http://10.4.6.233:4444"
driver = webdriver.Remote(command_executor=grid_url, options=options)

try:
    baseURL = "https://data.idx.co.id"
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

    # print(f"Title on {browser} {version} - {platform}: {driver.title}")

    MenuIDXData = driver.find_element(By.XPATH,"//span[normalize-space()='IDX Data']")
    MenuIDXData.click()

    PilihFolder = driver.find_element(By.XPATH, '//a[@href="javascript:GetFileList(\'idx-equity-eod-basic\');"]')
    PilihFolder.click()

    PilihDataDaily = driver.find_element(By.XPATH,'//a[@href="javascript:GetFileList(\'data-daily\');"]')
    PilihDataDaily.click()

    time.sleep(3)

    pagination = driver.find_element(By.ID, "tblReport_paginate")

    while True:
        # Locate the "Next" button
        next_button = pagination.find_element(By.CLASS_NAME, "next")

        # Check if the "Next" button is disabled
        if "disabled" in next_button.get_attribute("class"):
            print("Next button is disabled. Exiting loop.")
            break

        # Scroll into view and click the "Next" button
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        next_button.click()

        # Optional: Add a delay to allow the content to load before the next iteration
        time.sleep(2)

    rows = driver.find_elements(By.XPATH, "//tbody/tr")

    last_row = rows[-1]

    download_button = last_row.find_element(By.XPATH, ".//button[contains(@onclick, 'DownloadData')]")

    actions = ActionChains(driver)
    actions.move_to_element(download_button).perform()

    overlay_element = driver.find_element(By.XPATH, "//a[@class='dropdown-toggle']")
    WebDriverWait(driver, 10).until_not(EC.staleness_of(overlay_element))

    driver.execute_script("arguments[0].click();", download_button)

    time.sleep(5)

    ProfileLogOut = driver.find_element(By.XPATH,"//img[@class='user-image']")
    ProfileLogOut.click()

    LogOut = driver.find_element(By.XPATH,"//a[normalize-space()='Sign out']")
    LogOut.click()

    time.sleep(3)

    print(driver.title)

finally:
    driver.quit()

print(f"\nWaiting for 3 minutes before starting the next browser at {datetime.now()}...")
# time.sleep(interval_minutes * 5)

# if __name__ == "__main__":
#     pytest.main(["-v","-n"," 1", "test_4.py"])
