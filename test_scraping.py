import requests
from bs4 import BeautifulSoup
import time
from search_script import findJobsUrlByKeyword
from scrape_listings import scrapeArrayOfListings

# Required when sending request to avoid getting denied
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Send a GET request to the website
url = findJobsUrlByKeyword("salesforce")
# url = "https://www.glassdoor.com/Job/salesforce-jobs-SRCH_KO0,10.htm"
response = requests.get(url, headers=headers)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Pulls all links from the search results page
links = soup.find_all("a", {"class": "jobCard"})


print(len(scrapeArrayOfListings(links)))
