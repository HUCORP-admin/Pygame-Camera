import pygame as pg
import sys

from os import path

class Game:
    def __init__(self, title, dim):
        # initialize pygame
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(title)

        self.width = dim[0]
        self.height = dim[1]

        # set screen
        self.screen = None
        self.surface = pg.display.set_mode(dim)
        self.clock = pg.time.Clock()

        # current directory
        self.dir = path.dirname(__file__)

    def draw_text(self, x, y, font, color, text):
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.midtop = (x, y)
        self.surface.blit(surface, rect)

    def set_screen(self, scr):
        # delete existing
        if self.screen != None:
            del self.screen
            self.screen = None

        self.screen = scr

        # show new screen
        if (self.screen != None):
            self.screen.run()

    def quit(self):
        # exit
        pg.quit()
        sys.exit()

    def events(self):
        # handle events in game loop
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.quit()
