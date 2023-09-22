from constants import *
from game import Game
from os import path

from screen import Screen


class Launcher(Game):
    def __init__(self):
        super().__init__('CameraDemo', (WIDTH, HEIGHT))

        # asset directories
        self.img_dir = path.join(self.dir, 'assets', 'img')
        self.map_dir = path.join(self.dir, 'assets', 'map')

        # settings
        self.fps = 60

    def start(self):
        screen = Screen(self)
        self.set_screen(screen)


if __name__ == '__main__':
    launcher = Launcher()
    launcher.start()
    