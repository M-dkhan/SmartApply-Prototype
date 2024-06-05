#!/usr/bin/env python3

import email
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
from module2.mailjet import sendmail
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class AmazonScraper(BaseScraper):
    
    def __init__(self, baseUrl, driver, jobSearchKeyword, timeType, location):
        super().__init__(baseUrl, driver)
        self.open_url()
        self.jobsList = []
        self.searchLocation = location
        self.sleepTime = 1
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

        # TODO: introduce concurrenency here each job will execute on its own at same time
        self.jobsList = [self.process_job(job) for job in job_listings]

        if (len(self.jobsList) == 0):
            print("NO JOBS FOUND!!")


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
            url=self.base_url+title_element['href'],
            role_type=None,
            description=description_element.text,
            location=location_element.text,
            job_id=job_id,
            collectionName='AmazonJobs'
        )
        print(job)
        # self.apply_for_job(job)
        return job

    def apply_for_job(self, job):
        # Construct the full URL for the job application page
        job_url = self.base_url + job.url
        print(job_url)
        self.driver.get(job_url)
        

    # page 1 : click on the apply button 
        apply_button_xpath = "//input[@type='submit' and @name='j_id0:portId:j_id157:j_id160' and @value='Apply']"
        radio_button_xpath = "//input[@id='j_id0:portId:j_id162:j_id205:0']"
        continue_button_xpath = "//input[@id='j_id0:portId:j_id162:continue2']"

        # click on the apply button 
        apply_button = WebDriverWait(self.driver, self.sleepTime).until(EC.element_to_be_clickable((By.XPATH, apply_button_xpath)))
        apply_button.click()

    # page 2: accept the terms and conditions 
        # Select the radio button
        radio_button = WebDriverWait(self.driver, self.sleepTime).until(EC.element_to_be_clickable((By.XPATH, radio_button_xpath)))
        radio_button.click()

        # Wait for the "Continue" button to be enabled and click it
        continue_button = WebDriverWait(self.driver, self.sleepTime).until(lambda d: d.find_element(By.XPATH, continue_button_xpath).is_enabled())
        self.driver.find_element(By.XPATH, continue_button_xpath).click()


        # 

    # part 3 : Enter the phone / email
        self.login()


    # part 4: Two step verification



    # part 5: select shift 



    def login(self):
        email_field_xpath = '//*[@id="login"]'
        pin_xpath = '//*[@id="pin"]'
        next_button_xpath = '//*[@data-test-id="button-next"]'

        try:
            # page 1 Enter phone or email 

            # Wait for the email field to be present in the DOM
            WebDriverWait(self.driver, self.sleepTime).until(
                EC.presence_of_element_located((By.XPATH, email_field_xpath))
            )
            
            # Directly set the value of the email input field using JavaScript
            self.driver.execute_script(
                'document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = arguments[1];',
                email_field_xpath, '4168265259'
            )

            # Print the outer HTML for debugging
            outer_html = self.driver.execute_script(
                'return document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.outerHTML;',
                email_field_xpath
            )

            # Wait for the next button to be present in the DOM
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, next_button_xpath))
            )
            
            # Directly click the next button using JavaScript
            self.driver.execute_script(
                'document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();',
                next_button_xpath
            )

            # page 2 Enter pin 
            # Wait for the email field to be present in the DOM
            WebDriverWait(self.driver, self.sleepTime).until(
                EC.presence_of_element_located((By.XPATH, pin_xpath))
            )
            
            # Directly set the value of the email input field using JavaScript
            self.driver.execute_script(
                'document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = arguments[1];',
                pin_xpath, '628351'
            )

            # Print the outer HTML for debugging
            outer_html = self.driver.execute_script(
                'return document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.outerHTML;',
                pin_xpath
            )
            print(outer_html)

            # Wait for the next button to be present in the DOM
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, next_button_xpath))
            )
            
            # Directly click the next button using JavaScript
            self.driver.execute_script(
                'document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();',
                next_button_xpath
            )

            
        except TimeoutException:
            print("Timeout: Element not found within the given time")