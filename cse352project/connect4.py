import time
import numpy as np

TOTAL_ROW_COUNT: int = 6
TOTAL_COL_COUNT: int = 7

ai = 2
player = 1


class Game:

    def __init__(self):
        self.board = np.zeros((TOTAL_ROW_COUNT, TOTAL_COL_COUNT))
        self.keys = []

    def print_board(self):
        # board usage was backwards so i flipped the display so it looks right
        print(np.flip(self.board, 0))

    def is_valid(self, column):
        # checks top most position of the given column
        if self.board[TOTAL_ROW_COUNT - 1][column] == 0:
            return True
        else:
            return False

    # function to check if there is a win
    # parameter board = board state; color = color of most recent piece dropped
    # returns true if win and false if else
    def win_check(self, color):
        # check diagonal
        for col in range(TOTAL_COL_COUNT - 3):
            for row in range(TOTAL_ROW_COUNT):
                if row >= 3:
                    if self.board[row][col] == color and self.board[row - 1][col + 1] == color and self.board[row - 2][col + 2] == color and self.board[row - 3][col + 3] == color:
                        return True
                if row < TOTAL_ROW_COUNT - 3:
                    if self.board[row][col] == color and self.board[row + 1][col + 1] == color and self.board[row + 2][col + 2] == color and self.board[row + 3][col + 3] == color:
                        return True
        # check vertical and horizontal
        for row in range(TOTAL_ROW_COUNT - 3):
            for col in range(TOTAL_COL_COUNT):
                if self.board[row][col] == color and self.board[row + 1][col] == color and self.board[row + 2][col] == color and \
                        self.board[row + 3][col] == color:
                    return True
        for row in range(TOTAL_ROW_COUNT):
            for col in range(TOTAL_COL_COUNT - 3):
                if self.board[row][col] == color and self.board[row][col + 1] == color and self.board[row][col + 2] == color and \
                        self.board[row][col + 3] == color:
                    return True
        # if code reaches here no win condition was found return 0 for neutral
        return False

    # returns positive value for favor of player 2 negative for player 1 and 0 for neutral
    def board_score(self):
        total_score = 0
        for col in range(TOTAL_COL_COUNT - 3):
            for row in range(TOTAL_ROW_COUNT):
                value_count = [0, 0, 0]
                if row >= 3:
                    value_count[int(self.board[row][col])] += 1
                    value_count[int(self.board[row - 1][col + 1])] += 1
                    value_count[int(self.board[row - 2][col + 2])] += 1
                    value_count[int(self.board[row - 3][col + 3])] += 1

                    if value_count[1] == 0 or value_count[2] == 0:
                        if value_count[1] != 0:
                            total_score -= value_count[1]
                        if value_count[2] != 0:
                            total_score += value_count[2]

                value_count = [0, 0, 0]
                if row < TOTAL_ROW_COUNT - 3:
                    value_count[int(self.board[row][col])] += 1
                    value_count[int(self.board[row + 1][col + 1])] += 1
                    value_count[int(self.board[row + 2][col + 2])] += 1
                    value_count[int(self.board[row + 3][col + 3])] += 1

                    if value_count[1] == 0 or value_count[2] == 0:
                        if value_count[1] != 0:
                            total_score -= value_count[1]
                        if value_count[2] != 0:
                            total_score += value_count[2]

        # check vertical and horizontal
        for row in range(TOTAL_ROW_COUNT - 3):
            for col in range(TOTAL_COL_COUNT):
                value_count = [0, 0, 0]
                value_count[int(self.board[row][col])] += 1
                value_count[int(self.board[row + 1][col])] += 1
                value_count[int(self.board[row + 2][col])] += 1
                value_count[int(self.board[row + 3][col])] += 1

                if value_count[1] == 0 or value_count[2] == 0:
                    if value_count[1] != 0:
                        total_score -= value_count[1]
                    if value_count[2] != 0:
                        total_score += value_count[2]

        for row in range(TOTAL_ROW_COUNT):
            for col in range(TOTAL_COL_COUNT - 3):
                value_count = [0, 0, 0]
                value_count[int(self.board[row][col])] += 1
                value_count[int(self.board[row][col + 1])] += 1
                value_count[int(self.board[row][col + 2])] += 1
                value_count[int(self.board[row][col + 3])] += 1

                if value_count[1] == 0 or value_count[2] == 0:
                    if value_count[1] != 0:
                        total_score -= value_count[1]
                    if value_count[2] != 0:
                        total_score += value_count[2]
        return total_score

    def board_full(self):
        count = 0
        for i in range(TOTAL_COL_COUNT):
            if self.is_valid(i):
                count += 1
        if count == 0:
            return True
        else:
            return False

    def next_row_value(self, column):
        for i in range(TOTAL_ROW_COUNT):
            if self.board[i][column] == 0:
                return i

    def remove(self, row, column):
        self.board[row][column] = 0

    # place piece on game board
    def place_piece(self, piece, row, col):
        self.board[row][col] = piece

    def update_keys(self):
        key_list = []
        for i in range(TOTAL_COL_COUNT):
            if self.is_valid(i):
                key_list.append(i)
        return key_list

    def ai_turn(self):
        best_score = -1000
        bestmove = 0

        for moves in self.update_keys():
            rowv = self.next_row_value(moves)
            self.place_piece(ai, rowv, moves)
            score = self.minimax(0, False)
            self.remove(rowv, moves)
            if score > best_score:
                best_score = score
                bestmove = moves

        bestrow = self.next_row_value(bestmove)
        self.place_piece(ai, bestrow, bestmove)
        return

    def playerturn(self):
        pos = int(input("enter position 0-6: "))
        while not self.is_valid(pos):
            pos = int(input("enter position 0-6: "))
        else:
            rowv = self.next_row_value(pos)
            self.place_piece(player, rowv, pos)
        return

    def minimax(self, depth, ismaximizing):
        if self.win_check(ai):
            return 1000
        elif self.win_check(player):
            return -1000
        elif self.board_full():
            return 0

        if ismaximizing:
            bestscore = -1000
            if depth == 5:
                for key in self.update_keys():
                    rowv = self.next_row_value(key)
                    self.place_piece(ai, rowv, key)
                    score = self.board_score()
                    self.remove(rowv, key)
                    if score > bestscore:
                        bestscore = score
                return bestscore

            for key in self.update_keys():
                rowv = self.next_row_value(key)
                self.place_piece(ai, rowv, key)
                score = self.minimax(depth + 1, False)
                self.remove(rowv, key)
                if score > bestscore:
                    bestscore = score

            return bestscore
        else:
            bestscore = 1000
            if depth == 5:
                for key in self.update_keys():
                    rowv = self.next_row_value(key)
                    self.place_piece(ai, rowv, key)
                    score = self.board_score()
                    self.remove(rowv, key)
                    if score < bestscore:
                        bestscore = score
                return bestscore

            for key in self.update_keys():
                rowv = self.next_row_value(key)
                self.place_piece(player, rowv, key)
                score = self.minimax(depth + 1, True)
                self.remove(rowv, key)
                if score > bestscore:
                    bestscore = score

            return bestscore


if __name__ == "__main__":
    game = Game()
    while not game.board_full() or not game.win_check(player) or not game.win_check(ai):
        game.print_board()
        game.playerturn()
        if game.win_check(player):
            print("player has won")
            break
        game.ai_turn()
        if game.win_check(ai):
            print("ai has won")
            break
