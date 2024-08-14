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
        self.shooting_rangle = 0
        self.moving_rangle = 0
        self.shooting = False
        self.moving = False

        # Load images
        idle_sprite_sheet_img = pg.image.load('assets/idle_gun.png').convert_alpha()
        idle_sprite_sheet = ss.SpriteSheet(idle_sprite_sheet_img)

        shooting_sprite_sheet_img = pg.image.load('assets/shooting_fix.png').convert_alpha()
        shooting_sprite_sheet = ss.SpriteSheet(shooting_sprite_sheet_img)

        moving_sprite_sheet_img = pg.image.load('assets/run_gun.png').convert_alpha()
        moving_sprite_sheet = ss.SpriteSheet(moving_sprite_sheet_img)

        # Animation Vars
        self.idle_animation_lists = []
        self.shooting_animation_lists = []
        self.moving_animation_lists = []
        animation_steps = 8
        idle_animation_rows = 6
        shooting_animation_rows = 8
        self.current_idle_step = 0
        self.current_shooting_step = 0

        # Process sprite sheets into lists
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

        for i in range(shooting_animation_rows):
            tmp_list = []
            for j in range(animation_steps):
                tmp_list.append(moving_sprite_sheet.get_image(i, j, 48, 64, 3))
            self.moving_animation_lists.append(tmp_list)

        # Set player position to center
        self.x = (REAL_WIDTH // 2)
        self.y = (REAL_HEIGHT // 2)

    def update(self):
        self.movement()
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
        elif self.moving: #moving
            self.screen.blit(self.moving_animation_lists[self.moving_rangle][self.current_shooting_step//6], (self.x-72, self.y-96))
        else: # idle
            self.screen.blit(self.idle_animation_lists[self.idle_rangle][self.current_idle_step//16], (self.x-72, self.y-96))

        # draw line for mouse angle
        #WHITE = (255, 255, 255)
        #pg.draw.line(self.screen, WHITE, (self.x, self.y), (self.mx, self.my))

    def movement(self):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w] and not self.shooting:
            self.moving = True
            self.moving_rangle = 3
            num_key_pressed += 1
            if self.y > 115:
                dy += -speed
        if keys[pg.K_s] and not self.shooting:
            self.moving = True
            self.moving_rangle = 0
            num_key_pressed += 1
            if self.y < (REAL_HEIGHT-165):
                dy += speed
        if keys[pg.K_a] and not self.shooting:
            self.moving = True
            self.moving_rangle = 7
            num_key_pressed += 1
            if self.x > 125:
                dx += -speed
        if keys[pg.K_d] and not self.shooting:
            self.moving = True
            self.moving_rangle = 6
            num_key_pressed += 1
            if self.x < (REAL_WIDTH-125):
                dx += speed

        if num_key_pressed == -1:
            self.moving = False

        # diag move correction
        self.diag_move_corr = 0.70710678118
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr
            if ((dx < 0) and (dy < 0)): self.moving_rangle = 2
            if ((dx > 0) and (dy < 0)): self.moving_rangle = 4
            if ((dx > 0) and (dy > 0)): self.moving_rangle = 5
            if ((dx < 0) and (dy > 0)): self.moving_rangle = 1

        self.x += dx
        self.y += dy

    def mouse_control(self):
        # Get mouse pos
        self.mx, self.my = pg.mouse.get_pos()
        # Compute angle
        self.angle = math.atan2(self.x-self.mx, self.y-self.my)
        # Convert from radians into degrees
        self.angle %= 2*math.pi
        self.angle = math.degrees(self.angle)
