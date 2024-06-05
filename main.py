import time

from module1.jobs.specialized_jobs.amazon_job import AmazonJob
from module1.scrapers.portal_scrapers.amazon import AmazonScraper 
from selenium import webdriver
from dotenv import load_dotenv
import os
from module2.mailjet import sendmail

# Load environment variables from .env file
load_dotenv()

def _configure_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-popup-blocking")
    return webdriver.Chrome(options=chrome_options)


if __name__ == "__main__":

    start_time = time.time()

    driver = _configure_driver()

    # Example usage
    amazon = AmazonScraper(
        baseUrl="https://hvr-amazon.my.site.com",
        driver=driver,
        jobSearchKeyword='',
        location={'country': 'IN', 'state': ''},
        timeType='Part Time'
    )
    # sendmail(mailjet_apikey, mailjet_secretkey,"hello this is a testing email and this working")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Script executed in {elapsed_time:.2f} seconds.")

   