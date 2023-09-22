import pygame as pg
from os import path

from constants import *
from base_sprite import Character
from spritesheet import Spritesheet, Animation


class Player(Character):
	def __init__(self, screen, pos, *groups):
		super().__init__(pos, PLAYER_DAMAGE, groups)
		self.screen = screen
		self.pos = pos
		self.jump_release = 0

		# image
		self.load()
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.midbottom = pos

		self.width = self.rect.right - self.rect.left
		self.height = self.rect.top - self.rect.bottom

	def load(self):
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), bg=(34, 177, 76))

		# MOVEMENT ANIMATIONS
		# walking animation
		walking_frames = [[22, 346, 62, 55], [88, 348, 65, 49], [160, 345, 65, 54], [238, 344, 53, 56], \
			[296, 338, 60, 57], [365, 342, 63, 51], [433, 343, 65, 52], [503, 343, 58, 55]]
		walking_anim = spritesheet.get_animation(walking_frames, 0.12, Animation.PlayMode.LOOP, scale=1.2)
		self.store_animation('walking', walking_anim)

		# standing animation
		standing_frames = [(28, 247, 34, 63), (73, 248, 34, 62), (115, 248, 35, 61)]
		standing_animation = spritesheet.get_animation(standing_frames, 0.20, Animation.PlayMode.LOOP, scale=1.2)
		self.store_animation('standing', standing_animation)

		# jumping animation
		jumping_frames = [(609, 343, 43, 51), (664, 337, 48, 64), (720, 338, 48, 64)]
		jumping_animation = spritesheet.get_animation(jumping_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('jumping', jumping_animation)

		# falling animation
		falling_frames = [(773, 344, 60, 50), (839, 323, 44, 80), (897, 326, 46, 77)]
		falling_animation = spritesheet.get_animation(falling_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('falling', falling_animation)

		# landing animation
		landing_frames = [(960, 336, 47, 69), (1023, 362, 47, 43), (1081, 352, 42, 52)]
		landing_animation = spritesheet.get_animation(landing_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('landing', landing_animation)

		# batarang throw
		batarang_throw_frames = [(20, 1004, 46, 54), (81, 997, 53, 61), (149, 1004, 82, 54), (239, 1004, 72, 54), (326, 1003, 67, 55)]
		batarang_throw_animation = spritesheet.get_animation(batarang_throw_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('batarang_throw', batarang_throw_animation)

	def animate(self):
		if self.active_name == "walking":
			if self.vel.x == 0:
				self.set_active_animation("standing")

			if self.vel.y < 0:
				self.set_active_animation("jumping")

		if self.active_name == "standing":
			if abs(self.vel.x) > 0:
				self.set_active_animation("walking")

			if self.vel.y < 0:
				self.set_active_animation("jumping")

		if self.active_name == "jumping":
			if self.vel.y > 0:
				self.set_active_animation("falling")

		if self.active_name == "falling":
			if self.ground_count > 0:
				self.set_active_animation("landing")

		if self.active_name == "landing":
			if self.is_animation_finished():
				if abs(self.vel.x) > 0:
					self.set_active_animation("walking")
				else:
					self.set_active_animation("standing")
			else:
				self.vel.x = 0

		if self.active_name == 'batarang_throw':
			if self.active_anim.get_frame_index(self.elapsed_time) > 1:
				if self.shoot_count == 0:
					if self.direction == 'R':
						self.screen.create_bullet(self.rect.midright, 1, PLAYER_BULLET_DAMAGE, self.screen.player_bullets, self.bullet_animation)
					elif self.direction == 'L':
						self.screen.create_bullet(self.rect.midleft, -1, PLAYER_BULLET_DAMAGE, self.screen.player_bullets, self.bullet_animation)
					self.shoot_count += 1

			if self.is_animation_finished():
				self.set_active_animation("standing")
				self.shoot_count = 0

		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)
		
		# flip image if necessary
		if self.direction == 'L':
			self.image = pg.transform.flip(self.image, True, False)

		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def move(self):
		keys = pg.key.get_pressed()
		
		# horizontal movement
		if keys[pg.K_a]:
			self.direction = 'L'
			if not self.attack_count > 0 and not self.active_name == 'batarang_throw':
				self.acc.x = -PLAYER_ACC
		
		elif keys[pg.K_d]:
			self.direction = 'R'
			if not self.attack_count > 0 and not self.active_name == 'batarang_throw':
				self.acc.x = PLAYER_ACC

		# jumping
		if keys[pg.K_w]:
			if self.jump_release > 0:
				if self.ground_count > 0 and not self.active_name == 'falling':
					self.vel.y = PLAYER_JUMP
					self.ground_count = 0
					self.jump_release = 0

		else:
			self.jump_release += 1


	def update(self):
		super().update(1/self.screen.game.fps)
		self.animate()

		# update properties
		self.width = self.rect.right - self.rect.left
		self.height = self.rect.top - self.rect.bottom

		self.rect.midbottom = self.pos


class Obstacle(pg.sprite.Sprite):
	def __init__(self, pos, size, *groups):
		super().__init__(groups)

		# rect
		self.rect = pg.Rect(pos, size)
		
		# position
		self.x = pos[0]
		self.y = pos[1]
		self.rect.x = pos[0]
		self.rect.y = pos[1]
