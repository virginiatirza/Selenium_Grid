from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytest

@pytest.mark.parametrize("browser, version, platform", [
    ("chrome", "latest", "WINDOWS"),
    # ("chrome", "latest", "MAC"),  # Try "MicrosoftEdge"
    ("firefox", "latest", "WINDOWS"),
    ("msedge", "latest", "WINDOWS"),  # Add Firefox configuration
])

def test_cross_browser(browser, version, platform):
    interval_minutes = 2
    total_iterations = 1  # Adjust the number of iterations as needed

    for iteration in range(total_iterations):
        print(f"Running iteration {iteration + 1}...")

        url_hub = "http://10.4.75.29:4444"

        # Create WebDriver instance based on browser
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            driver = webdriver.Remote(
                command_executor=url_hub,
                options=options
            )
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.binary_location = "C:/Users/virginia/Downloads/geckodriver-v0.34.0-win32/geckodriver.exe"
            driver = webdriver.Remote(
                command_executor=url_hub,
                options=options
            )
        elif browser == "msedge":
            options = webdriver.EdgeOptions()
            driver = webdriver.Remote(
                command_executor=url_hub,
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        try:
            baseURL = "https://www.google.com/"
            driver.get(baseURL)
            driver.implicitly_wait(5)
            driver.maximize_window()
            wait = WebDriverWait(driver, 10)

            print(f"Title on {browser} {version} - {platform}: {driver.title}")

        finally:
            driver.quit()

        print(f"Waiting for {interval_minutes} minutes before the next iteration...")

        time.sleep(interval_minutes * 10)

if __name__ == "__main__":
    pytest.main(["-v","-n"," 3", "test_3.py"])
