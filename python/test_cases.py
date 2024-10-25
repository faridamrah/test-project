import os
import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

chrome_node_service = os.getenv('CHROME_NODE_SERVICE', 'selenium-hub')
selenium_hub_url = f'http://{chrome_node_service}:4444/wd/hub/status'


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

remote_url = f'http://{chrome_node_service}:4444/wd/hub'

# Initialize WebDriver with the options
driver = webdriver.Remote(command_executor=remote_url, options=options)

# Function to get the current time in CET
def get_cet_time():
    cet = pytz.timezone('CET')
    return datetime.now(cet).strftime('%Y-%m-%d %H:%M:%S')

def check_selenium_hub_status():
    try:
        response = requests.get(selenium_hub_url)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        status = response.json()

        # Log the entire response for debugging if the structure is unexpected
        logger.info(f"Selenium Hub response: {status}")

        # Adjust to match Selenium Hub's actual response format
        if status.get('value', {}).get('ready', False):
            logger.info("Selenium Hub is up and running ✅")
            return True
        else:
            logger.warning("Selenium Hub is not ready ❌")
            return False

    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking Selenium Hub status: {e}")
        return False

def test_case_1(driver):
    """Test Case 1: Validate home page."""
    try:
        driver.get('https://useinsider.com')
        if driver.current_url == 'https://useinsider.com/':
            logger.info("Test case 1: Insider home page opened successfully ✅")
        else:
            logger.warning("Test case 1: Insider home page didn't open successfully ❌")
    except Exception as e:
        logger.error(f"Test case 1 encountered an error: {e}")

def test_case_2(driver):
    """Test navigation to the Careers page and verify elements present."""
    try:
        company_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Company'))
        )
        company_element.click()
        logger.info("Test case 2: 'Company' navigation clicked successfully ✅.")

        careers_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Careers'))
        )
        careers_element.click()
        logger.info("Test case 2: 'Careers' link clicked successfully ✅.")

        WebDriverWait(driver, 10).until(
            EC.url_contains('careers')
        )
        logger.info("Test case 2: 'Careers' page opened successfully ✅.")

        life_at_insider_block = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Life at Insider']"))
        )
        
        if life_at_insider_block.is_displayed():
            logger.info("Test case 2: 'Life at Insider' block is visible ✅.")
        else:
            logger.warning("Test case 2: 'Life at Insider' block is not visible ❌.")

        our_locations_block = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "career-our-location"))
        )

        if our_locations_block.is_displayed():
            logger.info("Test case 2: 'Our Locations' block is visible ✅.")
        else:
            logger.warning("Test case 2: 'Our Locations' block is not visible ❌.")


        location_elements = our_locations_block.find_elements(By.CLASS_NAME, "glide__slide")

        if location_elements:
            logger.info(f"Test case 2: Found {len(location_elements)} locations ✅.")
        else:
            logger.warning("Test case 2: No locations found ❌.")
    except Exception as e:
        logger.error(f"Test case 2 encountered an error: {e}")

def test_case_3(driver):
    """Test navigation and validation of the QA careers page."""
    try:
        driver.get('https://useinsider.com/careers/quality-assurance/')

        see_all_jobs_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
        )
        see_all_jobs_button.click()
        logger.info("Test case 3: Clicked 'See all QA jobs' button successfully ✅")

        time.sleep(20)

        department_filter = driver.find_element(By.ID, "select2-filter-by-department-container")
        selected_department = department_filter.get_attribute("title")

        if selected_department == "Quality Assurance":
            logger.info("Test case 3: Department 'Quality Assurance' is already selected ✅")
        else:
            logger.warning("Test case 3: Department 'Quality Assurance' is not selected. Waiting...")
            time.sleep(20)

        filter_by_location_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "select2-filter-by-location-container"))
        )
        filter_by_location_dropdown.click()
        logger.info("Test case 3: Opened 'Filter by Location' dropdown successfully ✅")

        time.sleep(5)

        location_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[text()='Istanbul, Turkey']"))
        )
        location_option.click()
        logger.info("Test case 3: Selected 'Istanbul, Turkey' from the filter list successfully ✅")

        time.sleep(5)

        job_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jobs-list"))
        )

        job_items = job_list.find_elements(By.CLASS_NAME, "position-list-item-wrapper")

        if not job_items:
            logger.warning("Test case 3: No job items found ❌")
        else:
            job_item = job_items[0]
            title = job_item.find_element(By.CLASS_NAME, "position-title").text
            department = job_item.find_element(By.CLASS_NAME, "position-department").text
            location = job_item.find_element(By.CLASS_NAME, "position-location").text

            logger.info(f"Job Title: {title}")
            logger.info(f"Department: {department}")
            logger.info(f"Location: {location}")

            if "Quality Assurance" in title and department == "Quality Assurance" and location == "Istanbul, Turkey":
                logger.info("Test case 3: Job details validation passed ✅")
            else:
                logger.warning("Test case 3: Job details validation failed ❌")
    except Exception as e:
        logger.error(f"Test case 3: QA careers page test encountered an error: {e}")

def test_case_4(driver):
    """Test Case 4: Validate job URLs."""
    try:
        job_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jobs-list"))
        )

        job_items = job_list.find_elements(By.CLASS_NAME, "position-list-item-wrapper")

        if not job_items:
            logger.warning("Test case 4: No job items found ❌")
        else:
            for job_item in job_items:
                try:
                    view_role_button = job_item.find_element(By.XPATH, ".//a[@class='btn btn-navy rounded pt-2 pr-5 pb-2 pl-5']")
                    href = view_role_button.get_attribute("href")

                    if href and href.startswith("https://jobs.lever.co/useinsider/"):
                        logger.info(f"Test case 4: Redirect URL is correct for job: {job_item.text} ✅")
                    else:
                        logger.warning(f"Test case 4: Incorrect redirect URL for job: {job_item.text} ❌")

                except Exception as e:
                    logger.error(f"Error processing job: {e}")
                    continue

    except Exception as e:
        logger.error(f"Error in Test Case 4: {e}")

if __name__ == "__main__":
    while True:
        try:
            if check_selenium_hub_status():
                test_case_1(driver)
                test_case_2(driver)
                test_case_3(driver)
                test_case_4(driver)
            else:
                logger.warning("Skipping tests due to Selenium Hub being down.")
        finally:
            time.sleep(5)

        logger.info("Restarting tests after a pause...")
        driver.quit()
        time.sleep(5)
        driver = webdriver.Remote(command_executor=remote_url, options=options)
