from math import log

import checkers


def log_fun(x_val, eps_val):
    result = 0.
    accuracy = eps_val + 1
    iterations_count = 1

    while accuracy >= eps_val and iterations_count <= 500:
        result += -1 * x_val ** iterations_count / iterations_count
        accuracy = abs(log(x_val) - result)
        iterations_count += 1

    return result, iterations_count


def task1():
    x = 0
    while True:
        try:
            x = checkers.get_float_number(msg='Enter x, |x| < 1')
            if x >= 1 or x <= -1:
                raise Exception
            break
        except:
            print('Incorrect input, try again! Input only one number between 1 and 5, or -1 to exit\n')
            continue

    eps = checkers.get_float_number(msg='Enter eps')

    res, n = log_fun(x, eps)
    print(f'x = {x}\n'
          f'n = {n}\n'
          f'F(x) = {res}\n'
          f'Math F(x) = {log(1 - x)}\n'
          f'eps = {eps}')
