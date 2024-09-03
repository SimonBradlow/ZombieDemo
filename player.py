from settings import *
import pygame as pg
import spritesheet as ss
from projectile import *
import math

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.x, self.y = PLAYER_POS
        self.mx, self.my = (0, 0) # Mouse position
        self.angle = PLAYER_ANGLE
        self.radians = 0
        self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.SPRITE_SCALE = 48, 64, 3
        # Offset of center of sprite from (0,0) of sprite
        self.X_OFFSET = (self.SPRITE_WIDTH*self.SPRITE_SCALE)/2
        self.Y_OFFSET = (self.SPRITE_HEIGHT*self.SPRITE_SCALE)/2
        # Coordinates of top left of sprite, this is where we draw the sprite
        self.truex = self.x - self.X_OFFSET
        self.truey = self.y - self.Y_OFFSET
        # Converted relative angle for sprite rotation
        # Not actual angles, but the index of the sprites rotation
        self.idle_rangle = 0
        self.shooting_rangle = 0
        self.moving_rangle = 0
        self.shooting = False
        self.moving = False

        # Projectile group
        self.projectiles = pg.sprite.Group()

        # Load images
        idle_sprite_sheet_img = pg.image.load('assets/idle_gun.png').convert_alpha()
        idle_sprite_sheet = ss.SpriteSheet(idle_sprite_sheet_img)

        shooting_sprite_sheet_img = pg.image.load('assets/shooting_fix.png').convert_alpha()
        shooting_sprite_sheet = ss.SpriteSheet(shooting_sprite_sheet_img)

        moving_sprite_sheet_img = pg.image.load('assets/run_gun.png').convert_alpha()
        moving_sprite_sheet = ss.SpriteSheet(moving_sprite_sheet_img)

        shadow_img = pg.image.load('assets/shadow.png').convert_alpha()
        shadow_sheet = ss.SpriteSheet(shadow_img)

        self.projectile_img = pg.image.load('assets/bullet.png').convert_alpha()
        self.bullet_offsets = [(-4, 10), (-14, 6), (-14, -2), (-11, -7), 
                               (5, -13), (16, -6), (15, -2), (13, 8)]

        # Animation Vars
        # 2d arrays storing sprite lists for each direction
        self.idle_animation_lists = []
        self.shooting_animation_lists = []
        self.moving_animation_lists = []

        # number of frames per animation
        animation_steps = 8
        # number of rows per sprite
        idle_animation_rows = 6
        shooting_animation_rows = 8
        # current frame of animation
        self.current_idle_step = 0
        self.current_shooting_step = 0
        self.current_moving_step = 0

        # Process sprite sheets into lists
        for i in range(idle_animation_rows):
            tmp_list = []
            for j in range(animation_steps):
                tmp_list.append(idle_sprite_sheet.get_image(i, j, 
                                                            self.SPRITE_WIDTH, 
                                                            self.SPRITE_HEIGHT, 
                                                            self.SPRITE_SCALE))
            self.idle_animation_lists.append(tmp_list)

        for i in range(shooting_animation_rows):
            tmp_list = []
            for j in range(animation_steps):
                tmp_list.append(shooting_sprite_sheet.get_image(i, j, 
                                                            self.SPRITE_WIDTH, 
                                                            self.SPRITE_HEIGHT, 
                                                            self.SPRITE_SCALE))
            self.shooting_animation_lists.append(tmp_list)

        for i in range(shooting_animation_rows):
            tmp_list = []
            for j in range(animation_steps):
                tmp_list.append(moving_sprite_sheet.get_image(i, j, 
                                                            self.SPRITE_WIDTH, 
                                                            self.SPRITE_HEIGHT, 
                                                            self.SPRITE_SCALE))
            self.moving_animation_lists.append(tmp_list)

        self.shadow = shadow_sheet.get_image(0, 0, 
                                             self.SPRITE_WIDTH, 
                                             self.SPRITE_HEIGHT, 
                                             self.SPRITE_SCALE)

        # Set player position to center
        self.x = (REAL_WIDTH // 2)
        self.y = (REAL_HEIGHT // 2)

    def update(self):
        self.movement()
        self.projectiles.update()

        # angle normalization to match assets/idle.png
        self.idle_rangle = int(abs(((self.angle + 150) % 360) - 360) // 60)
        self.shooting_rangle = int(abs(((self.angle + 157.5) % 360) - 360) // 45)
        
        # projectile group
        if self.shooting:
            if (self.current_shooting_step%12 == 0):
                self.projectiles.add(Projectile(self.projectile_img, 
                                                self.x + (self.SPRITE_SCALE*self.bullet_offsets[self.shooting_rangle][0]), 
                                                self.y + (self.SPRITE_SCALE*self.bullet_offsets[self.shooting_rangle][1]), 
                                                self.radians))
            # hacky deltatime nonsense
            self.current_shooting_step = (self.current_shooting_step+1) % 48
        else:
            self.current_shooting_step = 0

        # hacky deltatime nonsense - PLEASE FIX
        self.current_idle_step = (self.current_idle_step+1) % 128
        self.current_moving_step = (self.current_moving_step+1) % 48

    def draw(self):
        # draw shadow
        self.screen.blit(self.shadow, (self.truex, self.truey))

        # Projectiles
        self.projectiles.draw(self.screen)

        # draw sprite (over shadow)
        if self.shooting: # shooting
            self.screen.blit(self.shooting_animation_lists[self.shooting_rangle][self.current_shooting_step//6], 
                             (self.truex, self.truey))
        elif self.moving: #moving
            self.screen.blit(self.moving_animation_lists[self.moving_rangle][self.current_moving_step//6], 
                             (self.truex, self.truey))
        else: # idle
            self.screen.blit(self.idle_animation_lists[self.idle_rangle][self.current_idle_step//16], 
                             (self.truex, self.truey))

        # draw line for mouse angle
        #WHITE = (255, 255, 255)
        #pg.draw.line(self.screen, WHITE, (self.x, self.y), (self.mx, self.my))

    def movement(self):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w] and not self.shooting:
            self.moving = True # Update flag
            self.moving_rangle = 3 # Assign sprite rotation index
            num_key_pressed += 1 # key press counter for diagonal movement
            if self.y > REAL_HEIGHT/9: # bounding box
                dy += -speed
        if keys[pg.K_s] and not self.shooting:
            self.moving = True
            self.moving_rangle = 0
            num_key_pressed += 1
            if self.y < ((REAL_HEIGHT/5)*4)+10:
                dy += speed
        if keys[pg.K_a] and not self.shooting:
            self.moving = True
            self.moving_rangle = 7
            num_key_pressed += 1
            if self.x > (REAL_WIDTH/10)+5:
                dx += -speed
        if keys[pg.K_d] and not self.shooting:
            self.moving = True
            self.moving_rangle = 6
            num_key_pressed += 1
            if self.x < ((REAL_WIDTH/10)*9)-5:
                dx += speed

        if num_key_pressed == -1:
            self.moving = False

        # diag move correction
        # sin(45) and cos(45) are the same magic number
        self.diag_move_corr = 0.70710678118
        if num_key_pressed:
            # multiply our velocities by the magic number
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr
            # Hacky fix to switch sprite angle for diagonals
            if ((dx < 0) and (dy < 0)): self.moving_rangle = 2
            if ((dx > 0) and (dy < 0)): self.moving_rangle = 4
            if ((dx > 0) and (dy > 0)): self.moving_rangle = 5
            if ((dx < 0) and (dy > 0)): self.moving_rangle = 1

        #update position
        self.x += dx
        self.y += dy
        self.truex = self.x - self.X_OFFSET
        self.truey = self.y - self.Y_OFFSET

    def mouse_control(self):
        # Get mouse pos
        self.mx, self.my = self.game.cursor.centerx, self.game.cursor.centery
        # Compute angle
        self.angle = math.atan2(self.x-self.mx, self.y-self.my)
        self.radians = self.angle
        # Convert from radians into degrees
        self.angle %= 2*math.pi
        self.angle = math.degrees(self.angle)
