import math
import random
import time


# Player interface to be implemented by different types of players
class Player:
    def __init__(self, letter: str):
        self.letter = letter

    def get_move(self, game):
        pass


# Human player expecting moves from the standard input
class HumanPlayer(Player):
    def __init__(self, letter: str):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        value = None

        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9): ')

            try:
                value = int(square)
                if value not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')

        return value


# Random computer player creating moved from available ones. Not intelligence at all
class RandomComputerPlayer(Player):
    def __init__(self, letter: str):
        super().__init__(letter)

    def get_move(self, game):
        return random.choice(game.available_moves())


# Intelligent player based on a Minimax algorithm
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']

        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        # Check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1)
                    if other_player == max_player
                    else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # maximising
        else:
            best = {'position': None, 'score': math.inf}  # minimising

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # keep exploring with the new move

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # optimal next move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best


class TicTacToe:
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i * 3: (i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True

        return False

    def winner(self, square, letter):
        row_ind = math.floor(square / 3)
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([s == letter for s in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True

            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True

        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + ' moves to square {}'.format(square))
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            letter = 'O' if letter == 'X' else 'X'  # switches player

        if print_game:
            time.sleep(.8)

    if print_game:
        print('It\'s a tie!')


if __name__ == '__main__':
    # Play a game showing it
    x_player = RandomComputerPlayer('X')
    o_player = SmartComputerPlayer('O')
    t = TicTacToe()
    result = play(t, x_player, o_player)

    # Check how good it the smart player (smart player should never lose. Ties are allowed)
    x_wins = 0
    o_wins = 0
    ties = 0

    for i in range(1000):
        x_player = RandomComputerPlayer('X')
        o_player = SmartComputerPlayer('O')
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=False)

        print(f'Game number {i} with result {result}')

        if result == 'X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            ties += 1

    print(f'After 1000 iterations, we see {x_wins} X wins, {o_wins} O wins, {ties} ties.')
