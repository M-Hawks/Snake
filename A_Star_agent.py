from queue import PriorityQueue
from snake_logic import SnakeGameLogic
from snake_ui import SnakeGameUI



# game: grid, came_from, hueristic
class A_Star:
    def __init__(self) -> None:
        pass


    def get_path(self, game):
        open_set = PriorityQueue()

        open_set.put((game.hueristic(), game))
        directions = [(1,0,0), (0,1,0), (0,0,1)]
        # construct path for every move
        while not open_set.empty():
            game = open_set.get()[1]
            for dir in directions:
                child = game.copy()
                _, _, dead, found_food, win = child.play_step(dir)
                child.add_to_path(game)
                if dead:
                    continue
                if found_food:
                    return child, win
                open_set.put((game.hueristic(), child))
        return None, False

    
    #if crashed: stop #if ate: reset #if moved: continue #if win: stop

if __name__ == "__main__":
    game = SnakeGameLogic()
    a_star = A_Star()
    ui = SnakeGameUI(game)
    while True:
        game, win = a_star.get_path(game)
        if win:
            break
        if game == None:
            break
        #pass to the ui the game path
        for step in game.path:
            ui.update_ui(step)
        ui.update_ui(game)
        #game resets for next fruit loop
        game.path = []
    pass
   
    
    