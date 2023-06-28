import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def findJobsUrlByKeyword(keyword):
    # Enable logging
    logging.basicConfig(level=logging.INFO)

    # Set up Chrome driver options
    chrome_options = Options()
    # Commenting out headless mode for troubleshooting
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1080,720")
    chrome_options.add_argument("--no-sandbox")

    # Set path to your Chrome driver executable
    webdriver_path = "/path/to/chromedriver"

    # Instantiate Chrome driver
    driver = webdriver.Chrome(
        service=Service(executable_path=webdriver_path), options=chrome_options
    )

    try:
        # Open Glassdoor website
        driver.get("https://www.glassdoor.com/Job/")

        # Find and interact with the search input field
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sc.keyword"))
        )
        search_input.send_keys(keyword)  # Replace with your desired keyword
        search_input.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "filter_jobType"))
        )

        # Get the URL of the search results page
        search_results_url = driver.current_url
        print("Search Results URL:", search_results_url)
        # return search_results_url

        # Store the URLs of all pages
        page_urls = [search_results_url]

        # Extract URLs from subsequent pages until the "Next" button is disabled
        for _ in range(3):
            # while True:
            try:
                # Wait for the "Next" button to be clickable
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button[data-test='pagination-next']")
                    )
                )
                next_button.click()

                # Wait for the second page to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "modal_main"))
                )

                # Check if the modal is present and close it
                modal_close_button = driver.find_element(
                    By.CLASS_NAME, "modal_CloseIcon"
                )
                if modal_close_button.is_displayed():
                    modal_close_button.click()

                # Wait for the modal to disappear
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "modal_main"))
                )
                time.sleep(4)  # Wait for the page to load

                # Store the URL of the current page
                page_urls.append(driver.current_url)
                print("Page URL:", driver.current_url)
            except:
                print("There was an error abort abort")
                break

        return page_urls

    except Exception as e:
        print("An exception occurred:", repr(e))

    finally:
        # Close the browser
        driver.quit()


findJobsUrlByKeyword("salesforce")
