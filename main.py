from helper_functions import (
    get_headers_list,
    get_random_header,
    filter_strings_with_keyword,
    find_sentences_with_keyword,
    format_into_bullets,
    format_into_search_term,
)

from paginate import next_page_found, go_to_next_page
from search_for_jobs import search_jobs_by_keywords

import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

from scrape_page_of_listings import scrape_listings

KEYWORDS = ["netsuite"]
URL = "https://www.glassdoor.com/Job/"

# Set up and open chrome driver

# Enable logging
logging.basicConfig(level=logging.INFO)

# Set up Chrome driver options
chrome_options = Options()

headers_list = get_headers_list()
random_headers = get_random_header(headers_list)

# Commenting out headless mode for troubleshooting
chrome_options.add_argument("--headless=new")

# Put random headers for request
for header, value in random_headers.items():
    chrome_options.add_argument(f"--header={header}:{value}")

chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1080,720")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument(f"--proxy-server={proxy}")

# Set path to your Chrome driver executable
webdriver_path = "/path/to/chromedriver"

# Instantiate Chrome driver
driver = webdriver.Chrome(options=chrome_options)


try:
    # Run search
    search_jobs_by_keywords(url=URL, keywords=KEYWORDS, driver=driver)

    page = 1
    while True:  # While there is a next page, run the script
        # Scrape listings on current page
        scrape_listings(keywords=KEYWORDS, driver=driver)

        if next_page_found(driver=driver):
            print("the next page is found")
            go_to_next_page(driver=driver)
        else:
            break

        print(f"finished scraping page {page}")
        page += 1
except Exception as e:
    print("error:", repr(e))
finally:
    print("finished scraping")
    driver.quit()
