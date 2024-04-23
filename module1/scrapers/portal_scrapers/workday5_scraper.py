from module1.scrapers.base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from module1.utils.helpers import extract_numbers

class Workday5_scraper(BaseScraper):

    def __init__(self, baseUrl, jobSearchKeyword):
        super().__init__(baseUrl)

        # open the portal
        self.open_url()

        # serach for specific if provided
        self.searchJobs(jobSearchKeyword, 5)

        # fetch total jobs after seraching
        self.totalJobs = self.fetchTotalJobsFound()

    def scrape(self):
        return super().scrape()

    def searchJobs(self, jobSearchKeyword, sleepTimeInSeconds):
        # Locate the search field using XPath
        search_field_xpath = '//*[@data-automation-id="keywordSearchInput"]'
        search_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, search_field_xpath)))
        search_field.send_keys(jobSearchKeyword)

        # Locate the search button using XPath
        search_button_xpath = '//*[@data-automation-id="keywordSearchButton"]'
        search_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
        search_button.click()
        time.sleep(sleepTimeInSeconds)

    def fetchTotalJobsFound(self):
        totalJobsFound_xpath = '//*[@data-automation-id="jobFoundText"]'
        totalJobsFoundElement = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, totalJobsFound_xpath)))
        totalJobsFoundText = totalJobsFoundElement.text
        totalJobsFound = extract_numbers(totalJobsFoundText)
        return totalJobsFound
