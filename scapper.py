from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrapJobsTitle(driver, titleXpath, nextButtonXpath, totalJobsPerPage):
    jobsTitle = []
    with open('job-title.txt', 'w') as file:  # Open file once outside the loop
        for i in range(4):
            print(f"Scrapping Page {i + 1}")
            
            # Ensure that the page has loaded and elements are present
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, titleXpath))
            )
            
            # Re-fetch products to avoid StaleElementReferenceException
            products = driver.find_elements(By.XPATH, titleXpath)
            for product in products:
                title = product.text
                print(f"Product Title = {title}\n")
                jobsTitle.append(title)
                file.write(f'Job Title = {title}\n')  # Write each title

            # Handle next button
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, nextButtonXpath)))
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(1)  # Brief pause to let the page start loading
            except Exception as e:
                print(f"Failed to click next button on page {i+1}: {str(e)}")
                break  # Exit loop if can't click next

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
    
    titleXpath = '//*[@data-automation-id="jobTitle"]'  # Update this XPath based on actual job title elements
    nextButtonXpath = "//button[@data-uxi-widget-type='stepToNextButton']"  # Update this if needed

    # Scrape job titles
    totalJobsPerPage = 20  # Adjust as needed based on the pagination of the site
    job_titles = scrapJobsTitle(driver, titleXpath, nextButtonXpath, totalJobsPerPage)
    print(job_titles)
finally:
    driver.quit()
