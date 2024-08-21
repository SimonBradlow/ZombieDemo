from settings import *
import pygame as pg
import spritesheet as ss
from projectile import *
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.game = game
        self.x, self.y = (x, y)

        enemy_img = pg.image.load('assets/box.png').convert_alpha()
        enemy_img = pg.transform.scale_by(enemy_img, 3)
        #enemy_sheet = ss.SpriteSheet(idle_sprite_sheet_img)

        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # could be moved to the projectile.update()
        # not sure, though, which needs the info more
        csprite = pg.sprite.spritecollideany(self, self.game.player.projectiles)
        if csprite is not None:
            csprite.kill()

    #def draw(self):
    #    self.image.blit(enemy_img, (x, y))
