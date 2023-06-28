import random


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


def get_list_of_proxies():
    with open("valid_proxies.txt", "r") as f:
        proxies = f.read().split("\n")

    return proxies


def get_random_proxy(proxy_list):
    proxy = random.choice(proxy_list)
    return proxy


def format_proxies(proxy):
    proxies = {}
    proxies["http"] = f"http://{proxy}"
    proxies["https"] = f"https://{proxy}"
    return proxies
