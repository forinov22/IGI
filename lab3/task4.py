def find_long_words(words_arr):
    result = []

    for element in words_arr:
        if len(element) < 6:
            result.append(element)

    return result


def find_shortest_endswith_w(words_arr, suffix):
    words_endswith_w = []

    for element in words_arr:
        if element.endswith(suffix):
            words_endswith_w.append(element)

    words_endswith_w.sort()

    if len(words_endswith_w) <= 0:
        return -1

    return words_endswith_w[0]


def task4():
    s = ('So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and '
         'stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the'
         'daisies, when suddenly a White Rabbit with pink eyes ran close by her.')

    s.replace(',', ' ')

    words = s.split(' ')

    long_words = find_long_words(words)

    suffix = 'w'
    shortest_word_endswith_w = find_shortest_endswith_w(words, suffix)

    print(f"Count of words, shorter than 6 symbols: {len(long_words)}")

    if shortest_word_endswith_w == -1:
        print(f"No words that end with \'{suffix}\'")
    else:
        print(f"Shortest word that ends with \'w\': {shortest_word_endswith_w}")

    print('Words sorted by DESC')
    print(sorted(words, key=lambda elem: len(elem), reverse=True))
