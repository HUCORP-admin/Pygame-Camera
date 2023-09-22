import pygame as pg
from pytmx.util_pygame import load_pygame


class TiledMap:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
        self.width = self.tmx_data.width*self.tmx_data.tilewidth
        self.height = self.tmx_data.height*self.tmx_data.tileheight

    def render(self, surface):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmx_data.tilewidth, y*self.tmx_data.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface, temp_surface.get_rect()
