from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from abc import ABC, abstractmethod 
from module2.firebase_setup import FirestoreManager
class BaseScraper:

    def __init__(self, baseUrl):
        self.chrome_options, self.driver = self._configure()
        self.baseUrl = baseUrl
        self.db = FirestoreManager.db

    def open_url(self, url=''):
        fullUrl = f"{self.baseUrl}{url}"
        self.driver.get(fullUrl)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))  # Wait until the page loads

    def close(self):
        self.driver.quit()

    def scrape(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def _configure(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # To run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        driver = webdriver.Chrome(options=chrome_options)
        return chrome_options, driver

    def fetchJobsList():
        raise NotImplementedError("This method should be overridden by subclasses")

    # def fetchTitle():
    #     raise NotImplementedError("This method should be overridden by subclasses")
    
    # def fetchApplyUrl():
    #     raise NotImplementedError("This method should be overridden by subclasses")

    # def fetchLocation():
    #     raise NotImplementedError("This method should be overridden by subclasses")

    # def fetchRoleType():
    #     raise NotImplementedError("This method should be overridden by subclasses")

    # def fetchPosition():
    #     raise NotImplementedError("This method should be overridden by subclasses")
    
    # def fetchRequisitionId():
    #     raise NotImplementedError("This method should be overridden by subclasses")
    
    # def fetchDescription():
    #     raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def filter_by_keyword(self, keyword):
        """
        Abstract method to filter jobs by keyword.
        Derived classes must implement this method with their own logic.
        """
        pass
    
    @abstractmethod
    def filter_by_location(self, location):
        """
        Abstract method to filter jobs by location.
        Derived classes must implement this method with their own logic.
        """
        pass
    
    @abstractmethod
    def filter_by_date_posted(self, date_range):
        """
        Abstract method to filter jobs by date posted.
        Derived classes must implement this method with their own logic.
        """
        pass
    
    @abstractmethod
    def filter_by_time_type(self, time_type):
        """
        Abstract method to filter jobs by employment type.
        Derived classes must implement this method with their own logic.
        """
        pass
    
    
    # Main filter function to call specific filter methods based on given parameters
    def apply_filters(self, keyword=None, location=None, date_range=None, time_type=None, sleep_time=20):
        """
        Apply multiple filters based on the given parameters.
        """
        if keyword:
            self.filter_by_keyword(keyword)
        
        if location:
            self.filter_by_location(location)
        
        if date_range:
            self.filter_by_date_posted(date_range)
        
        if time_type:
            self.filter_by_time_type(time_type)
        
        # Wait for any changes to take effect
        time.sleep(sleep_time)