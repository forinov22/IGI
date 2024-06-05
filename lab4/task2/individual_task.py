import re


def count_sentences(text):
    sentences = re.split(r'[.!?]', text)
    return len(sentences), sentences


def count_sentence_types(sentences):
    narr_count = sum(1 for sentence in sentences if re.match(r'^[A-Z][^.?!]*\.$', sentence))
    interrog_count = sum(1 for sentence in sentences if re.match(r'^.*\?$', sentence))
    imper_count = sum(1 for sentence in sentences if re.match(r'^.*!$', sentence))
    return narr_count, interrog_count, imper_count


def average_sentence_length(sentences):
    words_count = sum(len(re.findall(r'\b\w+\b', sentence)) for sentence in sentences)
    return words_count / len(sentences)


def average_word_length(text):
    words = re.findall(r'\b\w+\b', text)
    return sum(len(word) for word in words) / len(words)


def count_smileys(text):
    smiley_count = len(re.findall(r'(?<=[;:])--+[\(\)\[\]]+', text))
    return smiley_count


def find_lowercase_punctuation_words(text):
    lowercase_punctuation_words = re.findall(r'\b[a-z][\w\s,;:\'"\(\)\[\]\{\}\-]*[,.!?;:\'"\(\)\[\]\{\}]\b', text)
    return lowercase_punctuation_words


def is_valid_mac_address(mac_address):
    return bool(re.match(r'^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})$', mac_address))


def count_consonant_starting_words(text):
    consonant_starting_words = re.findall(r'\b[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]\w*\b', text)
    return len(consonant_starting_words)


def find_repeated_letters_words(text):
    repeated_letters_words = re.findall(r'\b\w*(\w)\1\w*\b', text)
    return [(word, re.search(r'(\w)\1', word).start()) for word in repeated_letters_words]


def get_words_alphabetically(text):
    words = re.findall(r'\b\w+\b', text)
    return sorted(words)
