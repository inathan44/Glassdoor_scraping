from random import randint
from dotenv import load_dotenv
import os
import requests
import re

load_dotenv()
SCRAPE_OPS_API_KEY = os.getenv("SCRAPE_OPS_API_KEY")


def find_sentences_with_keyword(paragraph, keyword):
    paragraph_lower = paragraph.lower()
    sentences = paragraph_lower.split(". ")
    matching_sentences = []

    for sentence in sentences:
        # If keyword passed in is a list of joint keywords, parse them individually
        if isinstance(keyword, list):
            for individual_keyword in keyword:
                if individual_keyword.lower() in sentence:
                    matching_sentences.append(sentence)

        else:
            if keyword.lower() in sentence:
                matching_sentences.append(sentence)

    return matching_sentences


def filter_strings_with_keyword(strings, keyword):
    matching_strings = []
    for string in strings:
        if isinstance(keyword, list):
            for individual_keyword in keyword:
                if individual_keyword.lower() in string.lower():
                    matching_strings.append(string)
        else:
            if keyword.lower() in string.lower():
                matching_strings.append(string)

    matching_strings = " ".join(matching_strings)
    matching_strings = find_sentences_with_keyword(matching_strings, keyword)

    return matching_strings


def format_into_search_term(list_of_keywords):
    formatted_keywords = " ".join([f'"{keyword}"' for keyword in list_of_keywords])
    # temporarily only search first keyword
    # formatted_keywords = " ".join([f'"{keyword}"' for keyword in list_of_keywords[0:1]])
    return formatted_keywords


def get_headers_list():
    response = requests.get(
        "http://headers.scrapeops.io/v1/browser-headers?api_key=" + SCRAPE_OPS_API_KEY
    )
    json_response = response.json()
    return json_response.get("result", [])


def get_random_header(header_list):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]


def request_through_proxy(url_to_search):
    response = requests.get(
        url="https://proxy.scrapeops.io/v1/",
        params={
            "api_key": SCRAPE_OPS_API_KEY,
            "url": url_to_search,
        },
    )

    return response


def extract_context_sentence(text, keyword, max_words_before_after):
    # Split the text into words
    words = text.split()

    # Define a regular expression pattern to match the keyword, ignoring case
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    for i, word in enumerate(words):
        # Check if the word contains the keyword
        if re.search(pattern, word):
            keyword_index = i
            break
    else:
        keyword_index = -1

    if keyword_index != -1:
        # Calculate the start and end indices for the context
        start_index = max(keyword_index - max_words_before_after, 0)
        end_index = min(keyword_index + max_words_before_after + 1, len(words))

        # Extract the context sentence
        context = " ".join(words[start_index:end_index])

        return context

    return text


def format_into_bullets(array_of_strings, keyword):
    formatted_strings = [
        "- " + s for s in array_of_strings
    ]  # Prepend "-" to each string

    if isinstance(keyword, list):
        for indiv_keyword in keyword:
            formatted_strings = [
                extract_context_sentence(
                    text=string, keyword=indiv_keyword, max_words_before_after=20
                )
                for string in formatted_strings
            ]
    else:
        formatted_strings = [
            extract_context_sentence(
                text=string, keyword=keyword, max_words_before_after=20
            )
            for string in formatted_strings
        ]

    joined_strings = "\n".join(formatted_strings)  # Join strings with line break

    return joined_strings


from bs4 import BeautifulSoup


def find_company_title(html):
    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Find the parent div with class starting with "JobDetails_jobDetailsHeader"
    parent_div = soup.find(
        "div", class_=lambda x: x and x.startswith("JobDetails_jobDetailsHeader")
    )

    if parent_div:
        # Check if there is an "a" tag inside the parent div
        logo_link = parent_div.find("a")

        if logo_link:
            # If there is a logo, find the second div inside the "a" tag
            div_elements_inside_logo = logo_link.find_all("div")

            if len(div_elements_inside_logo) >= 2:
                second_div_inside_logo = div_elements_inside_logo[1]
                return second_div_inside_logo.text.strip()
            else:
                return "N/A"
        else:
            # If there is no "a" tag (logo), find the first div directly within the parent div
            first_div = parent_div.find("div")

            if first_div:
                return first_div.text.strip()
            else:
                return "No div elements found directly within the parent div."
    else:
        return "Parent div not found."
