from settings import *
import pygame as pg
import math

# Function to calculate a point on the quadratic bezier curve
def bezier_point(p0, p1, p2, t):
    """ Returns a point on a quadratic Bezier curve given by points p0, p1, and p2, at time t """
    x = (1-t)**2 * p0[0] + 2 * (1-t) * t * p1[0] + t**2 * p2[0]
    y = (1-t)**2 * p0[1] + 2 * (1-t) * t * p1[1] + t**2 * p2[1]
    return (x, y)

# Function to calculate a slope of a pointon the quadratic bezier curve
def bezier_derivative(p0, p1, p2, t):
    """ Returns the derivative of the Bezier curve at time t """
    dx = 2*(1-t)*(p1[0] - p0[0]) + 2*t*(p2[0] - p1[0])
    dy = 2*(1-t)*(p1[1] - p0[1]) + 2*t*(p2[1] - p1[1])
    return (dx, dy)

# Calculate control point from angle
def calculate_control_point(start, angle, distance):
    """ Calculate control point using angle and distance from the start point """
    dx = distance * math.cos(angle)
    dy = distance * math.sin(angle)
    return (start[0] + dx, start[1] + dy)

#create class for squares
class RatProjectile(pg.sprite.Sprite):
    def __init__(self, game, img, ilist, ilist2, sx, sy, ex, ey, cx, cy):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.original_image = img
        self.image = img
        self.particle_list = ilist
        self.hit_particle_list = ilist2
        self.rect = self.image.get_rect()
        self.start_point = (sx, sy)
        self.end_point = (ex, ey)
        self.control_point = (cx, cy)
        self.rect.center = self.start_point
        self.t = 0
        self.speed = 1/18
        self.particle_step = 0

    def update(self):
        self.t += self.speed

        if self.t < 1:
            # Update the position based on the new t
            d_pos = bezier_point(self.start_point, self.control_point, self.end_point, self.t)
            self.rect.center = d_pos

            # Calculate the derivative to get the slope at the current point
            derivative = bezier_derivative(self.start_point, self.control_point, self.end_point, self.t)

            # Calculate the angle of the slope
            angle = math.degrees(math.atan2(derivative[1], derivative[0]))

            # Rotate the image based on the angle
            self.image = pg.transform.rotate(self.original_image, -angle)  # Negative because pygame rotates counterclockwise
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            # Only on first frame of impact
            if self.particle_step == 0:
                x1, y1 = self.end_point
                x2, y2 = self.game.player.x, self.game.player.y
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if distance < 40:
                    #self.game.player.health -= 10
                    self.game.player.take_hit()
                    self.particle_list = self.hit_particle_list
                    self.end_point = (self.end_point[0], self.end_point[1]-30)

            self.t = 1
            self.particle_step = (self.particle_step+1) % 24
            self.image = self.particle_list[self.particle_step//3] 
            self.rect = self.image.get_rect()
            self.rect.center = self.end_point

            # Only on last frame
            if self.particle_step == 23:
                self.kill()
