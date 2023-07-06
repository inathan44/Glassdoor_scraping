from random import randint
from dotenv import load_dotenv
import os
import requests

load_dotenv()
SCRAPE_OPS_API_KEY = os.getenv("SCRAPE_OPS_API_KEY")


def find_sentences_with_keyword(paragraph, keyword):
    paragraph_lower = paragraph.lower()
    sentences = paragraph_lower.split(". ")
    matching_sentences = []
    for sentence in sentences:
        if keyword.lower() in sentence:
            # original_sentence = paragraph.split(". ")[sentences.index(sentence)].strip()
            matching_sentences.append(sentence)
    return matching_sentences


def filter_strings_with_keyword(strings, keyword):
    matching_strings = []
    for string in strings:
        if keyword.lower() in string.lower():
            matching_strings.append(string)
    # matching_strings = matching_strings.join(" ")
    matching_strings = " ".join(matching_strings)
    matching_strings = find_sentences_with_keyword(matching_strings, keyword)

    return matching_strings
    # return " ".join(matching_strings)


def format_into_search_term(list_of_keywords):
    formatted_keywords = " ".join([f'"{keyword}"' for keyword in list_of_keywords])
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


def format_into_bullets(array_of_strings):
    formatted_strings = [
        "- " + s for s in array_of_strings
    ]  # Prepend "-" to each string
    joined_strings = "\n".join(formatted_strings)  # Join strings with line break
    return joined_strings
