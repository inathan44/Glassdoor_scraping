import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from helper_functions import get_list_of_proxies, get_random_proxy

list_of_proxies = get_list_of_proxies()

random_proxy = get_random_proxy(list_of_proxies)


def findPageUrlsByKeyword(keyword, proxy_address=None):
    if proxy_address:
        print("proxy:", random_proxy)

    # Enable logging
    logging.basicConfig(level=logging.INFO)

    # Set up Chrome driver options
    chrome_options = Options()

    # Commenting out headless mode for troubleshooting
    # chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1080,720")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument(f"--proxy-server={proxy_address}")

    # Set path to your Chrome driver executable
    webdriver_path = "/path/to/chromedriver"

    # Instantiate Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open Glassdoor website
        driver.get("https://www.glassdoor.com/Job/")

        # Find and interact with the search input field
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sc.keyword"))
        )
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "filter_jobType"))
        )

        # Get the URL of the search results page
        search_results_url = driver.current_url

        # Store the URLs of all pages
        page_urls = [search_results_url]

        # Extract URLs from subsequent pages until the "Next" button is disabled
        idx = 0
        # while True:
        for i in range(2):
            print(f"page {idx+1}")

            # Delay to allow the page to load
            time.sleep(4)

            # Check if the modal is present and close it
            try:
                modal = driver.find_element(By.CLASS_NAME, "actionBarMt0")
                if modal.is_displayed():
                    modal_close_button = modal.find_element(By.TAG_NAME, "button")
                    modal_close_button.click()

                    time.sleep(1)  # Give some time for the modal to close
            except:
                pass

            # Click on the "Next" button
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button[data-test='pagination-next']")
                    )
                )
                next_button.click()
            except Exception as e:
                print(
                    "modal found when trying to click the button"
                    if modal.is_displayed
                    else "no modal found when trying to click the next button"
                )
                print("Error trying to click the next page button", repr(e))
                break  # Break the loop if the "Next" button is disabled

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "filter_jobType"))
            )

            # Store the URL of the current page
            time.sleep(2)
            page_urls.append(driver.current_url)

            idx += 1

    except Exception as e:
        print("An exception occurred:", repr(e))

    finally:
        # Close the browser
        driver.quit()
        return page_urls
