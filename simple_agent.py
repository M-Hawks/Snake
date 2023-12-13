
import random
import numpy as np
from collections import deque
from snake_logic import SnakeGameLogic, Direction, Point
from model import Linear_QNet, QTrainer
from Helper import plot
from snake_logic import SnakeGameLogic
from snake_ui import SnakeGameUI
from snake_logic import GAME_SIZE
FORWARD_MOVE = (1,0,0)
RIGHT_MOVE = (0,1,0)
LEFT_MOVE = (0,0,1)

class SimpleAgent:
    def __init__(self):
        pass

    def get_action(self, game):

        odd = game.w % 2 == 1
        
        if game.direction == Direction.RIGHT and game.is_oob(Point(game.head.x + 1, game.head.y)):
            return [LEFT_MOVE]
        
        elif game.direction == Direction.DOWN and game.is_oob(Point(game.head.x, game.head.y + 2)):
            if game.is_oob(Point(game.head.x -1, game.head.y)):
                return [FORWARD_MOVE, LEFT_MOVE]
            else:
                return [RIGHT_MOVE, RIGHT_MOVE]

        elif game.direction == Direction.UP and game.is_oob(Point(game.head.x, game.head.y - 1)):
                return[LEFT_MOVE, LEFT_MOVE]
            
        else:
            return [FORWARD_MOVE]
        

if __name__ == "__main__":
    game = SnakeGameLogic()
    agent = SimpleAgent()
    ui = SnakeGameUI(game)

    alive = True
    while alive:
        moves = agent.get_action(game)
        for m in moves:
            print(m)
            _, _, dead, _, _ = game.play_step(m)
            alive = not dead
            ui.update_ui(game)

