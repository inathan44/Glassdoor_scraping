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

from urllib.parse import urljoin


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

        current_url = driver.current_url

        new_param = "sortBy=date_desc"
        new_url = f"{current_url}&{new_param}"

        driver.get(new_url)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "filter_jobType"))
        )

        # # Find and click on the div with attribute "data-test" and value "sort-by-header"
        # div_element = driver.find_element(
        #     By.CSS_SELECTOR, "div[data-test='sort-by-header']"
        # )
        # div_element.click()

        # # Wait for the sorting options to appear
        # time.sleep(2)

        # # Find and click on the button with attribute "data-test" and value "date_desc"
        # button_element = driver.find_element(
        #     By.CSS_SELECTOR, "button[data-test='date_desc']"
        # )
        # button_element.click()

        # # Wait for the page to reload with the new sorting applied
        # time.sleep(5)

    except Exception as e:
        print("error when searching:", repr(e))
