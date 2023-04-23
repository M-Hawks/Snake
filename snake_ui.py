import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import math
pygame.init()
font = pygame.font.Font('arial.ttf',17)


BLOCK_SIZE = 20
SPEED = 40
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class SnakeGameUI:
    def __init__(self, snake_game):
        self.w = (snake_game.w  ) * BLOCK_SIZE
        self.h = (snake_game.h ) * BLOCK_SIZE
        self.snake_game = snake_game
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.frame_iteration = 0

    def update_ui(self):
        self.frame_iteration += 1

        self.display.fill(BLACK)
        for pt in self.snake_game.snake:
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x * BLOCK_SIZE,pt.y * BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display,BLUE2,pygame.Rect((pt.x * BLOCK_SIZE)+4,(pt.y * BLOCK_SIZE)+4,12,12))
        pygame.draw.rect(self.display,RED,pygame.Rect(self.snake_game.food.x * BLOCK_SIZE,self.snake_game.food.y * BLOCK_SIZE ,BLOCK_SIZE,BLOCK_SIZE))
        text = font.render("Score: "+str(self.snake_game.score) + " Moves: " + str(self.snake_game.steps_left),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()


        self.clock.tick(SPEED)