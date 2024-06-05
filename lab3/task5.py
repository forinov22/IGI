import checkers
import sequence_generator


def debug_decorator(func):
    def wrapper(*args, **kwargs):
        print("Function call: ", func.__name__)
        print("Arguments: ", args, kwargs)
        result = func(*args, **kwargs)
        print("Result: ", result)
        return result
    return wrapper


def task5():
    n = checkers.get_number_of_elements_in_sequence()
    seq = []
    opt = input('Do you want to generate list by yourself?(y, otherwise - no): ')

    if opt.lower() == 'y':
        seq = sequence_generator.user_sequence_generator(n)
    else:
        seq = [i for i in sequence_generator.random_sequence_generator(n)]

    max_element = seq[0]
    max_index = 0

    for index, element in enumerate(seq):
        if abs(element) > abs(max_element):
            max_element = element
            max_index = index

    # print(max_element, max_index)

    sum_positive = 0
    mult_negative = 1
    positive_flag = False
    negative_flag = False

    for i in range(max_index):
        if seq[i] > 0:
            sum_positive += seq[i]
            positive_flag = True

        if seq[i] < 0:
            mult_negative *= seq[i]
            negative_flag = True

    @debug_decorator
    def print_list(array):
        for item in array:
            yield item

    print('Source list:')
    for i in print_list(seq):
        print(i)

    if not positive_flag:
        print(f'There is not positive elements')
    else:
        print(f"Sum of positive numbers before max element: {sum_positive}\n")

    if not negative_flag:
        print(f"There is not negative elements")
    else:
        print(f"Multiply of negative numbers before max element: {mult_negative}")
