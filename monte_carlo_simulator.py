import copy
import statistics

from game import Game
from enums import GameStatus
from game_board import GameBoard
from player import Player, RandomMovePlayer


class MonteCarloSimulator:

    def __init__(self, player: Player, current_game_board: GameBoard, n: int = 10000):
        self.player = player
        self.simulator_board = copy.deepcopy(current_game_board)
        self.n = n
        self.win_counts = dict((move, 0) for move in range(current_game_board.columns_count))

    def run(self):
        """ Monte Carlo method"""
        for move in range(self.simulator_board.columns_count):
            if not self.simulator_board.is_move_allowed(move):
                self.win_counts[move] = 0
                continue
            for i in range(self.n):
                self._simulator(move)

        return self._get_best_move()

    def _simulator(self, move) -> None:
        """ Play randomly until the end """
        current_board = copy.deepcopy(self.simulator_board)
        game: Game = self._create_game_for_simulator(current_board, move)
        game_result = game.play()

        if game_result.status == GameStatus.WIN and game_result.player.id == self.player.id:
            self.win_counts[move] += 1
        elif game_result == GameStatus.DRAW:
            self.win_counts[move] += 0.5

    def _get_best_move(self) -> int:
        score = 0
        best_move = 0
        for move in self.win_counts.keys():
            self._print_move_with_winning_probability(move)
            # Has better winning probability
            current_score = self.win_counts[move]
            if current_score > score or (
                    current_score == score and self._is_new_value_closer_to_median(move, best_move)):
                best_move = move
                score = current_score

        return best_move

    def _create_game_for_simulator(self, current_board: GameBoard, move: int) -> Game:
        player_1 = RandomMovePlayer(name=self.player.name, symbol=self.player.symbol)
        player_1.id = self.player.id

        other_player_symbol = "O" if self.player.symbol == "X" else "X"
        player_2 = RandomMovePlayer(name="random_player", symbol=other_player_symbol)

        simulator_game = Game(
            player_1=player_1,
            player_2=player_2,
            game_board=current_board,
            show_game_board=False,
            first_move=move
        )

        return simulator_game

    def _is_new_value_closer_to_median(self, new_value, old_value):
        """ Find is new element is closer to the median (means closer to the middle of the game board) """
        median = statistics.median(self.win_counts.keys())
        return abs(new_value - median) < abs(old_value - median)

    def _print_move_with_winning_probability(self, move):
        """ Find winning probability """
        winning_probability = round(self.win_counts[move] / self.n * 100, 2)
        print(f"Move {str(move)} {str(winning_probability)}%")
