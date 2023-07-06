from helper_functions import (
    get_headers_list,
    get_random_header,
    filter_strings_with_keyword,
    find_sentences_with_keyword,
    format_into_bullets,
    format_into_search_term,
)

import logging

from selenium import webdriver

# from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup


def search_jobs_by_keywords(url, keywords, driver):
    try:
        # Open Glassdoor website
        driver.get("https://www.glassdoor.com/Job/")

        # Find and interact with the search input field
        search_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "sc.keyword"))
        )

        print("search term:", format_into_search_term(keywords))

        search_input.send_keys(format_into_search_term(keywords))
        search_input.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "filter_jobType"))
        )
    except Exception as e:
        print("error when searching:", repr(e))
