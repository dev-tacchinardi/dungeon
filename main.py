import kivent_core
import kivent_cymunk
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.config import Config
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivent_core.gameworld import GameWorld
from kivent_core.managers.resource_managers import texture_manager
from kivent_core.systems.renderers import RotateRenderer
from kivent_core.systems.position_systems import PositionSystem2D
from kivent_core.systems.rotate_systems import RotateSystem2D
from kivent_cymunk.interaction import CymunkTouchSystem
from kivy.properties import StringProperty, NumericProperty
from math import radians, pi, sin, cos

from random import randint, choice
from functools import partial
from os.path import dirname, join, abspath

from maze import Maze

__version__ = '0.0.1'


texture_manager.load_atlas(join(dirname(abspath(__file__)),
                                'assets', 'dungeon.atlas'))


class Dungeon(Widget):
    def __init__(self, **kwargs):
        super(Dungeon, self).__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['cymunk_physics', 'rotate_renderer', 'rotate', 'position',
             # 'cymunk_touch',
             'camera1'],
            callback=self.init_game)
        self.mazeobj = Maze()
        self.mazeobj.makeMap(50, 50, 100, 10, 30)
        self.maze = self.mazeobj.mapArr

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.draw_some_stuff()

    def draw_some_stuff(self):
        gameview = self.gameworld.system_manager['camera1']
        # x, y = int(-gameview.camera_pos[0]), int(-gameview.camera_pos[1])
        # w, h = int(gameview.size[0] + x), int(gameview.size[1] + y)
        create_wall = self.create_wall
        for y in range(50):
            for x in range(50):
                if self.maze[y][x] in [1, 2]:
                    create_wall((50*x, 50*y))
        # gameview.focus_entity = True
        # gameview.entity_to_focus = None
        # self.mazeobj.printt()
        
    def create_wall(self, pos):
        x_vel = y_vel = 0
        angle = radians(0)
        angular_velocity = radians(0)
        shape_dict = {'width': 50, 'height': 50, 'mass': 1}
        col_shape = {'shape_type': 'box', 'elasticity': .5,
                     'collision_type': 1, 'shape_info': shape_dict,
                     'friction': 1.0}
        col_shapes = [col_shape]
        physics_component = {
            'main_shape': 'circle',
            'velocity': (x_vel, y_vel),
            'position': pos, 'angle': angle,
            'angular_velocity': angular_velocity,
            'vel_limit': 0,
            'ang_vel_limit': radians(0),
            'mass': 10, 'col_shapes': col_shapes}
        create_component_dict = {
            'cymunk_physics': physics_component,
            'rotate_renderer': {
                'texture': 'wall',
                'size': (50, 50),
                'render': True},
            'position': pos, 'rotate': 0, }
        component_order = [
            'position', 'rotate', 'rotate_renderer', 'cymunk_physics']
        return self.gameworld.init_entity(
            create_component_dict, component_order)

    def update(self, dt):
        self.gameworld.update(dt)

    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=['rotate_renderer'],
            systems_removed=[], systems_paused=[],
            systems_unpaused=['rotate_renderer'],
            screenmanager_screen='main')

    def set_state(self):
        self.gameworld.state = 'main'


class DebugPanel(Widget):
    fps = StringProperty(None)

    def __init__(self, **kwargs):
        super(DebugPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.update_fps)

    def update_fps(self, dt):
        self.fps = str(int(Clock.get_fps()))
        Clock.schedule_once(self.update_fps, .05)


class DungeonApp(App):
    count = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Dungeon Explorer"


if __name__ == '__main__':
    DungeonApp().run()

# class Hero():
#     pass

# class Dungeon(GridLayout):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.cols = self.rows = 50
#         self.maze = Maze()
#         self.maze.makeMap(self.rows, self.cols, 100, 10, 30)
#         self.maze = self.maze.mapArr
#         self.position_maze()

#     def position_maze(self, start_y=0, start_x=0):
#         for line in self.maze:
#             for j in line:
#                 lbl = Label(text="")
#                 self.add_widget(lbl)
#                 if j in [1, 2]:
#                     lbl.image.source = "assets/wall.jpg"
                

# class DungeonGame(GridLayout):
#     pass

# class DungeonApp(App):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         Builder.load_file('assets/dungeon.kv')
#         self.title = "Dungeon Explorer"

#     def build(self):
#         game = DungeonGame()
#         return game

# if __name__ == '__main__':
#     Config.set('kivy', 'desktop', 1)
#     DungeonApp().run()
