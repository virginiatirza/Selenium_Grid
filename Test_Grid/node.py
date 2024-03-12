from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up ChromeDriver
chrome_service = ChromeService(executable_path='path/to/chromedriver')
chrome_service.start()

# Set up Selenium Grid Node
node_capabilities = {
    'browserName': 'chrome',
}

node = WebDriver(
    command_executor='http://172.20.10.2:4444/',
    desired_capabilities=node_capabilities,
)

node.get('https://www.google.com')
print(node.title)

node.quit()
chrome_service.stop()
