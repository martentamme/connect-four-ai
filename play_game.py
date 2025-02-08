from enums import GameStatus
from game import Game
from game_board import GameBoard
from player import HumanPlayer, MonteCarloSimulatorPlayer

if __name__ == '__main__':
    game_board = GameBoard()
    player_1 = HumanPlayer("Player 1", "X")
    player_2 = MonteCarloSimulatorPlayer("Player 2", "O", iteration_count=20_000)

    game = Game(player_1, player_2, game_board)
    result = game.play()

    status = result.status
    print(status)
    if status == GameStatus.WIN:
        print(result.player.name)
