class MiniMax():


    def __init__(self, game):
        self.player = 1
        self.ai = 2
        self.ZERO = 0
        self.TOTAL_ROW_COUNT = 6
        self.TOTAL_COL_COUNT = 7
        pass

    def is_terminal(self, board):
        return len(self.get_keys(board)) == 0 or win_check(board, self.ai) or win_check(board, self.player)

    def minimax(self, board, depth, alpha, beta, isMaximizing):
        valid_drops = self.get_keys(board)
        terminal = self.is_terminal(board)
        if depth == 0 or terminal:
            if terminal:
                if win_check(board, self.ai):
                    return (10000000000000, None)
                elif win_check(board, self.player):
                    return (-10000000000000, None)
                else:
                    return (0, None)
            else:
                return (self.scoring(board, ai), None)
        if isMaximizing:
            score = -math.inf
            column = random.choice(valid_drops)
            for col in valid_drops:
                row = next_row_value(board, col)
                copy = board.copy()
                place_piece(copy, self.ai, row, col)
                new_score = self.minimax(copy, depth - 1, alpha, beta, False)[0]
                if new_score > score:
                    score = new_score
                    column = col
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return (score, column)
        else:
            score = math.inf
            column = random.choice(valid_drops)
            for col in valid_drops:
                row = next_row_value(board, col)
                copy = board.copy()
                place_piece(copy, self.player, row, col)
                new_score = self.minimax(copy, depth - 1, alpha, beta, True)[0]
                if new_score < score:
                    score = new_score
                    column = col
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return (score, column)


    def score_4(self, cells, piece):
        score = 0
        opponent = self.player
        if piece == self.player:
            opponent = self.ai

        if cells.count(piece) == 4:
            score += 100
        elif cells.count(piece) == 3 and cells.count(self.ZERO) == 1:
            score += 5
        # looks for 2
        elif cells.count(piece) == 2 and cells.count(self.ZERO) == 2:
            score += 2

        if cells.count(opponent) == 3 and cells.count(self.ZERO) == 1:
            score -= 4
        # elif cells.count(opponent) == 2 and cells.count(ZERO) == 2:
        #     score -= 5
        return score

    def scoring(self, board, piece):
        score = 0
        center_array = [int(i) for i in list(board[:, self.TOTAL_COL_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        for col in range(self.TOTAL_COL_COUNT):
            array = [int(i) for i in list(board[:, col])]
            for row in range(self.TOTAL_ROW_COUNT - 3):
                cells = array[row: row + 4]
                score += self.score_4(cells, piece)

        for row in range(self.TOTAL_ROW_COUNT):
            array = [int(i) for i in list(board[row, :])]
            for col in range(self.TOTAL_COL_COUNT - 3):
                cells = array[col:col + 4]
                score += self.score_4(cells, piece)

        for row in range(self.TOTAL_ROW_COUNT - 3):
            for col in range(self.TOTAL_COL_COUNT - 3):
                cells = [board[row + i][col + i] for i in range(4)]
                score += self.score_4(cells, piece)

        for row in range(3, self.TOTAL_ROW_COUNT):
            for col in range(self.TOTAL_COL_COUNT - 3):
                cells = [board[row - i][col + i] for i in range(4)]
                score += self.score_4(cells, piece)
        return score

    def get_keys(self, board):
        key_list = []
        for i in range(self.TOTAL_COL_COUNT):
            if is_valid(board, i):
                key_list.append(i)
        return key_list