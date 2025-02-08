class GameBoard:

    def __init__(self):
        self.columns_count = 7
        self.rows_count = 6
        self.board = self._build_board()
        self.columns_tracker = [0] * self.columns_count

    def print_game_table(self) -> None:
        """ Show game table """
        for index in range(self.rows_count):
            line = self.board[index]
            print("|".join(line))
        print(0, 1, 2, 3, 4, 5, 6)

    def is_move_allowed(self, move: int) -> bool:
        """
        Check if:
        1. Column number is allowed
        2. Column is not full
        """
        return 7 > move >= 0 and self.columns_tracker[move] < 6

    def make_move(self, player, move) -> None:
        """ Update game board by move """
        for index in reversed(range(0, self.rows_count)):
            if self.board[index][move] == " ":
                self.board[index][move] = player.symbol
                self.columns_tracker[move] += 1
                return

    def has_winner(self, player, last_column) -> bool:
        last_row = self.columns_tracker[last_column] - 1
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Right, Down, Diagonal (\), Anti-Diagonal (/)
        for dr, dc in directions:
            count = 1
            for sign in [-1, 1]:
                r, c = last_row, last_column
                while True:
                    r += sign * dr
                    c += sign * dc
                    if 0 <= r < self.rows_count and 0 <= c < self.columns_count and self.board[self.rows_count - 1 - r][c] == player.symbol:
                        count += 1
                    else:
                        break
                    if count >= 4:
                        return True
        return False

    def is_board_full(self) -> bool:
        return sum(self.columns_tracker) == self.columns_count * self.rows_count

    def _build_board(self):
        return [[" "] * self.columns_count for _ in range(self.rows_count)]
