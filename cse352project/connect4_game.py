import numpy as np
import sys

# random used for now will remove later
import random

# global variable to denote the number of row and col in game board
TOTAL_ROW_COUNT: int = 6
TOTAL_COL_COUNT: int = 7

"""
board is simulated by 2d array where the 0 index row value is the bottom most value and the 
last position in rows is the uppermost value
"""


# function to initialize the game board
# returns the newly made game board
def make_board():
    # using numpy fill a 6x7 with zeros as a board
    board = np.zeros((TOTAL_ROW_COUNT, TOTAL_COL_COUNT))
    # return created board
    return board


# function to check if given column position is a valid move
# parameter board = board state; column = given column value
# returns boolean value true if there exist a valid move and false if not
def is_valid(board, column):
    # checks top most position of the given column
    if board[TOTAL_ROW_COUNT-1][column] == 0:
        return True
    else:
        return False


# function to find the row at next valid move (asume is_valid runs before this function)
# parameter board = board state; column = given column value
# returns row index that is next valid move
def next_row_value(board, column):
    for i in range(TOTAL_ROW_COUNT):
        if board[i][column] == 0:
            return i


# place piece on game board
def place_piece(board, piece, row, col):
    board[row][col] = piece


# function to print the given board state
# parameter board = board to be printed
# prints the given state of board
def print_board(board):
    # board usage was backwards so i flipped the display so it looks right
    print(np.flip(board, 0))


# returns positive value for favor of player 1 negative for player 2 and 0 for neutral
def board_score(board):
    total_score = 0
    for col in range(TOTAL_COL_COUNT-3):
        for row in range(TOTAL_ROW_COUNT):
            value_count = [0, 0, 0]
            if row >= 3:
                value_count[int(board[row][col])] += 1
                value_count[int(board[row-1][col+1])] += 1
                value_count[int(board[row-2][col+2])] += 1
                value_count[int(board[row-3][col+3])] += 1

                if value_count[1] == 0 or value_count[2] == 0:
                    if value_count[1] != 0:
                        total_score += value_count[1]
                    if value_count[2] != 0:
                        total_score -= value_count[2]

            value_count = [0, 0, 0]
            if row < TOTAL_ROW_COUNT-3:
                value_count[int(board[row][col])] += 1
                value_count[int(board[row + 1][col + 1])] += 1
                value_count[int(board[row + 2][col + 2])] += 1
                value_count[int(board[row + 3][col + 3])] += 1

                if value_count[1] == 0 or value_count[2] == 0:
                    if value_count[1] != 0:
                        total_score += value_count[1]
                    if value_count[2] != 0:
                        total_score -= value_count[2]

    # check vertical and horizontal
    for row in range(TOTAL_ROW_COUNT-3):
        for col in range(TOTAL_COL_COUNT):
            value_count = [0, 0, 0]
            value_count[int(board[row][col])] += 1
            value_count[int(board[row + 1][col])] += 1
            value_count[int(board[row + 2][col])] += 1
            value_count[int(board[row + 3][col])] += 1

            if value_count[1] == 0 or value_count[2] == 0:
                if value_count[1] != 0:
                    total_score += value_count[1]
                if value_count[2] != 0:
                    total_score -= value_count[2]

    for row in range(TOTAL_ROW_COUNT):
        for col in range(TOTAL_COL_COUNT-3):
            value_count = [0, 0, 0]
            value_count[int(board[row][col])] += 1
            value_count[int(board[row][col + 1])] += 1
            value_count[int(board[row][col + 2])] += 1
            value_count[int(board[row][col + 3])] += 1

            if value_count[1] == 0 or value_count[2] == 0:
                if value_count[1] != 0:
                    total_score += value_count[1]
                if value_count[2] != 0:
                    total_score -= value_count[2]
    return total_score


# function to check if there is a win
# parameter board = board state; color = color of most recent piece dropped
# returns true if win and false if else
def win_check(board, color):
    # check diagonal
    for col in range(TOTAL_COL_COUNT-3):
        for row in range(TOTAL_ROW_COUNT):
            if row >= 3:
                if board[row][col] == color and board[row-1][col+1] == color and board[row-2][col+2] == color and board[row-3][col+3] == color:
                    return True
            if row < TOTAL_ROW_COUNT-3:
                if board[row][col] == color and board[row+1][col+1] == color and board[row+2][col+2] == color and board[row+3][col+3] == color:
                    return True
    # check vertical and horizontal
    for row in range(TOTAL_ROW_COUNT-3):
        for col in range(TOTAL_COL_COUNT):
            if board[row][col] == color and board[row+1][col] == color and board[row+2][col] == color and board[row+3][col] == color:
                return True
    for row in range(TOTAL_ROW_COUNT):
        for col in range(TOTAL_COL_COUNT-3):
            if board[row][col] == color and board[row][col+1] == color and board[row][col+2] == color and board[row][col+3] == color:
                return True
    # if code reaches here no win condition was found return 0 for neutral
    return False


# currently using random int
""" replace later for ai decisions """
def player2_move(board):
    value = int(random.randint(0, 6))
    while not is_valid(board, value):
        value = int(random.randint(0, 6))
    return value


if __name__ == "__main__":
    # used to check running status of the current game
    game_running = True

    # initialize the game board
    game_board = make_board()

    while game_running:
        print_board(game_board)
        user_input = int(input("position to place piece (0-6):"))
        # waits for valid input from user
        while not is_valid(game_board, user_input):
            print("invalid position please select another.")
            user_input = int(input("position to place piece (0-6):"))
        r_value = next_row_value(game_board, user_input)
        place_piece(game_board, 1, r_value, user_input)
        #places the piece and checks to see if there is a winner
        print_board(game_board)
        print("board score: " + str(board_score(game_board)))
        if win_check(game_board, 1):
            print("player 1 wins")
            game_running = False
            break
        # gets random comp value and place piece and checks if there is winner
        comp_input = player2_move(game_board)
        r_value = next_row_value(game_board, comp_input)
        place_piece(game_board, 2, r_value, comp_input)
        print_board(game_board)
        print("board score: " + str(board_score(game_board)))
        if win_check(game_board, 2):
            print("player 2/computer wins")
            game_running = False
            break
