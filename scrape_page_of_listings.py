from helper_functions import (
    filter_strings_with_keyword,
    find_sentences_with_keyword,
    format_into_bullets,
    extract_context_sentence,
    find_company_title,
)


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


def scrape_listings(keywords, driver):
    max_retries = 3

    try:
        # Find all <a> tags with class "jobCard"
        time.sleep(5)
        # job_card_links = driver.find_elements(By.CSS_SELECTOR, "a.jobCard")
        job_card_links = driver.find_elements(By.CSS_SELECTOR, ".jobCard")

        print("length of cards on page", len(job_card_links))

        if len(job_card_links) % 20 == 0:
            most_recent_listings = 20
        else:
            most_recent_listings = len(job_card_links) % 20
        print("num of most recent listings:", most_recent_listings)

        max = 30
        # Click on each <a> tag with a delay of one second
        for idx, link in enumerate(job_card_links[-most_recent_listings:]):
            # Placeholder variable definitions
            revenue = "N/A"
            industry = "N/A"
            size = "N/A"
            company_website = "N/A"

            # if idx > max:
            #     break
            print(
                "================================================================================================================================================================================================================================================"
            )
            # Check if the modal is present and close it
            # try:
            #     modal = driver.find_element(By.CLASS_NAME, "actionBarMt0")
            #     if modal.is_displayed():
            #         modal_close_button = modal.find_element(By.TAG_NAME, "button")
            #         modal_close_button.click()

            #         time.sleep(2)  # Give some time for the modal to close
            # except Exception as e:
            #     print(repr(e))

            # Find the modal element with a class that starts with "Modal"
            try:
                modal = driver.find_element(By.CSS_SELECTOR, '[class^="Modal"]')

                # Check if the modal is displayed
                if modal.is_displayed():
                    # Find the button with the classname 'CloseButton' inside the modal
                    try:
                        modal_close_button = modal.find_element(
                            By.CLASS_NAME, "CloseButton"
                        )
                        modal_close_button.click()

                        time.sleep(2)  # Give some time for the modal to close
                    except Exception as e:
                        print("CloseButton not found in the modal!")
                else:
                    print("Modal is not displayed.")
            except Exception as e:
                print("Modal not found!")

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
                id_job_title = driver.find_elements(
                    By.CSS_SELECTOR, "[id^='jd-job-title']"
                )

                job_title = id_job_title[0].text

                company_name = find_company_title(html=html_source)

                print("company:", company_name)

                link_a_element = link.find_element(By.CSS_SELECTOR, "a[href]")

                url = link_a_element.get_attribute("href")

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

                # descriptions = soup.find(attrs={"class": "desc"})
                descriptions = soup.find(
                    "div",
                    class_=lambda x: x and x.startswith("JobDetails_blurDescription"),
                )

                keyword_snippets = {}

                if len(descriptions) > 2:
                    print("method 1")

                    for keyword in keywords:
                        print("KEYWORD:", keyword)
                        array_of_strings = [
                            description.get_text(separator=" ", strip=True)
                            for description in descriptions
                        ]

                        if isinstance(keyword, list):
                            joined_keyword = " + ".join(keyword)
                            keyword_snippets[
                                joined_keyword
                            ] = filter_strings_with_keyword(array_of_strings, keyword)
                        else:
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

                        if isinstance(keyword, list):
                            joined_keyword = " + ".join(keyword)
                            keyword_snippets[
                                joined_keyword
                            ] = find_sentences_with_keyword(
                                concatenated_strings, keyword
                            )
                        else:
                            keyword_snippets[keyword] = find_sentences_with_keyword(
                                concatenated_strings, keyword
                            )

                for keyword in keywords:
                    if isinstance(keyword, list):
                        joined_keyword = " + ".join(keyword)

                        keyword_snippets[joined_keyword] = format_into_bullets(
                            keyword_snippets[joined_keyword], keyword
                        )
                    else:
                        keyword_snippets[keyword] = format_into_bullets(
                            keyword_snippets[keyword], keyword
                        )

                # print("Data posted:", job_age)
                # print("\n")
                print("Company name:", company_name)
                print("\n")
                print("job title:", job_title)
                print("\n")
                # print("keyword snippets", keyword_snippets)
                # print("\n")
                print("url:", url)
                print("\n")
                print("size:", size)
                print("indsutry:", industry)
                print("revenue:", revenue)

                # write_to_excel(
                #     file_name="scrape_data.xlsx",
                #     # sheet_name=" + ".join(keywords),
                #     sheet_name=keywords[0],
                #     company=company_name,
                #     title=job_title,
                #     url=url,
                #     size=size,
                #     industry=industry,
                #     revenue=revenue,
                #     age=job_age,
                #     keyword_snippets=keyword_snippets,
                #     company_website=company_website,
                # )
                write_to_excel(
                    file_name="scrape_data.xlsx",
                    # sheet_name=" + ".join(keywords),
                    sheet_name=keywords[0],
                    company=company_name,
                    title=job_title,
                    url=url,
                    size=size,
                    industry=industry,
                    revenue=revenue,
                    age="N/A",
                    keyword_snippets=keyword_snippets,
                    company_website=company_website,
                )

            except Exception as e:
                print(repr(e))

    except Exception as e:
        modal = driver.find_element(By.CLASS_NAME, "actionBarMt0")
        if modal.is_displayed():
            print("modal likely caused the error")
        print("An exception occurred:", repr(e))

    finally:
        print(f"finished scraping this many listings: {idx+1}")
