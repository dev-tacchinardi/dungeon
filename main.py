from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.config import Config
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout

from maze import Maze

__version__ = '0.0.1'

class Hero():
    pass

class Dungeon(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.maze = Maze()
        self.maze.makeMap(100, 100, 100, 50, 300)
        self.maze = self.maze.mapArr
        # for y in range(100):
        #     line = ""
        #     for x in range(100):
        #         if self.maze[y][x] == 0:
        #             line += " "
        #         if self.maze[y][x] == 1:
        #             line += "#"
        #         if self.maze[y][x] == 2:
        #             line += "#"
        #         if self.maze[y][x] == 3 or self.maze[y][x] == 4 or self.maze[y][x] == 5:
        #             line += " "
        #     print(line)
        self.position_maze()

    def position_maze(self, start_y=0, start_x=0):
        for line in self.maze[start_y:start_y + 20]:
            for j in line[start_x:start_x + 20]:
                lbl = Label(text="")
                self.add_widget(lbl)
                if j in [1, 2]:
                    lbl.image.source = "assets/wall.jpg"
                

class DungeonGame(GridLayout):
    pass

class DungeonApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('assets/dungeon.kv')
        self.title = "Dungeon Explorer"

    def build(self):
        game = DungeonGame()
        return game

if __name__ == '__main__':
    Config.set('kivy', 'desktop', 1)
    DungeonApp().run()
