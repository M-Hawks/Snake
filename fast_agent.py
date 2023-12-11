import torch
import random
import numpy as np
from collections import deque
from snake_logic import SnakeGameLogic, Direction, Point
from model import Linear_QNet, QTrainer
from Helper import plot
from snake_logic import SnakeGameLogic
from snake_ui import SnakeGameUI
from snake_logic import GAME_SIZE


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.01


class Agent:
    def __init__(self):
        self.n_game = 0
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()

        self.model = Linear_QNet((2 * GAME_SIZE - 1) * (2 * GAME_SIZE - 1), 3).cuda()
        self.model.load_state_dict(torch.load('model.pth'))
        self.targetModel = Linear_QNet((2 * GAME_SIZE - 1) * (2 * GAME_SIZE - 1), 3).cuda()
        self.targetModel.load_state_dict(self.model.state_dict())

        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.highScore = 0
        # for n,p in self.model.named_parameters():
        #     print(p.device,'',n)
        # self.model.to('cuda')
        # for n,p in self.model.named_parameters():
        #     print(p.device,'',n)
        # TODO: model,trainer



    def get_state(self, game):
        # Rotate based on snake direction
        copyGrid = game.grid.copy()
        snakePos = Point(game.head.x, game.head.y)

        if game.direction == Direction.RIGHT:
            copyGrid = np.rot90(copyGrid, 1)
            snakePos = Point(GAME_SIZE - 1 - game.head.y, game.head.x)
        elif game.direction == Direction.LEFT:
            copyGrid = np.rot90(copyGrid, 3)
            snakePos = Point(game.head.y, GAME_SIZE - 1 - game.head.x)
        elif game.direction == Direction.DOWN:
            copyGrid = np.rot90(copyGrid, 2)
            snakePos = Point(game.head.y, game.head.x)

        # figure out offset to start writing into new grid.
        xOffset = GAME_SIZE - 1 - snakePos.x
        yOffset = GAME_SIZE - 1 - snakePos.y


        # write into new grid
        outGrid = np.full((2 * GAME_SIZE - 1, 2 * GAME_SIZE - 1), 1)
        for i in range(yOffset, yOffset + GAME_SIZE):
            for j in range(xOffset, xOffset + GAME_SIZE):
                outGrid[i][j] = copyGrid[i - yOffset][j - xOffset]

        # flatten new grid as input features.
        # print(outGrid)
        return outGrid.flatten()
        # return game.grid.copy().flatten()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if memory exceed

    def train_long_memory(self):
        if (len(self.memory) > BATCH_SIZE):
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, epsilon, epsilon_decay):
        # random moves: tradeoff explotation / exploitation
        final_move = [0, 0, 0]
        prob = random.random()
        if prob <= epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float).cuda()
            prediction = self.model(state0).cuda()  # prediction by model
            move = torch.argmax(prediction).item()
            final_move[move] = 1

            # decay the epsilon
            epsilon_decayed = epsilon * epsilon_decay
        return final_move


def main():
    epsilon = 1
    epsilon_decay = .8
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    game = SnakeGameLogic()
    agent = Agent()
    # ui = SnakeGameUI(game)
    i = 0
    while True:
        i += 1
        # Get Old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old, epsilon, epsilon_decay)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        # ui.update_ui()

        if done:
            # Train long memory,plot result
            game.reset()
            agent.n_game += 1
            agent.train_long_memory()
            if score > record:  # new High score
                record = score
            if agent.n_game % 100 == 0:

                plot(plot_scores, plot_mean_scores)
                print('Game:', agent.n_game, 'Score:', score, 'Record:', record)

                if agent.n_game % 500 == 0:
                    agent.model.save()

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_game
            plot_mean_scores.append(mean_score)




if (__name__ == "__main__"):
    main()