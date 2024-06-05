def get_task_number():
    while True:
        task_number = 0
        try:
            task_number = int(input('Enter task number(1-5, 6 to exit): '))
            if not 1 <= task_number <= 6:
                raise Exception
            return task_number
        except:
            print('Wrong input! Try again')
            continue


def get_float_number(msg='Enter floating number'):
    while True:
        number = 0
        try:
            number = float(input(f'{msg}: '))
            return number
        except:
            print('Wrong input! Try again')
            continue


def get_number_of_elements_in_sequence(msg='Enter number of elements in list'):
    while True:
        number = 0
        try:
            number = int(input(f'{msg}: '))
            if number <= 0:
                raise Exception
            return number
        except:
            print('Wrong input! Try again')
            continue
