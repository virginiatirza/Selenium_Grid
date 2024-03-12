from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytest
from datetime import datetime
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException

def handle_verification_checkbox(driver): 
    try:
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='ctp-checkbox-container']//input[@type='checkbox']"))
        )
        checkbox.click()

        verifying_msg = WebDriverWait(driver, 60).until(
            EC.invisibility_of_element_located((By.ID, "verifying-msg"))
        )

        success_element = driver.find_element(By.ID, "success")
        failure_element = driver.find_element(By.ID, "fail")

        if success_element.is_displayed():
            print("Verification successful!")
        elif failure_element.is_displayed():
            print("Verification failed!")

    except TimeoutException:
        print("Timeout waiting for verification checkbox or result elements.")

    except Exception as e:
        print(f"Error handling verification checkbox: {e}")

def handle_alert(driver):
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alert text: {alert_text}")

        if "Firefox must send information" in alert_text:
            print("Handling Firefox resend alert...")
            alert.accept()
        else:
            alert.accept()

        print("Alert handled successfully.")

    except NoAlertPresentException:
        print("No alert present.")

    except Exception as e:
        print(f"Error handling alert: {e}")

@pytest.mark.parametrize("browser, version, platform", [
    ("chrome", "latest", "WINDOWS"),
    # ("chrome", "latest", "MAC"),
    ("firefox", "latest", "WINDOWS"),
    ("msedge", "latest", "WINDOWS"), 
])

def test_cross_browser(browser, version, platform):
    interval_minutes = 3
    total_iterations = 1 

    for iteration in range(total_iterations):
        print(f"\nRunning iteration {iteration + 1} at {datetime.now()}...")
        
        hub_url = "http://10.4.75.110:4444"
        
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            driver = webdriver.Remote(
                command_executor=hub_url,
                options=options
            )
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"            
            driver = webdriver.Remote(
            command_executor=hub_url,
            options=options
            ) 
        elif browser == "msedge":
            options = webdriver.EdgeOptions()
            driver = webdriver.Remote(
                command_executor=hub_url,
                options=options
            )   
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        baseURL = "https://data.idx.co.id"
        driver.get(baseURL)
        driver.implicitly_wait(5)
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

        handle_verification_checkbox(driver)

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

        print(f"Title on {browser} {version} - {platform}: {driver.title}")

        MenuIDXData = driver.find_element(By.XPATH,"//span[normalize-space()='IDX Data']")
        MenuIDXData.click()

        # PilihFolder = driver.find_element(By.XPATH, '//a[@href="javascript:GetFileList(\'idx-equity-eod-basic\');"]')
        # PilihFolder.click()s

        time.sleep(3)

        PilihFolder = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="javascript:GetFileList(\'idx-equity-eod-basic\');"]')))
        PilihFolder.click()

        # PilihDataDaily = driver.find_element(By.XPATH,'//a[@href="javascript:GetFileList(\'data-daily\');"]')
        # PilihDataDaily.click()

        PilihDataDaily = wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@href="javascript:GetFileList(\'data-daily\');"]')))
        PilihDataDaily.click()

        time.sleep(3)

        pagination = driver.find_element(By.ID, "tblReport_paginate")

        while True:
            next_button = pagination.find_element(By.CLASS_NAME, "next")

            if "disabled" in next_button.get_attribute("class"):
                print("Next button is disabled. Exiting loop.")
                break

            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            next_button.click()

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

        handle_verification_checkbox(driver)

        ProfileLogOut = driver.find_element(By.XPATH,"//img[@class='user-image']")
        ProfileLogOut.click()

        LogOut = driver.find_element(By.XPATH,"//a[normalize-space()='Sign out']")
        LogOut.click()

        time.sleep(3)

        print(driver.title)

        print("LOG OUT")

        driver.quit()

        print("Success!")

        print(f"\nWaiting for 3 minutes before starting the next browser at {datetime.now()}...")
        time.sleep(interval_minutes * 70)

if __name__ == "__main__":
    pytest.main(["-v","test_2fix.py"])