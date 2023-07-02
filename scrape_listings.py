import time
import requests
from bs4 import BeautifulSoup
from helper_functions import (
    filter_strings_with_keyword,
    find_sentences_with_keyword,
    request_through_proxy,
)
from write_to_excel import write_to_excel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrapeArrayOfListings(links, keywords):
    scraped_info = []

    # Required when sending request to avoid getting denied
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # variable to limit how many listing to scrape if I select to
    max = 0

    for idx, link in enumerate(links):
        job_link = link.get("href")
        max += 1

        print(
            "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        )
        # run another search on each job listing found on the page
        url = "https://www.glassdoor.com" + job_link
        response = request_through_proxy(url)

        print("url:", url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        print("status code:", response.status_code)

        descriptions = soup.find(attrs={"class": "desc"})

        title = soup.find(attrs={"data-test": "job-title"})
        company_name = soup.find(attrs={"data-test": "employer-name"})

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

                # print("array of strings", keyword_snippets)
                print("\n")

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

                keyword_snippets[keyword] = ", ".join(keyword_snippets[keyword])
                # print("concat strings", keyword_snippets)

        for keyword in keywords:
            print("keyword snippets:", keyword_snippets[keyword])
            print("keyword snippets length:", len(keyword_snippets[keyword]))
            print("keyword snippets type:", type(keyword_snippets[keyword]))

        current_page_information = [
            title.get_text(),
            company_name.get_text(),
            url,
            keyword_snippets,
        ]

        ### temporarily stopping writing to excel ###
        # if len(keyword_snippets) > 0:
        #     write_to_excel("glassdoor_info.xlsx", current_page_information)

        scraped_info.append(
            {
                "title": title.get_text(),
                "company_name": company_name.get_text(),
                "url": url,
                "keyword_snippets": keyword_snippets,
            }
        )

        # Set up the WebDriver (e.g., ChromeDriver)
        driver = webdriver.Chrome()

        # Load the page in Selenium WebDriver
        driver.get(url)

        # Find the span element with innerHTML "Company"
        company_span = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Company')]")
            )
        )

        # Click on the span element to reveal the other information
        company_span.click()

        # Wait for the content to load, if necessary
        # You may need to introduce a delay or use explicit waits

        # Extract the revenue information using Selenium
        revenue_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "revenue"))
        )
        revenue = revenue_element.text

        # Close the WebDriver
        driver.quit()

        print(f"Finished with scrape #{idx+1}")

        time.sleep(1)

    return scraped_info


def scrape_pages(list_of_pages):
    scraped_info = []
    for page in list_of_pages[:4]:
        scraped_info.append(scrapeArrayOfListings(page))
