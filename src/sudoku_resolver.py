def find_next_empty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == -1:
                return i, j

    return None, None


def is_valid(puzzle, guess, row, column):
    row_values = puzzle[row]
    if guess in row_values:
        return False

    column_values = [puzzle[i][column] for i in range(9)]
    if guess in column_values:
        return False

    row_start = (row // 3) * 3
    column_start = (column // 3) * 3

    for i in range(row_start, row_start + 3):
        for j in range(column_start, column_start + 3):
            if puzzle[i][j] == guess:
                return False

    return True


def solve_sudoku(puzzle):
    row, column = find_next_empty(puzzle)

    if row is None:
        return True

    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, column):
            puzzle[row][column] = guess

            if solve_sudoku(puzzle):
                return True

        puzzle[row][column] = -1

    return False


if __name__ == '__main__':
    example_board = [
        [-1, 8, -1, -1, -1, -1, -1, 4, 1],
        [-1, 4, 9, -1, -1, -1, 6, 2, -1],
        [-1, -1, 3, -1, 6, 4, 8, -1, 9],

        [3, -1, -1, -1, 4, -1, -1, 1, 7],
        [6, -1, -1, 2, -1, 8, -1, -1, 4],
        [7, 2, -1, -1, 9, -1, -1, -1, 6],

        [4, -1, 5, 7, 2, -1, 3, -1, -1],
        [-1, 3, 7, -1, -1, -1, 4, 6, -1],
        [9, 6, -1, -1, -1, -1, -1, 7, -1]
    ]

    solved = solve_sudoku(example_board)

    if solved:
        for i in range(9):
            print(example_board[i])
