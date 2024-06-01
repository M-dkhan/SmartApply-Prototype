from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import ABC, abstractmethod
from typing import Optional
from module2.firebase_setup import FirestoreManager
import time

start_time = time.time()

class BaseScraper(ABC):
    def __init__(self, base_url: str):
        self.driver = self._configure_driver()
        self.base_url = base_url
        self.db = FirestoreManager.db

    def open_url(self, url: str = ''):
        full_url = f"{self.base_url}{url}"
        self.driver.get(full_url)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )  # Wait until the page loads

    def close(self):
        self.driver.quit()

    @abstractmethod
    def scrape(self):
        """
        Abstract method to scrape data from the website.
        Derived classes must implement this method with their own logic.
        """
        pass

    def _configure_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # To run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--start-maximized")  # Start browser maximized to avoid dynamic content loading issues
        return webdriver.Chrome(options=chrome_options)

    
    def filter_by_keyword(self, keyword: str):
        """
        Abstract method to filter jobs by keyword.
        Derived classes must implement this method with their own logic.
        """
        pass

    
    def filter_by_location(self, location: str):
        """
        Abstract method to filter jobs by location.
        Derived classes must implement this method with their own logic.
        """
        pass

    
    def filter_by_date_posted(self, date_range: str):
        """
        Abstract method to filter jobs by date posted.
        Derived classes must implement this method with their own logic.
        """
        pass

    
    def filter_by_time_type(self, time_type: str):
        """
        Abstract method to filter jobs by employment type.
        Derived classes must implement this method with their own logic.
        """
        pass

    def apply_filters(self, keyword: Optional[str] = None, location: Optional[str] = None, date_range: Optional[str] = None, time_type: Optional[str] = None):
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

        # Wait for any changes to take effect, if necessary
        WebDriverWait(self.driver, 1).until_not(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'loading-indicator')]"))
        )

end_time = time.time()
execution_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
print(f"Execution time: {execution_time_ms} milliseconds")