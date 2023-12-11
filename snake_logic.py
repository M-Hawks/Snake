from enum import Enum
from collections import namedtuple
import numpy as np
import random


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x , y')
GAME_SIZE = 10
BODY = 1
HEAD = 2
FOOD = 3


class SnakeGameLogic:
    def __init__(self):
        self.w = GAME_SIZE
        self.h = GAME_SIZE
        self.reset()

        # init display

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [self.head,
                      Point(self.head.x - 1, self.head.y),
                      Point(self.head.x - 2, self.head.y)]
        self.score = 0

        self.iteration = 0
        self.steps_left = 50

        self.grid = np.zeros((self.w, self.h))
        for point in self.snake[1:]:
            self.grid[point.y][point.x] = 1
        self.grid[self.head.y, self.head.x] = 2

        self.food = None
        self._place__food()


    def _place__food(self):
        #todo: make this more effecient
        x = random.randint(0, self.w - 1)
        y = random.randint(0, self.h - 1 )
        self.food = Point(x, y)

        if self.food not in self.snake:
            self.grid[self.food.y, self.food.x] = 3
        else:
            self._place__food()

    def play_step(self, action):
        self.iteration += 1
        self.steps_left -= 1
        # 2. Move
        movePoint = self._move(action)

        # 3. Check if game Loss
        reward = 0  # eat food: +10 , game over: -10 , win: 50, else: 0
        game_over = False
        if self.is_collision(movePoint) or self.steps_left <= 0:
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # make old head body and make new head head
        self.grid[self.head.y, self.head.x] = 1
        self.head = movePoint
        self.snake.insert(0, self.head)
        self.grid[self.head.y, self.head.x] = 2

        # Check for game win
        if len(self.snake) >= self.h * self.w:
            game_over = True
            reward = 100
            return reward, game_over, self.score

        # 4. Place new Food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.steps_left += 50
            self._place__food()
        else:
            # if self.direction == Direction.UP and self.head.y > self.food.y:
            #     reward = .1
            # elif self.direction == Direction.DOWN and self.head.y < self.food.y:
            #     reward = .1
            # elif self.direction == Direction.RIGHT and self.head.x < self.food.x:
            #     reward = .1
            # elif self.direction == Direction.LEFT and self.head.x > self.food.x:
            #     reward = .1
            # else:
            #     reward = -.1

            tail = self.snake.pop()
            self.grid[tail.y][tail.x] = 0

        return reward, game_over, self.score

    def _move(self, action):
        # Action
        # [1,0,0] -> Straight
        # [0,1,0] -> Right Turn
        # [0,0,1] -> Left Turn

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right Turn
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # Left Turn
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if (self.direction == Direction.RIGHT):
            x += 1
        elif (self.direction == Direction.LEFT):
            x -= 1
        elif (self.direction == Direction.DOWN):
            y += 1
        elif (self.direction == Direction.UP):
            y -= 1
        return Point(x, y)

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hit boundary
        if pt.x >= self.w or pt.x < 0 or pt.y >= self.h or pt.y < 0:
            return True
        if self.grid[pt.y][pt.x] == BODY:
            return True
        return False


