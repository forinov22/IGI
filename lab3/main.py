import task1
import task2
import task3
import task4
import task5
import checkers

# Lab3. Standard data types, collections, functions, modules.
# Performed by a student of group 253505, Forinov Egor.
# Fulfillment date: 20.03.2024
# Variant: 24


def main():
    while True:
        choice = checkers.get_task_number()

        if choice == 6:
            return
        if choice == 1:
            task1.task1()
        if choice == 2:
            task2.task2()
        if choice == 3:
            task3.task3()
        if choice == 4:
            task4.task4()
        if choice == 5:
            task5.task5()


if __name__ == '__main__':
    main()
