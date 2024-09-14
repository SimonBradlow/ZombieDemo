from settings import *
import pygame as pg
import math

#create class for squares
class Projectile(pg.sprite.Sprite):
    def __init__(self, img, ilist, x, y, angle):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.particle_list = ilist
        self.has_hit = False
        self.hit_step = 0

    def update(self):
        if not self.has_hit:
            speed = 24
            dx = (speed*math.cos(self.angle)) * -1
            dy = (speed*math.sin(self.angle)) * -1
            self.rect.move_ip(dy, dx)

        if self.has_hit:
            self.hit_step = (self.hit_step+1) % 32
            x, y = self.rect.center
            self.image = self.particle_list[self.hit_step//4]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            if self.hit_step == 31:
                self.kill()

        if ((self.rect.top > REAL_HEIGHT) or (self.rect.left > REAL_WIDTH) or 
            (self.rect.bottom < 0) or (self.rect.left < 0)):
            self.kill()

    def new_kill(self):
        self.has_hit = True
