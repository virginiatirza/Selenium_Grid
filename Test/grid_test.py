from selenium import webdriver

# Connect to Selenium Grid Hub
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities={'browserName': 'chrome'}
)

# Perform Selenium actions
driver.get("https://www.google.com")
print("Title:", driver.title)

# Close the browser
driver.quit()