
default = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]

def main():
    print('Welcome to Danial\'s 8 puzzle solver!')

    # Getting user input for if they want to use default or their own
    inputsel = input('Please type “1” to use a default puzzle, or “2” to enter your own puzzle!'
                     ' Please be sure to press ENTER after making your choice!\n')
    inputnum = int(inputsel)

    # Setting up puzzle if user uses a custom puzzle
    if inputnum == 2:
        print('Enter your puzzle, use a zero to represent the blank \n')

        # Getting the first row
        row1 = input('Enter the first row, use spaces between numbers: ')
        row1 = row1.split(' ')

        # Getting the second row
        row2 = input('Enter the second row, use spaces between numbers: ')
        row2 = row2.split(' ')

        # Getting the third row
        row3 = input('Enter the third row, use spaces between numbers: ')
        row3 = row3.split(' ')

        print(row1, row2, row3)


if __name__ == "__main__":
    main()

