import unittest
from unittest.mock import patch, MagicMock
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from module1.scrapers.portal_scrapers.workday5_scraper import Workday5Scraper
from module1.scrapers.base_scraper import BaseScraper

class TestBaseScraper(unittest.TestCase):
    @patch('module1.scrapers.base_scraper.webdriver.Chrome')
    def setUp(self, mock_chrome):
        # Mocking the Chrome WebDriver
        self.mock_chrome = MagicMock()
        mock_chrome.return_value = self.mock_chrome
        self.scraper = BaseScraper('https://walmart.wd5.myworkdayjobs.com/WalmartExternal')

    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_open_url(self, mock_wait):
        # Mocking the WebDriverWait to immediately return True
        mock_wait.return_value = True

        # Testing open_url method
        self.scraper.open_url("")
        self.mock_chrome.get.assert_called_with('https://walmart.wd5.myworkdayjobs.com/WalmartExternal')

    def tearDown(self):
        # Ensure the browser is closed after tests
        self.scraper.close()

class TestWorkday5Scraper(TestBaseScraper):
    def setUp(self):
        super().setUp()
        self.scraper = Workday5Scraper('https://walmart.wd5.myworkdayjobs.com/WalmartExternal', "Ontario")

    @patch('module1.utils.helpers.extract_numbers', return_value=100)
    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_fetch_total_jobs_found(self, mock_wait, mock_extract_numbers):
        # Mocking WebDriverWait to immediately return a mock element with text
        mock_element = MagicMock()
        mock_element.text = "Found 100 jobs"
        mock_wait.return_value = mock_element

        # Testing fetchTotalJobsFound
        total_jobs = self.scraper.fetchTotalJobsFound()
        self.assertEqual(total_jobs, 100)

    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_search_jobs(self, mock_wait):
        # Mocking WebDriverWait to simulate clickable and visible elements
        mock_search_field = MagicMock()
        mock_search_button = MagicMock()
        mock_wait.side_effect = [mock_search_field, mock_search_button]

        # Performing the search
        self.scraper.searchJobs("associate", 1)
        mock_search_field.send_keys.assert_called_with("associate")
        mock_search_button.click.assert_called()

if __name__ == '__main__':
    unittest.main()
