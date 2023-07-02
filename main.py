import requests
from bs4 import BeautifulSoup
from pagination_script import findPageUrlsByKeyword
from scrape_listings import scrapeArrayOfListings, scrape_pages
from helper_functions import (
    # get_list_of_proxies,
    # get_random_proxy,
    # format_proxies,
    format_into_search_term,
    get_headers_list,
    get_random_header,
    request_through_proxy,
)
import os
from dotenv import load_dotenv

load_dotenv()

# TEMPORARY URLS
urls = [
    "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10.htm?clickSource=searchBox"  # ,
    #     "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10_IP2.htm?includeNoSalaryJobs=true&pgc=AB4AAYEAHgAAAAAAAAAAAAAAAgg%2BiHYASgEBAQcPguUxjgoriLIR8a6n5HkeZpJKZEGiYgIOll%2BshphhOAUwkryXL7%2FtNFRpxgaVUnjeRpftdyg4XwgNCWZ5HQefXAsVkub%2FAAA%3D",
    #     "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10_IP3.htm?includeNoSalaryJobs=true&pgc=AB4AAoEAPAAAAAAAAAAAAAAAAgg%2BiHYAfgECAQ8gCgXyDlEfyzTi2AVVZKfmmMElt1laRkVk7xsWeCsySdg08oEJSSohYPcckDQ2N56vtkPDadOlFZQ2gjMCjzbMz%2Bkdr%2BT68kMDXfMtSezBZcJD6LWI6EjbWzyYstYN8CZuw4s20zllahFnL8aH89xZcljlPYg4iN8xHQAA",
    #     "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10_IP4.htm?includeNoSalaryJobs=true&pgc=AB4AA4EAWgAAAAAAAAAAAAAAAgg%2BiHYAuAECAQ8gCgNyzE2BeUCy6LC4P8bBhkbQipR2i%2FPNzcL2SH%2FGrAPVY7Qbh62%2BIoBVF7t2qxEPFx0%2FnefVBjM90y67yYpAihek0y5jAlsMo%2BFxthkyzi9KQaHRBHcUk4Tsle8JXsF4Derv3yxKaRxyEeXdXZRWIcAS0J%2FKHIazzxjI7yOer5NK8CFU91%2BOd1UG2yWK1YBtkxkghhn2T4x8NpiIC4ug41IGllBeeZbcBgt6%2F9ICweskre0AAA%3D%3D",
    #     "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10_IP5.htm?includeNoSalaryJobs=true&pgc=AB4ABIEAeAAAAAAAAAAAAAAAAgg%2BiHYA4wEFAQ8gDS4GDgYmBkgnW3vovA%2BL9kLhbExsK%2Ba0rQgkzIoEiP7mJx504GAwHf5LlABuYB3MWTKTl5tVpND3XTLWRM1Po7KgXYc2W4bGqQux%2FcgFSbUv3Te7sGcmednmO3NqPxionYUZqZgjMfqJVbQXNRrWzsEFH41hHwOd5yBnKqeA3hBtPyf2q6QDilZAm%2F%2BANBPRUAMHiAszLsOroqpRRcaYiKacmNDT1T8uIzZ05ogKC%2BzfOqyEhByBaYq0NmX7UWykQ7hR%2B78QtTsXxPnmCEtpBSuBEyni9K2brRPQsW86AAA%3D",
    #     "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10_IP6.htm?includeNoSalaryJobs=true&pgc=AB4ABYEAlgAAAAAAAAAAAAAAAgg%2BiHYBDQEDAR9ADh4GSwE5Gt08L6VIKzB%2FUaoPCX09PxcNVjtuKmi1Y1giWTSR6WoWjHkwBdfNATzyyRpJK6F3TM8XCjrok8ezod2A6L0st8AMzjgL1d%2F0TqCfAzoKgke8DkJqoU0L%2BgC1LM0eZvgoLS7xG8CSXrc9tWf1XPochFn8WUv8Pw0kA75PjNqV%2FnFvA%2FLMx5qwnekZbpTa5dGs0bGY8P9%2BeR9dI5EqtsanBa7HT%2F0Qc68VOW%2B%2Frkmgqu%2Flh8QZNmQHkcnSTskKzBkWvLZ7mmmYA%2Fwbe6DQYfPWQG4EgS8fMCoWI8WIPiNKtyCpmaT7nde2O7%2BBhsmzGyQJwxjEzruqPpWmMZFvX4fJYl6dAAA%3D",
    #     "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10_IP7.htm?includeNoSalaryJobs=true",
    #     "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10_IP8.htm?includeNoSalaryJobs=true",
]

scraped_info = []

# list_of_proxies = get_list_of_proxies()
# random_proxy = get_random_proxy(list_of_proxies)

# formatted_proxies = format_proxies(random_proxy)

proxy_user = os.getenv("SMART_PROXY_USER")
proxy_pass = os.getenv("SMART_PROXY_PASSWORD")
proxy_host = os.getenv("SMART_PROXY_HOST")
proxy_port = os.getenv("SMART_PROXY_PORT")

proxies = {
    "http": f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}",
    "https": f"https://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}",
}

# print("proxies:", proxies)

KEYWORDS = ["netsuite"]

search_term = format_into_search_term(KEYWORDS)


# Required when sending request to avoid getting denied
headers_list = get_headers_list()
# random_headers = {"User-Agent": get_random_header(headers_list)}
random_headers = get_random_header(headers_list)
# print("headers:", random_headers)

# Send a GET request to the website
urls = findPageUrlsByKeyword(search_term)
# print("Paginated URLS", urls)

# Loop through each of the urls, scrape information and port it into excel
for url in urls:
    proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    try:
        response = request_through_proxy(url)

        print("response", response.status_code)
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Pulls all links/URLs from the search results page
        listings = soup.find_all("a", {"class": "jobCard"})
        # listings = [listing.get("href") for listing in listings]

        result = scrapeArrayOfListings(listings, KEYWORDS)

        print(result)

        scraped_info.append(result)
    except Exception as e:
        print("An exception occurred:", str(e))
