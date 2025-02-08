import uuid
import random

from game_board import GameBoard


class Player:

    def __init__(self, name: str, symbol: str):
        self.id = uuid.uuid4()
        self.name = name
        self.symbol = symbol

    def get_move(self, game_board: GameBoard):
        """To be implemented by subclasses."""
        raise NotImplementedError


class HumanPlayer(Player):

    def get_move(self, game_board: GameBoard):
        while True:
            info = f"{self.name} move: "
            move_str = input(info)
            try:
                move = int(str(move_str))
                if game_board.is_move_allowed(move):
                    return move
            except ValueError:
                return None


class MonteCarloSimulatorPlayer(Player):

    def __init__(self, name, symbol, iteration_count: int = 10000):
        super().__init__(name, symbol)
        self.iteration_count = iteration_count

    def get_move(self, game_board: GameBoard):
        from monte_carlo_simulator import MonteCarloSimulator
        monte_carlo_simulator = MonteCarloSimulator(self, game_board, self.iteration_count)
        return monte_carlo_simulator.run()


class RandomMovePlayer(Player):

    def get_move(self, game_board: GameBoard):
        move = random.randint(0, 6)

        # If random move (column) is already full then find another allowed move
        while not game_board.is_move_allowed(move):
            move = random.randint(0, 6)

        return move
