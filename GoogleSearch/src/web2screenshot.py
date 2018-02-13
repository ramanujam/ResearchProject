from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_PATH         = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
CHROMEDRIVER_PATH   = '/usr/local/bin/chromedriver'
WINDOW_SIZE         = "1920,1080"

chrome_options = Options()  
chrome_options.add_argument("--headless")
#chrome_options.add_argument("--screenshot")
# chrome_options.add_argument("--remote-debugging-port=9222")

chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

def make_screenshot(url, output):
    if not url.startswith('http'):
        raise Exception('URLs need to start with "http"')

    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        chrome_options=chrome_options
    )  
    driver.get(url)
    driver.save_screenshot(output)
    driver.close()