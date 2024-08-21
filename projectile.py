from settings import *
import pygame as pg
import math

#create class for squares
class Projectile(pg.sprite.Sprite):
    def __init__(self, img, x, y, angle):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle

    def update(self):
        speed = 24
        dx = (speed*math.cos(self.angle)) * -1
        dy = (speed*math.sin(self.angle)) * -1
        self.rect.move_ip(dy, dx)

        if ((self.rect.top > REAL_HEIGHT) or (self.rect.left > REAL_WIDTH) or 
            (self.rect.bottom < 0) or (self.rect.left < 0)):
            self.kill()
