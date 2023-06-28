import time
import requests
from bs4 import BeautifulSoup
from helper_functions import filter_strings_with_keyword, find_sentences_with_keyword
from write_to_excel import write_to_excel


def scrapeArrayOfListings(links, keyword):
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
        response = requests.get(url, headers=headers)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        print("status code:", response.status_code)

        descriptions = soup.find(attrs={"class": "desc"})

        title = soup.find(attrs={"data-test": "job-title"})
        company_name = soup.find(attrs={"data-test": "employer-name"})

        if len(descriptions) > 2:
            print("method 1")

            array_of_strings = [
                description.get_text(separator=" ", strip=True)
                for description in descriptions
            ]

            keyword_snippets = filter_strings_with_keyword(array_of_strings, keyword)

            print("array of strings", keyword_snippets)
            print("\n")

        else:
            print("method 2")
            concatenated_strings = " ".join(
                [description.get_text(" ", strip=True) for description in descriptions]
            )

            keyword_snippets = find_sentences_with_keyword(
                concatenated_strings, keyword
            )

            print("concat strings", keyword_snippets)

        keyword_snippets = ", ".join(keyword_snippets)

        current_page_information = [
            title.get_text(),
            company_name.get_text(),
            url,
            keyword_snippets,
        ]

        write_to_excel("glassdoor_info.xlsx", current_page_information)

        scraped_info.append(
            {
                "title": title.get_text(),
                "company_name": company_name.get_text(),
                "url": url,
                "keyword_snippets": keyword_snippets,
            }
        )

        print(f"Finished with scrape #{idx+1}")

        time.sleep(1)

    return scraped_info


def scrape_pages(list_of_pages):
    scraped_info = []
    for page in list_of_pages[:4]:
        scraped_info.append(scrapeArrayOfListings(page))
