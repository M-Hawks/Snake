from queue import PriorityQueue

# game: grid, came_from, hueristic

class A_Star:
    def __init__(self, game) -> None:
        self.game = game
        pass
    
    def get_path(self):
        open_set = PriorityQueue()
        start = self.game
        open_set.put((start.heuristic, start))
        # construct path for every move
        while not open_set.empty():
            current = open_set.get()[1]
            #TODO: check if current is end
            if current.end:
                return current
            #check neighbors add to queue
            for neighbor in self.get_neighbors(current):
                    open_set.put((neighbor.heuristic, neighbor))
        return None
    
    #get different game states to pass back to the agent
    def get_neighbors(self, current):
        s_game = self.current.copy()
        r_game = self.current.copy()
        l_game = self.current.copy()
        straight = self.s_game.play_step((1,0,0))
        right = self.r_game.play_step((0,1,0))
        left = self.l_game.play_step((0,0,1))
        return [straight, right, left]
def main():
    game = SnakeGameLogic()
    a_star = A_Star(game)
    #TODO: fenagle with the while loop... while loop is while end state can be reached.
    while fruit_loop:
        path = a_star.get_path()
        

    pass
   
    
    