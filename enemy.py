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

        self.enemy_img = pg.image.load('assets/box.png').convert_alpha()
        self.enemy_img = pg.transform.scale_by(self.enemy_img, 3)
        self.enemyhit_img = pg.image.load('assets/boxhit.png').convert_alpha()
        self.enemyhit_img = pg.transform.scale_by(self.enemyhit_img, 3)
        
        self.hit = False
        self.current_hit_step = 0
        #enemy_sheet = ss.SpriteSheet(idle_sprite_sheet_img)

        self.image = self.enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if self.hit:
            self.current_hit_step = (self.current_hit_step+1) % 6
            if self.current_hit_step == 0: 
                self.hit = False
                self.image = self.enemy_img
        # could be moved to the projectile.update()
        # not sure, though, which needs the info more
        csprite = pg.sprite.spritecollideany(self, self.game.player.projectiles)
        if csprite is not None:
            self.hit = True
            self.current_hit_step = 0
            self.image = self.enemyhit_img
            csprite.kill()

    #def draw(self):
    #    self.image.blit(self.enemy_img, (x, y))
