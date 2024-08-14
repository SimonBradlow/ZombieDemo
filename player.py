from settings import *
import pygame as pg
import spritesheet as ss
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.x, self.y = PLAYER_POS
        self.mx, self.my = (0, 0)
        self.angle = PLAYER_ANGLE
        self.idle_rangle = 0
        self.shooting_rangle = 8
        self.shooting = False

        idle_sprite_sheet_img = pg.image.load('assets/idle.png').convert_alpha()
        idle_sprite_sheet = ss.SpriteSheet(idle_sprite_sheet_img)

        shooting_sprite_sheet_img = pg.image.load('assets/shooting_fix.png').convert_alpha()
        shooting_sprite_sheet = ss.SpriteSheet(shooting_sprite_sheet_img)

        self.idle_animation_lists = []
        self.shooting_animation_lists = []
        animation_steps = 8
        idle_animation_rows = 6
        shooting_animation_rows = 8
        self.current_idle_step = 0
        self.current_shooting_step = 0

        for i in range(idle_animation_rows):
            tmp_list = []
            for j in range(animation_steps):
                tmp_list.append(idle_sprite_sheet.get_image(i, j, 48, 64, 3))
            self.idle_animation_lists.append(tmp_list)

        for i in range(shooting_animation_rows):
            tmp_list = []
            for j in range(animation_steps):
                tmp_list.append(shooting_sprite_sheet.get_image(i, j, 48, 64, 3))
            self.shooting_animation_lists.append(tmp_list)

        self.x = (REAL_WIDTH // 2)
        self.y = (REAL_HEIGHT // 2)

    def update(self):
        self.mouse_control()
        # angle normalization to match assets/idle.png
        self.idle_rangle = int(abs(((self.angle + 150) % 360) - 360) // 60)
        self.shooting_rangle = int(abs(((self.angle + 157.5) % 360) - 360) // 45)
        # hacky deltatime nonsense - PLEASE FIX
        self.current_idle_step = (self.current_idle_step+1)%128
        self.current_shooting_step = (self.current_shooting_step+1)%48

    def draw(self):
        # draw sprite
        if self.shooting: # shooting
            self.screen.blit(self.shooting_animation_lists[self.shooting_rangle][self.current_shooting_step//6], (self.x-72, self.y-96))
        else: # idle
            self.screen.blit(self.idle_animation_lists[self.idle_rangle][self.current_idle_step//16], (self.x-72, self.y-96))

        # draw line for mouse angle
        WHITE = (255, 255, 255)
        pg.draw.line(self.screen, WHITE, (self.x, self.y), (self.mx, self.my))

    def movement(self):
        pass

        '''
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # diag move correction
        #if num_key_pressed:
        #    dx *= self.diag_move_corr
        #    dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        #if keys[pg.K_LEFT]:
        #    self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        #if keys[pg.K_RIGHT]:
        #    self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        '''

    def mouse_control(self):
        self.mx, self.my = pg.mouse.get_pos()
        self.angle = math.atan2(self.x-self.mx, self.y-self.my)
        self.angle %= 2*math.pi
        self.angle = math.degrees(self.angle)
