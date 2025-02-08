from dataclasses import dataclass

from enums import GameStatus
from game_board import GameBoard
from player import Player


@dataclass
class GameResult:
    status: GameStatus
    player: Player = None


class Game:

    def __init__(self,
                 player_1: Player,
                 player_2: Player,
                 game_board: GameBoard,
                 show_game_board: bool = True,
                 first_move: int = None):

        self.player_1 = player_1
        self.player_2 = player_2
        self.game_board = game_board
        self.current_player = player_1
        self.show_game_board = show_game_board
        self.first_move = first_move

    def play(self):
        while True:
            if self.show_game_board:
                self.game_board.print_game_table()

            move = self._get_move()

            self.game_board.make_move(self.current_player, move)

            game_status = self.game_status(move)
            if game_status:
                if self.show_game_board:
                    self.game_board.print_game_table()
                return game_status

            self.switch_player()

    def switch_player(self):
        """
        Switch the player
        """
        if self.current_player.id == self.player_1.id:
            self.current_player = self.player_2
        else:
            self.current_player = self.player_1

    def game_status(self, last_move):
        if self.game_board.has_winner(self.current_player, last_move):
            return GameResult(status=GameStatus.WIN, player=self.current_player)
        elif self.game_board.is_board_full():
            return GameResult(status=GameStatus.DRAW)

        return None

    def _get_move(self) -> int:
        if self.first_move is not None:
            move = self.first_move
            self.first_move = None
        else:
            move = self.current_player.get_move(self.game_board)

        return move

    def _is_game_over(self, last_move: int):
        # Player won
        if self.game_board.has_winner(self.current_player, last_move):
            print("WINNER: " + str(self.current_player))
            self.game_board.print_game_table()
            return True
        # Board full - draw
        elif self.game_board.is_board_full():
            print("DRAW!")
            self.game_board.print_game_table()
            return True

        return False
