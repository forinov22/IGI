import zipfile
from individual_task import (count_sentences,
                             count_sentence_types,
                             average_sentence_length,
                             average_word_length, count_smileys,
                             count_consonant_starting_words,
                             find_lowercase_punctuation_words,
                             find_repeated_letters_words,
                             is_valid_mac_address,
                             get_words_alphabetically)


if __name__ == "__main__":
    with open('input.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    # Count sentences
    num_sentences, sentences = count_sentences(text)

    # Count sentence types
    narr_count, interrog_count, imper_count = count_sentence_types(sentences)

    # Calculate average sentence length
    avg_sentence_len = average_sentence_length(sentences)

    # Calculate average word length
    avg_word_len = average_word_length(text)

    # Count smileys
    smiley_count = count_smileys(text)

    # Find lowercase words with punctuation
    lowercase_punctuation_words = find_lowercase_punctuation_words(text)

    # Check MAC address validity
    mac_address = "aE:dC:cA:56:76:54"
    is_valid_mac = is_valid_mac_address(mac_address)

    # Count consonant starting words
    consonant_starting_word_count = count_consonant_starting_words(text)

    # Find words containing repeated letters and their positions
    repeated_letters_words = find_repeated_letters_words(text)

    # Get words in alphabetical order
    words_alphabetically = get_words_alphabetically(text)

    # Save results to file
    with open('results.txt', 'w', encoding='utf-8') as file:
        file.write(f"Number of sentences: {num_sentences}\n")
        file.write(f"Number of narrative sentences: {narr_count}\n")
        file.write(f"Number of interrogative sentences: {interrog_count}\n")
        file.write(f"Number of imperative sentences: {imper_count}\n")
        file.write(f"Average sentence length: {avg_sentence_len}\n")
        file.write(f"Average word length: {avg_word_len}\n")
        file.write(f"Number of smileys: {smiley_count}\n")
        file.write("\nLowercase words with punctuation:\n")
        file.write('\n'.join(lowercase_punctuation_words) + '\n')
        file.write(f"\nIs {mac_address} a valid MAC address: {is_valid_mac}\n")
        file.write(f"Number of consonant starting words: {consonant_starting_word_count}\n")
        file.write("\nWords containing repeated letters and their positions:\n")
        for word, position in repeated_letters_words:
            file.write(f"{word} (position: {position})\n")
        file.write("\nWords in alphabetical order:\n")
        file.write('\n'.join(words_alphabetically) + '\n')

    # Create a ZIP file with results
    with zipfile.ZipFile('results.zip', 'w') as zip_file:
        zip_file.write('results.txt')
