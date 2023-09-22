import pygame as pg
from os import path

from constants import *
from map import TiledMap, Camera
from sprites import Obstacle, Player


vec = pg.math.Vector2


def collide_with_obstacles(character, hit):
	# character's bottom and obstacle top
	if abs(hit.rect.top - character.rect.bottom) < COLLISION_TOLERANCE:
		character.vel.y = 0
		character.pos.y = hit.rect.top + 1
		character.ground_count += 1

	# character's top and obstacle bottom
	if abs(hit.rect.bottom - character.rect.top) < COLLISION_TOLERANCE:
		character.vel.y = 0 
		character.pos.y = (hit.rect.bottom - 1) + (character.rect.bottom - character.rect.top)

	if character.vel.y < 0:
		if abs(hit.rect.bottom - character.rect.top) < COLLISION_TOLERANCE + 30:
			character.vel.y = 0
			character.pos.y = (hit.rect.bottom - 1) + (character.rect.bottom - character.rect.top)

	# character's left and obstacle right
	if abs(hit.rect.right - character.rect.left) < COLLISION_TOLERANCE:
		character.vel.x = 0
		character.pos.x = hit.rect.right + character.rect.width/2 + 1

	# character's right and obstacle left
	if abs(hit.rect.left - character.rect.right) < COLLISION_TOLERANCE:
		character.vel.x = 0
		character.pos.x = hit.rect.left - character.rect.width/2 - 1


class Screen:
	def __init__(self, game):
		self.game = game
		
		self.load()
		self.new()

	def load(self):
		#  prepare map
		self.map = TiledMap(path.join(self.game.map_dir, 'Base Level.tmx'))
		self.map_img, self.map.rect = self.map.make_map()

	def new(self):
		# sprite groups
		self.all_sprites = pg.sprite.Group()
		self.obstacles = pg.sprite.Group()

		for obj in self.map.tmx_data.objects:
			obj_midbottom = vec(obj.x + obj.width/2, obj.y + obj.height)
			if obj.name == 'player':
				self.player = Player(self, obj_midbottom, self.all_sprites)
			elif obj.name == 'obstacle':
				Obstacle((obj.x, obj.y), (obj.width, obj.height), self.obstacles)

		self.camera = Camera(self.game, self.map.width, self.map.height)

	def run(self):
		while True:
			self.game.clock.tick(self.game.fps)
			self.game.events()
			self.update()
			self.display()

	def update(self):
		self.all_sprites.update()
		self.check_collisions()
		self.camera.update(self.player)

	def display(self):
		self.game.surface.blit(self.map_img, self.camera.apply(self.map))
		self.camera.draw(self.game.surface, self.all_sprites)

		pg.display.flip()

	def check_collisions(self):
		# PLAYER COLLISIONS
		# collision with obstacles
		hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
		if hits:
			for hit in hits:
				collide_with_obstacles(self.player, hit)
