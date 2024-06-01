#!/usr/bin/env python3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from module1.jobs.specialized_jobs.amazon_job import AmazonJob
from module1.scrapers.base_scraper import BaseScraper
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import re


class AmazonScraper(BaseScraper):
    
    def __init__(self, baseUrl, jobSearchKeyword, timeType, location):
        super().__init__(baseUrl)
        self.open_url()
        self.jobsList = []
        self.searchLocation = location
        self.sleepTime = 10
        self.filter_by_location()

    def scrape(self):
        pass
    
    def fetchJobsList(self):
        pass

    def filter_by_location(self):
        country = self.searchLocation.get('country')
        state = self.searchLocation.get('state')
        
        # Click on the search button to collapse the window 
        self.click_element(By.CLASS_NAME, "accordion-toggle")
        
        # Select country and state
        self.select_dropdown_option('select[id="j_id0:portId:j_id67:Country"]', country)
        self.select_dropdown_option('select[id="j_id0:portId:j_id67:State"]', state)
        
        # Click the filter jobs button
        self.click_element(By.XPATH, '//*[@id="search-container"]/div/div[2]/div/input')
        self.fetch_job_listings()

    def click_element(self, by, value):
        element = WebDriverWait(self.driver, self.sleepTime).until(
            EC.presence_of_element_located((by, value))
        )
        element.click()

    def select_dropdown_option(self, selector, value):
        select_element = WebDriverWait(self.driver, self.sleepTime).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        Select(select_element).select_by_value(value)

        # Verify if the option is selected
        if Select(select_element).first_selected_option.is_selected():
            print(f"{value} option is selected.")
        else:
            print(f"{value} option is not selected.")

    def fetch_job_listings(self):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        job_listings = soup.select('#recent-jobs2 .listing.row')

        self.jobsList = [self.process_job(job) for job in job_listings]


    def process_job(self, job):
        title_element = job.find('h6').find('a')
        description_element = job.find('p')
        location_element = job.find('h6').find('span')

        # Search for the <strong> tag containing the job ID directly
        job_id_element = job.find('strong')

        # Extract the text from the job ID element if found
        job_id = job_id_element.text.strip() if job_id_element else None

        job =  AmazonJob(
            title=title_element.text,
            url=title_element['href'],
            role_type=None,
            description=description_element.text,
            location=location_element.text,
            job_id=job_id,
            collectionName='AmazonJobs'
        )
        return job
