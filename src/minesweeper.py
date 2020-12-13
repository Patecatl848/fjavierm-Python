"""
Basic implementation of a command-line minesweeper
"""
import random
import re
import sys

DEFAULT_BOARD_DIMENSION = 10
DEFAULT_BOMBS = 10


class Board:

    def __init__(self, dimension: int, bombs: int):
        self.dimension = DEFAULT_BOARD_DIMENSION if dimension < 0 else dimension
        self.bombs = DEFAULT_BOMBS if bombs < 0 else dimension ** 2 if dimension ** 2 < bombs else bombs
        self.board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        self.revealed = set()

        self.set_bombs()
        self.set_values()

    def set_bombs(self):
        bombs_planted = 0

        while bombs_planted < self.bombs:
            row = random.randint(0, self.dimension - 1)
            column = random.randint(0, self.dimension - 1)

            if self.board[row][column] == '*':
                continue

            self.board[row][column] = '*'
            bombs_planted += 1

    def set_values(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i][j] == '*':
                    continue

                self.board[i][j] = self.count_neighbour_mines(i, j)

    def count_neighbour_mines(self, row: int, column: int) -> int:
        neighbour_bombs = 0

        for i in range(max(0, row - 1), min(self.dimension - 1, row + 1) + 1):
            for j in range(max(0, column - 1), min(self.dimension - 1, column + 1) + 1):
                if i == row and j == column:
                    continue

                if self.board[i][j] == '*':
                    neighbour_bombs += 1

        return neighbour_bombs

    def reveal(self, row: int, column: int) -> bool:
        self.revealed.add((row, column))

        if self.board[row][column] == '*':
            return False
        elif int(self.board[row][column]) > 0:
            return True

        for i in range(max(0, row - 1), min(self.dimension - 1, row + 1) + 1):
            for j in range(max(0, column - 1), min(self.dimension - 1, column + 1) + 1):
                if (i, j) in self.revealed:
                    continue
                self.reveal(i, j)

        return True

    def __str__(self) -> str:
        vertical_guide_length = len(str(self.dimension))
        header = (' ' * (vertical_guide_length + 1)) + ''.join(['| ' + str(i) + ' ' for i in range(self.dimension)]) + '|\n'
        horizontal_separator_line = ('-' * (len(header) - 1)) + '\n'

        rows = ''
        for i in range(self.dimension):
            rows += str(i).rjust(vertical_guide_length, ' ')
            for j in range(self.dimension):
                rows += ' | ' + (str(self.board[i][j]) if (i, j) in self.revealed else ' ')
            rows += ' |\n'

        return header + horizontal_separator_line + rows


def play(dimension: int = DEFAULT_BOARD_DIMENSION, bombs: int = DEFAULT_BOMBS):
    board = Board(dimension, bombs)
    is_victory = True

    while len(board.revealed) < board.dimension ** 2 - bombs:
        print(board)

        user_input = re.split(',(\\s)*', input("Reveal a box (row, column): "))
        row, column = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.dimension or column < 0 or column >= dimension:
            print("Invalid location. Try again.")
            continue

        is_victory = board.reveal(row, column)
        if not is_victory:
            break

    if is_victory:
        print("You win!")
    else:
        print("Game over!")
        board.dug = [(i, j) for i in range(board.dimension) for j in range(board.dimension)]
        print(board)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        play(int(sys.argv[1]), int(sys.argv[2]))
    else:
        play()
