from module1.scrapers.base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from module1.utils.helpers import extract_numbers, calculateTotalPages,extract_attribute
from bs4 import BeautifulSoup

class Workday5Scraper(BaseScraper):
    def __init__(self, baseUrl, jobSearchKeyword, timeType):
        super().__init__(baseUrl)

        # Open the portal
        self.open_url()  # Assuming open_url is correctly implemented in BaseScraper
        
        # create a dictonary for list of all the available jobs 
        self.jobList = {}
        
        # the job search keyword 
        self.jobSearchKeyword = jobSearchKeyword
        
        # time type either full time or part time 
        self.timeType = timeType
        
        #wait for sleepTime for any response from the web page  
        self.sleepTime = 5

        # constant for jobs per page for specific job portal
        self.JOBS_PER_PAGE = 20

        # Search for a specific job if provided
        self.apply_filters(keyword=self.jobSearchKeyword, time_type=self.timeType, location={'country':'Canada','state':'Ontraio'})

        # Fetch total jobs after searching
        self.totalJobs = self.fetchTotalJobsFound()

        # fetch Job List
        self.fetchJobsList()

    def scrape(self):
        # Return the total number of jobs found
        return self.totalJobs
    
            
    def fetchTotalJobsFound(self):
        try:
            totalJobsFound_xpath = '//*[@data-automation-id="jobFoundText"]'
            totalJobsFoundElement = WebDriverWait(self.driver, self.sleepTime).until(
                EC.visibility_of_element_located((By.XPATH, totalJobsFound_xpath))
            )
            totalJobsFoundText = totalJobsFoundElement.text
            totalJobsFound = extract_numbers(totalJobsFoundText)
            return totalJobsFound
        except Exception as e:
            print(f"An error occurred while fetching the total number of jobs: {str(e)}")
            return 0

    def fetchJobsList(self):
        totalPages = calculateTotalPages(self.fetchTotalJobsFound(), 20)
        nextPaginationButtonXpath = "//button[@data-uxi-widget-type='stepToNextButton']"
        titleXpath = '//*[@data-automation-id="jobTitle"]'
        print(totalPages)
        
        for i in range(totalPages):
            # print(f"Scraping Page {i + 1} of {totalPages}")
            jobTitles = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, titleXpath))
            )

            for index, job in enumerate(jobTitles):
                jobTitle = job.text
                jobLink = job.get_attribute("href")
                # print(f"Job Title: {jobTitle}_{index}")
                self.jobList[f"{jobTitle}_{index}"] = jobLink

            if i < totalPages - 1:
                try:
                    nextPaginationButton = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, nextPaginationButtonXpath))
                    )
                    nextPaginationButton.click()
                    time.sleep(3)  # Wait for page to stabilize before the next cycle
                except Exception as e:
                    print(f"Failed to navigate to next page on attempt {i + 1}: {str(e)}")
                    break
            print()
    
    # TODO: Currently its on by location but later on it should be either by location or by distance .
    # TODO: implement the logic for by distance
    def filter_by_location(self, location):
        
        # TODO: Make this dynamic 
        # the option for by locatin or by distance
        # by default is set to location 
        filter_criterion = 'location'
        filter_location_country = 'Canada'
        filter_location_state = 'Ontario'
        
        # Click on the employment type filter button
        location_filter_xpath = '//button[@data-automation-id="distanceLocation"]'
        location_filter_button = WebDriverWait(self.driver, self.sleepTime).until(
            EC.element_to_be_clickable((By.XPATH, location_filter_xpath))
        )
        # Now, you can print the HTML of just the filter button
        location_filter_button.click()

        location_filterMenu_xpath = '//fieldset[@data-automation-id="filterMenu"]'

        try:
            # Find the filter menu
            location_filterMenu = WebDriverWait(self.driver, self.sleepTime).until(
                EC.presence_of_element_located((By.XPATH, location_filterMenu_xpath))
            )

            # Extract the inner HTML of the filter menu
            location_radio_filterMenu_HTML = location_filterMenu.get_attribute('innerHTML')

            # Extract the checkbox ID based on the timeType
            location_radio_Checkbox_id = extract_attribute(location_radio_filterMenu_HTML, 'label', filter_criterion, 'for')
                        
            # Wait for and find the checkbox by ID
            location_radio_input_element = WebDriverWait(self.driver, self.sleepTime).until(
                        EC.presence_of_element_located((By.ID, str(location_radio_Checkbox_id)))
                    )
            if not location_radio_input_element.is_selected():
                location_radio_input_element.click()
                
            time.sleep(self.sleepTime)
            
            '''
            code to select the country 
            '''
            
            # Extract the inner HTML of the filter menu
            country_filter_menu_HTML = location_filterMenu.get_attribute('innerHTML')
            country_Checkbox_id = extract_attribute(country_filter_menu_HTML, 'label', filter_location_country, 'for')
            country_input_element = WebDriverWait(self.driver, self.sleepTime).until(
                        EC.presence_of_element_located((By.ID, str(country_Checkbox_id)))
                    )
            print(country_Checkbox_id)
            if not country_input_element.is_selected():
                country_input_element.click()
            time.sleep(self.sleepTime)
            
            
            # Click on the "View Jobs" button
            view_jobs_button_xpath = '//button[@data-automation-id="viewAllJobsButton"]'
            view_jobs_button = WebDriverWait(location_filterMenu, self.sleepTime).until(
                EC.element_to_be_clickable((By.XPATH, view_jobs_button_xpath))
            )
            view_jobs_button.click()
            # Wait for job listings to load after applying the filter
            time.sleep(self.sleepTime)    
            
            
        except Exception as e:
            # Handle exceptions and print traceback for debugging
            print("An error occurred:")
        
        
        return super().filter_by_location(location)
        
    def filter_by_time_type(self, time_type):
        # Click on the employment type filter button
        timeType_filter_xpath = '//button[@data-automation-id="employmentType"]'
        timeType_filter_button = WebDriverWait(self.driver, self.sleepTime).until(
            EC.element_to_be_clickable((By.XPATH, timeType_filter_xpath))
        )
        # Now, you can print the HTML of just the filter button
        timeType_filter_button.click()

        timeType_filterMenu_xpath = '//fieldset[@data-automation-id="employmentTypeCheckboxGroup"]'

        try:
            # Find the filter menu
            timeType_filterMenu = WebDriverWait(self.driver, self.sleepTime).until(
                EC.presence_of_element_located((By.XPATH, timeType_filterMenu_xpath))
            )

            # Extract the inner HTML of the filter menu
            timeType_filterMenu_HTML = timeType_filterMenu.get_attribute('innerHTML')

            # Extract the checkbox ID based on the timeType
            timeType_Checkbox_id = extract_attribute(timeType_filterMenu_HTML, 'label', time_type, 'for')
            
            # Wait for and find the checkbox by ID
            timeType_input_element = WebDriverWait(self.driver, self.sleepTime).until(
                        EC.presence_of_element_located((By.ID, str(timeType_Checkbox_id)))
                    )
            if not timeType_input_element.is_selected():
                timeType_input_element.click()
            
        except Exception as e:
            # Handle exceptions and print traceback for debugging
            print("An error occurred:")
        
        # Click on the "View Jobs" button
        view_jobs_button_xpath = '//button[@data-automation-id="viewAllJobsButton"]'
        view_jobs_button = WebDriverWait(timeType_filterMenu, self.sleepTime).until(
            EC.element_to_be_clickable((By.XPATH, view_jobs_button_xpath))
        )
        view_jobs_button.click()
        # Wait for job listings to load after applying the filter
        time.sleep(self.sleepTime)  # Adjust this wait time as needed
        
        return super().filter_by_time_type(time_type)
    
    
    def filter_by_keyword(self, keyword):
        # Locate the search field using XPath
        search_field_xpath = '//*[@data-automation-id="keywordSearchInput"]'
        search_field = WebDriverWait(self.driver, self.sleepTime).until(
            EC.visibility_of_element_located((By.XPATH, search_field_xpath))
        )
        search_field.clear()  # Clear any existing text
        search_field.send_keys(keyword)

        # Locate the search button using XPath and click it
        search_button_xpath = '//*[@data-automation-id="keywordSearchButton"]'
        search_button = WebDriverWait(self.driver, self.sleepTime).until(
            EC.element_to_be_clickable((By.XPATH, search_button_xpath))
        )
        
        search_button.click()

        # Wait for the page to load after search
        time.sleep(self.sleepTime)
        return super().filter_by_keyword(keyword)

jobScraper = Workday5Scraper(baseUrl="https://walmart.wd5.myworkdayjobs.com/WalmartExternal", jobSearchKeyword="", timeType="part time")

print(jobScraper.totalJobs, '= Total Jobs')
print(jobScraper.jobList)
print(len(jobScraper.jobList))