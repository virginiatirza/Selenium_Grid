from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import time
import os


def run_test(browser):
    options = Options()
    grid_url = os.environ.get("SELENIUM_HUB_URL", "http://localhost:4444/wd/hub")
    
    # grid_url = "http://192.168.56.1:4444/wd/hub"
    
    if browser.lower() == 'chrome':
        driver = webdriver.Remote(command_executor=grid_url, options=options)
    elif browser.lower() == 'firefox':
        driver = webdriver.Remote(command_executor=grid_url, options=options)
    # Add more browser options as needed

    try:
        baseURL = "https://data.idx.co.id"
        driver.get(baseURL)
        driver.implicitly_wait(5)
        driver.maximize_window()

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

        pagination = driver.find_element(By.ID, "tblReport_paginate")

        next_button = pagination.find_element(By.CLASS_NAME, "next")

        while True:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                driver.execute_script("arguments[0].click();", next_button)
            except Exception:
                break

        rows = driver.find_elements(By.XPATH, "//tbody/tr")

        last_row = rows[-1]

        download_button = last_row.find_element(By.XPATH, ".//button[contains(@onclick, 'DownloadData')]")

        actions = ActionChains(driver)
        actions.move_to_element(download_button).perform()

        overlay_element = driver.find_element(By.XPATH, "//a[@class='dropdown-toggle']")
        WebDriverWait(driver, 10).until_not(EC.staleness_of(overlay_element))

        driver.execute_script("arguments[0].click();", download_button)

        time.sleep(3)
        ProfileLogOut = driver.find_element(By.XPATH,"//img[@class='user-image']")
        ProfileLogOut.click()

        LogOut = driver.find_element(By.XPATH,"//a[normalize-space()='Sign out']")
        LogOut.click()

        time.sleep(3)

        print(driver.title)

    finally:
        driver.quit()

if __name__ == "__main__":
    browsers = ["chrome", "firefox", "safari"]  # Add more browsers if needed

    # Set up a thread pool for parallel execution
    with ThreadPoolExecutor(max_workers=len(browsers)) as executor:
        # Schedule the tests with different browsers
        for browser in browsers:
            executor.submit(run_test, browser)
