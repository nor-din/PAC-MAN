from src.player import Player
from src.pacgum import Pacgum
from src.maze import Maze
from src.ghost import Ghost


class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.pacgum = Pacgum()
        self.ghost = Ghost()
    