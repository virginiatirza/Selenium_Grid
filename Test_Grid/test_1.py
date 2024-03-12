import pytest
from selenium import webdriver

@pytest.mark.parametrize("browser, version, platform", [
    ("chrome", "latest", "WINDOWS"),
    ("chrome", "latest", "MAC"), # Try "MicrosoftEdge"
])

def test_cross_browser(browser, version, platform):
    # Create WebDriver instance based on browser
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(
            command_executor="http://192.168.56.1:4444",
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Your test script goes here
    driver.get("https://www.google.com")
    print(f"Title on {browser} {version} - {platform}: {driver.title}")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    pytest.main(["-v","-n", " 3", "test_1.py"])
