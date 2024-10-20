from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import pytz

# Initialize ChromeOptions
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

# Initialize WebDriver with the options
driver = webdriver.Chrome(options=options)

# Function to get the current time in CET
def get_cet_time():
    cet = pytz.timezone('CET')
    return datetime.now(cet).strftime('%Y-%m-%d %H:%M:%S')

def test_case_1(driver):
    """Test Case 1: Validate home page."""
    try:
        driver.get('https://useinsider.com')
        if driver.current_url == 'https://useinsider.com/':
            print(f"{get_cet_time()} - Test case 1: Insider home page opened successfully ✅")
        else:
            print(f"{get_cet_time()} - Test case 1: Insider home page didn't open successfully ❌")
    except Exception as e:
        print(f"{get_cet_time()} - Test case 1 encountered an error: {e}")

def test_case_2(driver):
    """Test navigation to the Careers page and verify elements present."""
    try:
        company_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Company'))
        )
        company_element.click()
        print(f"{get_cet_time()} - Test case 2: 'Company' navigation clicked successfully ✅.")

        careers_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Careers'))
        )
        careers_element.click()
        print(f"{get_cet_time()} - Test case 2: 'Careers' link clicked successfully ✅.")

        WebDriverWait(driver, 10).until(
            EC.url_contains('careers')
        )
        print(f"{get_cet_time()} - Test case 2: 'Careers' page opened successfully ✅.")

        life_at_insider_block = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Life at Insider']"))
        )
        
        if life_at_insider_block.is_displayed():
            print(f"{get_cet_time()} - Test case 2: 'Life at Insider' block is visible ✅.")
        else:
            print(f"{get_cet_time()} - Test case 2: 'Life at Insider' block is not visible ❌.")

        our_locations_block = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "career-our-location"))
        )

        if our_locations_block.is_displayed():
            print(f"{get_cet_time()} - Test case 2: 'Our Locations' block is visible ✅.")
        else:
            print(f"{get_cet_time()} - Test case 2: 'Our Locations' block is not visible ❌.")

        # 7. Validate that multiple locations are listed
        location_elements = our_locations_block.find_elements(By.CLASS_NAME, "glide__slide")

        if location_elements:
            print(f"{get_cet_time()} - Test case 2: Found {len(location_elements)} locations ✅.")
        else:
            print(f"{get_cet_time()} - Test case 2: No locations found ❌.")
    except Exception as e:
        print(f"{get_cet_time()} - Test case 2 encountered an error: {e}")

def test_case_3(driver):
    """Test navigation and validation of the QA careers page."""
    try:
        driver.get('https://useinsider.com/careers/quality-assurance/')

        see_all_jobs_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
        )
        see_all_jobs_button.click()
        print(f"{get_cet_time()} - Test case 3: Clicked 'See all QA jobs' button successfully ✅")

        time.sleep(20)

        department_filter = driver.find_element(By.ID, "select2-filter-by-department-container")
        selected_department = department_filter.get_attribute("title")

        if selected_department == "Quality Assurance":
            print(f"{get_cet_time()} - Test case 3: Department 'Quality Assurance' is already selected ✅")
        else:
            print(f"{get_cet_time()} - Test case 3: Department 'Quality Assurance' is not selected. Waiting...")
            time.sleep(20)

        filter_by_location_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "select2-filter-by-location-container"))
        )
        filter_by_location_dropdown.click()
        print(f"{get_cet_time()} - Test case 3: Opened 'Filter by Location' dropdown successfully ✅")

        time.sleep(5)

        location_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[text()='Istanbul, Turkey']"))
        )
        location_option.click()
        print(f"{get_cet_time()} - Test case 3: Selected 'Istanbul, Turkey' from the filter list successfully ✅")

        time.sleep(5)

        job_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jobs-list"))
        )

        job_items = job_list.find_elements(By.CLASS_NAME, "position-list-item-wrapper")

        if not job_items:
            print(f"{get_cet_time()} - Test case 3: No job items found ❌")
        else:
            job_item = job_items[0]
            title = job_item.find_element(By.CLASS_NAME, "position-title").text
            department = job_item.find_element(By.CLASS_NAME, "position-department").text
            location = job_item.find_element(By.CLASS_NAME, "position-location").text

            print(f"Job Title: {title}")
            print(f"Department: {department}")
            print(f"Location: {location}")

            if "Quality Assurance" in title and department == "Quality Assurance" and location == "Istanbul, Turkey":
                print(f"{get_cet_time()} - Test case 3: Job details validation passed ✅")
            else:
                print(f"{get_cet_time()} - Test case 3: Job details validation failed ❌")
    except Exception as e:
        print(f"{get_cet_time()} - Test case 3: QA careers page test encountered an error: {e}")

def test_case_4(driver):
    try:
        job_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jobs-list"))
        )

        job_items = job_list.find_elements(By.CLASS_NAME, "position-list-item-wrapper")

        if not job_items:
            print(f"{get_cet_time()} - Test case 4: No job items found ❌")
        else:

            for job_item in job_items:
                try:

                    view_role_button = job_item.find_element(By.XPATH, ".//a[@class='btn btn-navy rounded pt-2 pr-5 pb-2 pl-5']")


                    href = view_role_button.get_attribute("href")


                    if href and href.startswith("https://jobs.lever.co/useinsider/"):
                        print(f"{get_cet_time()} - Test case 4: Redirect URL is correct for job: {job_item.text} ✅")
                    else:
                        print(f"{get_cet_time()} - Test case 4: Incorrect redirect URL for job: {job_item.text} ❌")

                except Exception as e:
                    print(f"{get_cet_time()} - Error processing job: {e}")
                    continue

    except Exception as e:
        print(f"{get_cet_time()} - Error in Test Case 4: {e}")


if __name__ == "__main__":
    try:
        test_case_1(driver)
        test_case_2(driver)
        test_case_3(driver)
        test_case_4(driver)
    finally:
        time.sleep(5)
        driver.quit()
