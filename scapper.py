from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrapJobsTitle(driver, titleXpath, nextButtonXpath, totalJobsPerPage):
    jobsTitle = []

    # Correct the XPath format and usage
    for i in range(totalJobsPerPage):
        print(f"Scrapping Page {i + 1}")
        # Use the correct method to find elements by XPath
        products = driver.find_elements(By.XPATH, titleXpath)
        # print(products)
        for product in products:
            print(f"Product Title = {product.text}\n")
            jobsTitle.append(product.text)  # Store job title text
        
        # Find the next button and click it
        # next_button = driver.find_element(By.XPATH, nextButtonXpath)
        # next_button.click()
        time.sleep(3)  # Wait for the next page to load

    return jobsTitle

# Example usage
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # To run Chrome in headless mode
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://walmart.wd5.myworkdayjobs.com/WalmartExternal")
    # Assume corrected XPaths are provided here
    time.sleep(5)
    
    # Locate the search field using XPath
    search_field_xpath = '//*[@data-automation-id="keywordSearchInput"]'
    search_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, search_field_xpath)))
    search_field.send_keys('Ontario')

    # Locate the search button using XPath
    search_button_xpath = '//*[@data-automation-id="keywordSearchButton"]'
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
    search_button.click()
    time.sleep(5)
    
    
    job_titles = scrapJobsTitle(driver, '//*[@data-automation-id="jobTitle"]', '//*[@data-uxi-widget-type="stepToNextButton"]', 20)
    print(job_titles)
finally:
    driver.quit()
