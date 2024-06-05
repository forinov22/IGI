def count_spaces_and_apostrophe(s):
    spaces = 0
    apostrophes = 0

    for element in s:
        if element == ' ':
            spaces += 1

        elif element == '\'':
            apostrophes += 1

    return spaces, apostrophes


def task3():
    s = input('Enter string where you want to find spaces and apostrophes\n')

    spaces, apostrophes = count_spaces_and_apostrophe(s)
    print(f'Spaces = {spaces}\n'
          f'Apostrophes = {apostrophes}')
