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
