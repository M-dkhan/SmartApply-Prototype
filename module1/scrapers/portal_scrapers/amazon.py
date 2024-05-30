#!/usr/bin/env python3

from curses import panel
from itertools import count
from module1.scrapers.base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from module1.utils.helpers import extract_numbers, calculateTotalPages, extract_attribute
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
from module1.jobs.specialized_jobs.amazon_job import AmazonJob

class AmazonScrapper(BaseScraper):
    
    def __init__(self, baseUrl, jobSearchKeyword, timeType, location):
        super().__init__(baseUrl)
        self.open_url()
        self.jobsList = {}
        self.searchLocation = location
        self.sleepTime = 2  # Set sleepTime before calling filter_by_location
        self.filter_by_location(self.searchLocation)


    def scrape(self):
        pass
    
    def fetchJobsList(self):
        pass

    def filter_by_location(self, location):
        country = location.get('country')
        state = location.get('state')
        
        # click on the search button to collapse the window 
        search_btn = WebDriverWait(self.driver, self.sleepTime).until(
            EC.presence_of_element_located((By.CLASS_NAME, "accordion-toggle"))
        )
        search_btn.click()
        
        # =====================================================
        
        # get the location input select field
        
        select_element = WebDriverWait(self.driver, self.sleepTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select[id="j_id0:portId:j_id67:Country"]')))

        selected_option = Select(select_element)

        # TODO: Make this dynamic
        selected_option.select_by_value(country)

        # Verify if the option is selected
        option = selected_option.first_selected_option
        if option.is_selected():
            print(f"The option is selected.")
        else:
            print(f"The option is not selected.")

        # get the state input select field 
        state_select_element = WebDriverWait(self.driver, self.sleepTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select[id="j_id0:portId:j_id67:State"]')))

        selected_option = Select(state_select_element)

        # TODO: Make this dynamic
        selected_option.select_by_value(state)

        # Verify if the option is selected
        option = selected_option.first_selected_option
        if option.is_selected():
            print(option.text)
            print(f"The option is selected.")
        else:
            print(f"The option is not selected.")
            
            
        # scrap the filter jobs button
        filterJobsBtn = WebDriverWait(self.driver, self.sleepTime).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="search-container"]/div/div[2]/div/input'))
        )
        
        filterJobsBtn.click()
        
        # =========================================================
        
        try:
            # Wait for the job listings to appear
            # Print the job listings
            job_listings = self.driver.find_elements(By.XPATH, '//div[@id="recent-jobs2"]/div[@class="listing row"]')
            print(job_listings)
            for jobDetail in job_listings:
                title_element = jobDetail.find_element(By.XPATH, './/h6/a')
                title = title_element.text

                # Within the context of the current job listing, locate the job ID element
                job_id_element = jobDetail.find_element(By.XPATH, './/p[contains(text(), "Job ID")]/strong')

                # Extract the Job ID
                job_id = job_id_element.text

                # Extracting job description
                description_element = jobDetail.find_element(By.XPATH, './/p')
                description = description_element.text

                # Extracting job location
                location_element = jobDetail.find_element(By.XPATH, './/h6/span')
                location = location_element.text

                # Extracting details page link
                details_page_link = title_element.get_attribute('href')
                
                job = AmazonJob(title, details_page_link, None, description, location, job_id, collectionName='AmazonJobs')

        except TimeoutException:
            print("No Jobs Found.!!!")


    def apply_filters(self, keyword=None, location='Canada', date_range=None, time_type=None, sleep_time=20):
        return super().apply_filters(keyword, location, date_range, time_type, sleep_time)

amazon = AmazonScrapper(baseUrl="https://hvr-amazon.my.site.com", jobSearchKeyword='', location={'country': 'IN', 'state': 'PB'}, timeType='Part Time')
