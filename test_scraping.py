import requests
from bs4 import BeautifulSoup
import time

# Required when sending request to avoid getting denied
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Send a GET request to the website
url = "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10.htm"
response = requests.get(url, headers=headers)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Pulls all links from the search results page
links = soup.find_all("a", {"class": "jobCard"})

max = 0

for link in links:
    job_link = link.get("href")
    max += 1

    # run another search on each job listing found on the page
    url = "https://www.glassdoor.com" + job_link
    response = requests.get(url, headers=headers)

    print("URL <><><><><><><><><><>", url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    print("status code:", response.status_code)

    descriptions = soup.find(attrs={"class": "desc"})
    title = soup.find(attrs={"data-test": "job-title"})

    print("title", title.get_text() if title else "No Title soprry")

    text_list = [text for text in descriptions.stripped_strings]

    text_list_words_only = " ".join(text_list)

    # print("text list words only", text_list_words_only.split(" "))

    # print("Text list from stripped string:", repr(text_list))
    print("\n")

    # all_descriptions = soup.find_all(attrs={"class": "desc"})

    # for description in descriptions:
    #     print("Description get text:", description.get_text(" ", strip=True))

    print("\n")
    print("\n")
    print("\n")
    print("\n")

    if max >= 5:
        break
    time.sleep(3)
