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
    def __init__(self, game_size=GAME_SIZE, direction=Direction.RIGHT, snake=None, food=None, score=0, moves_made=0, path=[]):
        self.w = game_size
        self.h = game_size
        
        self.direction = direction
        if snake == None:
            self.head = Point(self.w // 2, self.h // 2)
            self.snake = [self.head,
                        Point(self.head.x - 1, self.head.y),
                        Point(self.head.x - 2, self.head.y)]
        else:
            self.head = snake[0]
            self.snake = snake

        self.score = score
        self.moves_made = moves_made
        self.steps_left = ((score + 1) * 100) - moves_made

        self.grid = np.zeros((self.w, self.h))
        for point in self.snake[1:]:
            self.grid[point.y][point.x] = 1
        self.grid[self.head.y, self.head.x] = 2

        if food:
            self.food = food
        else:
            self._place__food()
        
        self.path = path
    def __lt__(self, other):
        return self.hueristic() < other.hueristic()

    def hueristic(self):
        visited = set()
        # point = self.head
        # s = 0
        # s += self.d_search(Point(point.x +1, point.y), visited)
        # s += self.d_search(Point(point.x -1, point.y), visited)
        # s += self.d_search(Point(point.x, point.y+1), visited)
        # s += self.d_search(Point(point.x, point.y-1), visited)
        # s = self.w * self.h - (s + len(self.snake))

        point = self.food
        s = self.d_search(Point(point.x, point.y-1), visited)
        s = self.w * self.h - (s + len(self.snake))

        s += self.bad_squares()
        return s, self.manhattan(self.head)
    
    def d_search(self, point, visited):
        s = 1
        if self.is_oob(point) or self.is_body_or_head(point):
            return 0
        if point in visited:
            return 0
        else:
            visited.add(point)
            s += self.d_search(Point(point.x +1, point.y), visited)
            s += self.d_search(Point(point.x -1, point.y), visited)
            s += self.d_search(Point(point.x, point.y+1), visited)
            s += self.d_search(Point(point.x, point.y-1), visited)
            return s
    
    def bad_squares(self):
        total = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                # Check if i'm an empty space
                point = Point(x, y)
                if self.is_oob(point) or self.is_body_or_head(point):
                    continue
                
                right = Point(x +1, y)
                left = Point(x -1, y)
                up = Point(x, y - 1)
                down = Point(x, y + 1)
                dirs = [right, left, up, down]

                bad_dirs = 0
                for dir in dirs:
                    # if self.is_oob(point) or self.is_body_or_head(point):
                    #     bad_dirs += 1

                    if not self.is_oob(point) and self.is_body_or_head(point):
                        bad_dirs += 1

                if bad_dirs >= 3:
                    total += 1

        return total

        



    def manhattan(self, point):
        manhattan = abs(self.head.x - self.food.x) + abs(self.head.y - self.food.y)
        tot = manhattan + self.moves_made
        return manhattan
    
    def is_body_or_head(self, point):
        if self.grid[point.y][point.x] == BODY or self.grid[point.y][point.x] == HEAD:
            return True
        return False
    
    
    def _place__food(self):
        #todo: make this more effecient

        potential_places = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == 0:
                    potential_places.append((x, y))

        x, y = random.choice(potential_places)
        self.food = Point(x, y)
        self.grid[self.food.y, self.food.x] = 3

        # random placement code
        # x = random.choice(0, self.w - 1)
        # y = random.randint(0, self.h - 1 )
        # self.food = Point(x, y)

        # if self.food not in self.snake:
        #     self.grid[self.food.y, self.food.x] = 3
        # else:
        #     self._place__food()

    def play_step(self, action):
        self.moves_made += 1
        self.steps_left -= 1
        # 2. Move
        movePoint = self._move(action)

        found_food = False
        won_game = False

        # 3. Check if game Loss
        reward = 0  # eat food: +10 , game over: -10 , win: 50, else: 0
        game_over = False
        if self.is_collision(movePoint) or self.steps_left <= 0:
            game_over = True
            reward = -10
            return reward, self.score, game_over, found_food, won_game

        # make old head body and make new head head
        self.grid[self.head.y, self.head.x] = 1
        self.head = movePoint
        self.snake.insert(0, self.head)
        self.grid[self.head.y, self.head.x] = 2

        # Check for game win
        if len(self.snake) >= self.h * self.w:
            game_over = True
            won_game = True
            reward = 100
            return reward, self.score, game_over, found_food, won_game

        # 4. Place new Food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.steps_left += 100
            self._place__food()
            found_food = True
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

        return reward, self.score, game_over, found_food, won_game

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
    
    def add_to_path(self, parent):
        self.path.append(parent)

    def is_oob(self, point):
        if point.y < 0 or point.y >= self.h:
            return True
        
        if point.x < 0 or point.x >= self.w:
            return True
        
        return False
    
    def copy(self):
        snakeCopy = self.snake.copy()
        food = Point(self.food.x, self.food.y)
        path = self.path.copy()

        return SnakeGameLogic(direction=self.direction, snake=snakeCopy, food=food, score=self.score, moves_made=self.moves_made, path=path)


