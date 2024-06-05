import random
import checkers


def random_sequence_generator(count_of_elements):
    for i in range(count_of_elements):
        yield random.uniform(-100, 100)


def user_sequence_generator(count_of_elements):
    seq = []

    for i in range(count_of_elements):
        number = checkers.get_float_number('Enter number you want to add to list')
        seq.append(number)

    return seq
