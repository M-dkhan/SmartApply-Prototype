from .base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from module1.utils.helpers import extract_numbers, calculateTotalPages, extract_attribute
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed

class Workday5Scraper(BaseScraper):
    def __init__(self, baseUrl, jobSearchKeyword, timeType):
        super().__init__(baseUrl)

        # Open the portal
        self.open_url()  # Assuming open_url is correctly implemented in BaseScraper

        # create a dictionary for list of all the available jobs
        self.jobList = {}

        # the job search keyword
        self.jobSearchKeyword = jobSearchKeyword

        # time type either full time or part time
        self.timeType = timeType

        # wait for sleepTime for any response from the web page
        self.sleepTime = 20

        # constant for jobs per page for specific job portal
        self.JOBS_PER_PAGE = 20

        # Search for a specific job if provided
        self.apply_filters(keyword=self.jobSearchKeyword, time_type=self.timeType, location={'country': 'Canada', 'state': 'Ontario', 'keyword': 'Ontario'})

        # Fetch total jobs after searching
        self.totalJobs = self.fetchTotalJobsFound()

        # fetch Job List
        self.fetchJobsList()

    def scrape(self):
        # Return the total number of jobs found
        return self.totalJobs

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
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
            raise  # Re-raise the exception to trigger retry

    def fetchJobsList(self):
        try:
            # Get the total number of pages based on the total jobs
            totalJobs = self.fetchTotalJobsFound()  # Re-check if total jobs count is accurate
            totalPages = calculateTotalPages(totalJobs, self.JOBS_PER_PAGE)

            nextPaginationButtonXpath = "//button[@data-uxi-widget-type='stepToNextButton']"
            titleXpath = '//*[@data-automation-id="jobTitle"]'

            print("Total Pages: ", totalPages)

            for i in range(totalPages):
                # Try to scrape the current page's jobs
                jobTitles = WebDriverWait(self.driver, self.sleepTime).until(
                    EC.presence_of_all_elements_located((By.XPATH, titleXpath))
                )

                # Add unique keys to avoid overwriting in the dictionary
                for index, job in enumerate(jobTitles):
                    jobTitle = job.text
                    jobLink = job.get_attribute("href")
                    jobKey = f"{jobTitle}_{i}_{index}"
                    self.jobList[jobKey] = jobLink
                    print(jobTitle, jobLink)

                if i < totalPages - 1:
                    try:
                        # Try to navigate to the next page
                        nextPaginationButton = WebDriverWait(self.driver, self.sleepTime).until(
                            EC.element_to_be_clickable((By.XPATH, nextPaginationButtonXpath))
                        )
                        nextPaginationButton.click()
                        time.sleep(3)  # Allow the page to load
                    except Exception as e:
                        print(f"Failed to navigate to the next page on page {i + 1}: {str(e)}")
                        break
                print(f"Page {i + 1} completed. Total jobs in dictionary: {len(self.jobList)}")

        except Exception as e:
            print("An error occurred while fetching the jobs list:", str(e))

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def filter_by_location(self, location):
        # Click on the employment type filter button
        location_filter_xpath = '//button[@data-automation-id="distanceLocation"]'
        location_filter_button = WebDriverWait(self.driver, self.sleepTime).until(
            EC.element_to_be_clickable((By.XPATH, location_filter_xpath))
        )
        print(location_filter_button.get_attribute("innerHTML"))
        location_filter_button.click()

        location_filterMenu_xpath = "//div[@data-automation-id='filterMenu']"
        location_filterMenu = WebDriverWait(self.driver, self.sleepTime).until(
            EC.presence_of_element_located((By.XPATH, location_filterMenu_xpath))
        )
        print(location_filterMenu.get_attribute("innerHTML"))

        # Get the location filter checkbox ID
        location_radio_filterMenu_HTML = location_filterMenu.get_attribute('innerHTML')
        location_radio_Checkbox_id = extract_attribute(
            location_radio_filterMenu_HTML, 'label', 'location', 'for'
        )
        print(location_radio_Checkbox_id)

        # Wait for and find the checkbox by ID
        for _ in range(3):  # Retry clicking the checkbox up to 3 times
            try:
                location_radio_input_element = WebDriverWait(self.driver, self.sleepTime).until(
                    EC.presence_of_element_located((By.ID, str(location_radio_Checkbox_id)))
                )
                if not location_radio_input_element.is_selected():
                    location_radio_input_element.click()
                break  # Exit the loop if click is successful
                print("PASSED")
            except Exception as e:
                # Scroll the element into view and try again
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", location_radio_input_element
                )
                print('FAILED!!')
                time.sleep(1)  # Short delay before retrying

        # Delay to ensure the action is completed (optional)
        # time.sleep(self.sleepTime)

        # Search location with keyword if given
        search_field_xpath = '//*[@data-automation-id="searchInput"]'
        search_field = WebDriverWait(self.driver, self.sleepTime).until(
            EC.visibility_of_element_located((By.XPATH, search_field_xpath))
        )
        print("Search Button : -", search_field.get_attribute('innerHTML'), "its Empty. ")
        search_field.clear()
        search_field.send_keys(location['keyword'])

        # ... rest of your code to filter by country (similar logic with retries)

        # Click on the "View Jobs" button
        view_jobs_button_xpath = '//button[@data-automation-id="viewAllJobsButton"]'
        view_jobs_button = WebDriverWait(location_filterMenu, self.sleepTime).until(
            EC.element_to_be_clickable((By.XPATH, view_jobs_button_xpath))
        )
        time.sleep(self.sleepTime)
        view_jobs_button.click()

        # Wait for job listings to load after applying the filter
        time.sleep(self.sleepTime)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
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
            print("An error occurred while filtering by time type:", str(e))
            raise  # Re-raise the exception to trigger retry

        # Click on the "View Jobs" button
        view_jobs_button_xpath = '//button[@data-automation-id="viewAllJobsButton"]'
        view_jobs_button = WebDriverWait(timeType_filterMenu, self.sleepTime).until(
            EC.element_to_be_clickable((By.XPATH, view_jobs_button_xpath))
        )
        view_jobs_button.click()
        # Wait for job listings to load after applying the filter
        time.sleep(self.sleepTime)  # Adjust this wait time as needed

        return super().filter_by_time_type(time_type)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
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


jobScraper = Workday5Scraper(baseUrl="", jobSearchKeyword="", timeType="part time")

print(jobScraper.totalJobs, '= Total Jobs')
print(jobScraper.jobList)
print(len(jobScraper.jobList))
