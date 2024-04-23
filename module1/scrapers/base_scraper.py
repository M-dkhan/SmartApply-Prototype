from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BaseScraper:
    def __init__(self, baseUrl):
        self.chrome_options, self.driver = self.configure()
        self.baseUrl = baseUrl

    def open_url(self, url=''):
        fullUrl = f"{self.baseUrl}{url}"
        self.driver.get(fullUrl)
        time.sleep(5)

    def close(self):
        self.driver.quit()

    def scrape(self):
        raise NotImplementedError("This method should be overridden by subclasses")


    def configure():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # To run Chrome in headless mode
        driver = webdriver.Chrome(options=chrome_options)

        return [chrome_options, driver]