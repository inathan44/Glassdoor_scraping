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
            original_sentence = paragraph.split(". ")[sentences.index(sentence)].strip()
            matching_sentences.append(original_sentence)
    return matching_sentences


def filter_strings_with_keyword(strings, keyword):
    matching_strings = []
    for string in strings:
        if keyword.lower() in string.lower():
            matching_strings.append(string)
    return matching_strings


# def get_list_of_proxies():
#     with open("valid_proxies.txt", "r") as f:
#         proxies = f.read().split("\n")

#     return proxies


# def get_random_proxy(proxy_list):
#     proxy = random.choice(proxy_list)
#     return proxy


# def format_proxies(proxy):
#     proxies = {}
#     proxies["http"] = f"http://{proxy}"
#     proxies["https"] = f"https://{proxy}"
#     return proxies


def format_into_search_term(list_of_keywords):
    formatted_keywords = " ".join([f'"{keyword}"' for keyword in list_of_keywords])
    return formatted_keywords


def get_headers_list():
    response = requests.get(
        "http://headers.scrapeops.io/v1/user-agents?api_key=" + SCRAPE_OPS_API_KEY
    )
    json_response = response.json()
    return json_response.get("result", [])


def get_random_header(header_list):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]
