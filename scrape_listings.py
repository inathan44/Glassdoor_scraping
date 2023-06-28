import time
from bs4 import BeautifulSoup
import requests
from helper_functions import filter_strings_with_keyword, find_sentences_with_keyword


def scrapeArrayOfListings(links):
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

            array_of_strings = [description.get_text() for description in descriptions]

            # print("array of strings", array_of_strings)

            keyword_snippets = filter_strings_with_keyword(
                array_of_strings, "salesforce"
            )

        else:
            print("method 2")
            concatenated_strings = " ".join(
                [description.get_text(" ", strip=True) for description in descriptions]
            )
            # print("concat strings", concatenated_strings)

            keyword_snippets = find_sentences_with_keyword(
                concatenated_strings, "salesforce"
            )

        # for description in descriptions:
        #     print("Description get text:", description.get_text(" ", strip=True))
        #     pass

        # print([title, company_name, url])
        # print("Title:", title.get_text() if title else "No title real sorry about it.")
        # print("company name", company_name.get_text())
        # print("keyword snippets", keyword_snippets)
        # print("url", url)

        # print("\n")
        # print("\n")
        # print("\n")

        if max >= 200:
            break

        scraped_info.append(
            {
                "title": title.get_text(),
                "company_name": company_name.get_text(),
                "url": url,
                "keyword_snippets": keyword_snippets,
            }
        )

        print(f"Finished with scrape #{idx}")

        time.sleep(1)

    return scraped_info
