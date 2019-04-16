#Dependency: pip install PyPokerEngine
import pypokerengine

from pypokerengine.api.game import setup_config, start_poker
from fish_player import FishPlayer
from console_player import ConsolePlayer
from random_player import RandomPlayer

from smallstakes_player import SmallStakesPlayer


config = setup_config(max_round=100, initial_stack=1000, small_blind_amount=20)
config.register_player(name="f1", algorithm=SmallStakesPlayer())

#Uncomment to play against above AI through the console
config.register_player(name="ME", algorithm=ConsolePlayer())

game_result = start_poker(config, verbose=1)

print(game_result)