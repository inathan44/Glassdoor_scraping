from helper_functions import (
    filter_strings_with_keyword,
    find_sentences_with_keyword,
    format_into_bullets,
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
from selenium.common.exceptions import StaleElementReferenceException
import time
from bs4 import BeautifulSoup

from write_to_excel import write_to_excel


KEYWORDS = [""]


def scrape_listings(keywords, driver):
    max_retries = 3

    try:
        # Find all <a> tags with class "jobCard"
        time.sleep(5)
        job_card_links = driver.find_elements(By.CSS_SELECTOR, "a.jobCard")
        print("length of cards on page", len(job_card_links))

        max = 30
        # Click on each <a> tag with a delay of one second
        for idx, link in enumerate(job_card_links):
            # Placeholder variable definitions
            revenue = "N/A"
            industry = "N/A"
            size = "N/A"

            if idx > max:
                break
            print(
                "================================================================================================================================================================================================================================================"
            )
            # Check if the modal is present and close it
            try:
                modal = driver.find_element(By.CLASS_NAME, "actionBarMt0")
                if modal.is_displayed():
                    modal_close_button = modal.find_element(By.TAG_NAME, "button")
                    modal_close_button.click()

                    time.sleep(2)  # Give some time for the modal to close
            except Exception as e:
                pass

            retry_count = 0
            while retry_count < max_retries:
                try:
                    link.click()
                    time.sleep(2)
                    html_source = driver.page_source
                    soup = BeautifulSoup(html_source, "html.parser")
                    break  # Exit the loop if the operation is successful
                except StaleElementReferenceException:
                    print("Retrying because of stale element...")
                    retry_count += 1
                    time.sleep(3)

            # Find the div with attribute 'data-test' and value 'jobTitle'
            try:
                div_job_title = soup.find("div", {"data-test": "jobTitle"})
                job_title = div_job_title.text

                div_company_name = soup.find("div", {"data-test": "employerName"})
                company_name = div_company_name.text

                div_job_age = soup.find("div", {"data-test": "job-age"})
                job_age = div_job_age.text

                url = link.get_attribute("href")

                # Find the <span> element with the text "Size"
                span_with_size = soup.find("span", text="Size")
                if span_with_size:
                    # Find the next sibling element
                    size = span_with_size.find_next_sibling().text

                # Find the <span> element with the text "Industry"
                span_with_industry = soup.find("span", text="Industry")
                if span_with_industry:
                    industry = span_with_industry.find_next_sibling().text

                # Find the <span> element with the text "Revenue"
                span_with_revenue = soup.find("span", text="Revenue")
                if span_with_revenue:
                    revenue = span_with_revenue.find_next_sibling().text

                descriptions = soup.find(attrs={"class": "desc"})
                keyword_snippets = {}

                if len(descriptions) > 2:
                    print("method 1")

                    for keyword in keywords:
                        array_of_strings = [
                            description.get_text(separator=" ", strip=True)
                            for description in descriptions
                        ]

                        keyword_snippets[keyword] = filter_strings_with_keyword(
                            array_of_strings, keyword
                        )

                else:
                    for keyword in keywords:
                        print("method 2")
                        concatenated_strings = " ".join(
                            [
                                description.get_text(" ", strip=True)
                                for description in descriptions
                            ]
                        )

                        keyword_snippets[keyword] = find_sentences_with_keyword(
                            concatenated_strings, keyword
                        )

                for keyword in keywords:
                    keyword_snippets[keyword] = format_into_bullets(
                        keyword_snippets[keyword]
                    )

                print("Data posted:", job_age)
                print("\n")
                print("Company name:", company_name)
                print("\n")
                print("job title:", job_title)
                print("\n")
                print("keyword snippets", keyword_snippets)
                print("\n")
                print("url:", url)
                print("\n")
                print("size:", size)
                print("indsutry:", industry)
                print("revenue:", revenue)

                write_to_excel(
                    file_name="excel_testing.xlsx",
                    # sheet_name=" + ".join(keywords),
                    sheet_name=keywords[0],
                    # sheet_name="SMC + DM",
                    company=company_name,
                    title=job_title,
                    url=url,
                    size=size,
                    industry=industry,
                    revenue=revenue,
                    age=job_age,
                    keyword_snippets=keyword_snippets,
                )

            except Exception as e:
                print(repr(e))

    except Exception as e:
        modal = driver.find_element(By.CLASS_NAME, "actionBarMt0")
        if modal.is_displayed():
            print("modal likely caused the error probably")
        print("An exception occurred:", repr(e))

    finally:
        print(f"finished scraping this many listings: {idx+1}")
