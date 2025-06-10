#冉路遥_2023141461068
import time

def is_valid(res, row, col, n) -> bool:
    '''
    this is a function for checking the position of a new queen
    :param res: currently result
    :param row: the tested row
    :param col: the tested column
    :param n: total number of queens
    :return: check if the tested position is valid or not
    '''
    #Check all rows in result
    for i in range(row):
        #check if the tested column is in the same row or diagonal with the tested row
        if res[i] == col or abs(res[i] - col) == abs(i-row):
            return False

    return True

def backtrack(res, row, n, solutions):
    '''
    this is a function for getting the result of the N-Queens problem
    :param res: currently result
    :param row: the tested row
    :param n: total number of queens
    :param solutions: solutions list
    :return: all of solutions
    '''
    if row == n:
        solutions.append(res[:])
        return

    for i in range(n):
        if is_valid(res, row, i, n):
            res[row] = i
            backtrack(res, row+1, n, solutions)
            res[row] = 0

def print_board(solutions, n, choice):
    '''
    this is a function for printing the board
    0-all solutions
    1-one solution
    :param solutions: list of solutions
    :param n: number of queens
    :param choice: user choice
    :return: None
    '''
    print(f"The number of solutions is: {len(solutions)}")
    match choice :
        case 0:
            for solution in solutions:
                print("----------")
                for col in solution:
                    row = ['Q' if i == col else '*' for i in range(n)]
                    print(" ".join(row))

        case -1:
            print("----------")

        case _:
            for i in range(choice):
                print("----------")
                for col in solutions[i]:
                    row = ['Q' if i == col else '*' for i in range(n)]
                    print(" ".join(row))


if __name__ == '__main__':

    # 判断N数量
    n = int(input("Please Enter the number of queens: "))
    while n < 4:
        print("Please Enter the number of queens greater than or equal to 4: ")
        n = int(input("Please Enter the number of queens: "))

    choice = int(input("Please Enter the choice: \n (0:all solutions; \n else:n solutions)"))
    start = time.time()
    solutions = []
    backtrack([0]*n, 0, n, solutions)
    end = time.time()
    print_board(solutions, n, choice)
    print(f"Time used: {end - start} seconds")
