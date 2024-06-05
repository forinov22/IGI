import checkers
import sequence_generator


def count_numbers_between_range(sequence):
    result = 0

    for element in sequence:
        if 5 <= element <= 25:
            result += 1

    return result


def task2():
    n = checkers.get_number_of_elements_in_sequence()
    seq = []
    opt = input('Do you want to generate list by yourself?(y, otherwise - no): ')

    if opt.lower() == 'y':
        seq = sequence_generator.user_sequence_generator(n)
    else:
        seq = [i for i in sequence_generator.random_sequence_generator(n)]

    res = count_numbers_between_range(seq)

    if opt.lower() != 'y':
        print(seq)

    print(f'Result = {res}')
