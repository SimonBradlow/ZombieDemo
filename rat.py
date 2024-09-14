from settings import *
import pygame as pg
import spritesheet as ss
from ratprojectile import *
import math

class Rat(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.x, self.y = (x, y)
        self.face_right = True
        self.left_adj = 0
        self.down= False
        self.moving = False
        self.shooting = False
        self.is_hit = False
        self.hit_timer = 0
        self.flash_duration = 100
        self.angle = 0
        self.radians = 0

        self.SPRITE_WIDTH = 96
        self.SPRITE_HEIGHT = 96
        self.SPRITE_SCALE = 3

        # Offset of center of sprite from (0,0) of sprite
        self.X_OFFSET = (self.SPRITE_WIDTH*self.SPRITE_SCALE)/2
        self.Y_OFFSET = (self.SPRITE_HEIGHT*self.SPRITE_SCALE)/2
        # Coordinates of top left of sprite, this is where we draw the sprite
        self.truex = self.x - self.X_OFFSET
        self.truey = self.y - self.Y_OFFSET
        self.visualcx, self.visualcy = self.x+24, self.y+96

        # Load sprite sheets
        idle_sheet_img = pg.image.load('assets/rat/Idle.png').convert_alpha()
        idle_sheet = ss.SpriteSheet(idle_sheet_img)
        walk_sheet_img = pg.image.load('assets/rat/Walk.png').convert_alpha()
        walk_sheet = ss.SpriteSheet(walk_sheet_img)
        hurt_sheet_img = pg.image.load('assets/rat/Hurt.png').convert_alpha()
        hurt_sheet = ss.SpriteSheet(hurt_sheet_img)
        trail_sheet_img = pg.image.load('assets/rat/rocket_trail.png').convert_alpha()
        trail_sheet = ss.SpriteSheet(trail_sheet_img)
        particle_sheet_img = pg.image.load('assets/rat/particle.png').convert_alpha()
        particle_sheet = ss.SpriteSheet(particle_sheet_img)

        # Process sprite sheets into lists
        self.idle_list = []
        self.walk_list = []
        self.trail_list = []
        self.particle_list = []
        self.hurt_list = []

        for i in range(4):
            self.idle_list.append(idle_sheet.get_image(0, i, 
                                                       self.SPRITE_WIDTH, 
                                                       self.SPRITE_HEIGHT, 
                                                       self.SPRITE_SCALE))
        for i in range(6):
            self.walk_list.append(walk_sheet.get_image(0, i, 
                                                       self.SPRITE_WIDTH, 
                                                       self.SPRITE_HEIGHT, 
                                                       self.SPRITE_SCALE))
        for i in range(2):
            self.hurt_list.append(hurt_sheet.get_image(0, i, 
                                                       self.SPRITE_WIDTH, 
                                                       self.SPRITE_HEIGHT, 
                                                       self.SPRITE_SCALE))
        for i in range(6):
            self.trail_list.append(trail_sheet.get_image(0, i, 
                                                         self.SPRITE_WIDTH, 
                                                         self.SPRITE_HEIGHT, 
                                                         self.SPRITE_SCALE))
        for i in range(8):
            self.particle_list.append(particle_sheet.get_image(0, i, 
                                                         64, 
                                                         64, 
                                                         1.5))
        
        # current frame index
        self.current_idle_step = 0
        self.current_walk_step = 0
        self.current_shoot_step = 0

        # init self sprite values
        self.image = self.idle_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # projectile group for rockets
        self.projectiles = pg.sprite.Group()

        # rocket image and spawn offset
        self.rocket_image = pg.image.load('assets/rat/Rocket1.png').convert_alpha()
        self.rocket_image = pg.transform.scale_by(self.rocket_image, 3)
        self.projectile_offset = (40, 6)

        # Shadow
        shadow_img = pg.image.load('assets/bigshadow.png').convert_alpha()
        shadow_sheet = ss.SpriteSheet(shadow_img)
        self.shadow = shadow_sheet.get_image(0, 0, 
                                             self.SPRITE_WIDTH, 
                                             self.SPRITE_HEIGHT, 
                                             self.SPRITE_SCALE)

    def update(self):
        self.projectiles.update()
        keys = pg.key.get_pressed()
        if self.visualcx > self.game.player.x:
            self.face_right = False
            self.left_adj = 48
        else:
            self.face_right = True
            self.left_adj = 0
        
        # input on T key to debug shooting
        if keys[pg.K_t] and not self.shooting:
            self.shooting = True
            # Calculate angle from cannon to player
            self.radians = math.atan2((self.x + (self.projectile_offset[0]*self.SPRITE_SCALE)) - self.game.player.x, 
                                      (self.y + (self.projectile_offset[1]*self.SPRITE_SCALE)) - self.game.player.y)

            # Points
            start_point = ((self.x + (self.projectile_offset[0]*self.SPRITE_SCALE)), 
                           (self.y + (self.projectile_offset[1]*self.SPRITE_SCALE)))  # Starting point
            end_point = (self.game.player.x, 
                         self.game.player.y)    # End point
            tangent_angle = math.radians(350)  # Angle of tangent in radians
            control_distance = 300  # How far the control point is from the start point

            # fix points if facing left
            if not self.face_right:
                start_point = ((self.x - (self.projectile_offset[0]*self.SPRITE_SCALE)), 
                               (self.y + (self.projectile_offset[1]*self.SPRITE_SCALE)))  # Starting point
                tangent_angle = math.radians(190)

            # Calculate the control point
            control_point = calculate_control_point(start_point, 
                                                    tangent_angle, 
                                                    control_distance)

            # create projectile for shot and add to projectile group
            #img = pg.transform.rotate(self.projectile_sprite_list[0], self.angle)
            self.projectiles.add(RatProjectile(self.game,
                                               self.rocket_image, 
                                               self.particle_list,
                                               start_point[0], 
                                               start_point[1],
                                               end_point[0],
                                               end_point[1]+30,
                                               control_point[0],
                                               control_point[1]))


        # Increment frame counters
        self.current_idle_step = (self.current_idle_step+1) % 64
        self.current_walk_step = (self.current_walk_step+1) % 36
        self.current_shoot_step = (self.current_shoot_step+1) % 12

        if self.current_shoot_step == 11:
            self.shooting = False

        if self.moving:
            self.image = self.walk_list[self.current_walk_step//6]
        else: #idle
            self.image = self.idle_list[self.current_idle_step//16]

        # flip self.image if facing left
        if not self.face_right:
            self.image = pg.transform.flip(self.image, True, False)

        coll_surf = pg.sprite.Sprite()
        coll_surf.rect = pg.Rect(self.visualcx-self.left_adj-80, self.visualcy-50, 160, 100)
        csprite_list = pg.sprite.spritecollide(coll_surf, self.game.player.projectiles, False)
        if csprite_list is not None:
            for csprite in csprite_list:
                if not csprite.has_hit:
                    self.is_hit = True
                    self.current_hit_step = 0
                    self.hit_timer = pg.time.get_ticks()
                    csprite.new_kill()

        # Flash logic: if hit, switch to a dynamically created white image
        if self.is_hit:
            current_time = pg.time.get_ticks()
            if current_time - self.hit_timer > self.flash_duration:
                self.is_hit = False
            else:
                tmp_img = self.image.copy()
                tmp_img.fill((96, 96, 96), special_flags=pg.BLEND_RGB_ADD)
                self.image = tmp_img


        self.decide_action()

    def draw(self):
        # rocket trail
        if self.shooting:
            img = self.trail_list[self.current_shoot_step//6]
            # flip image if facing left
            if not self.face_right:
                img = pg.transform.flip(img, True, False)
            self.screen.blit(img, (self.truex, self.truey))
        # rocket
        self.projectiles.draw(self.screen)

    def draw_shadow(self):
        self.screen.blit(self.shadow, (self.truex+30, self.truey+130))

    def draw_rocket_zone(self):
        for item in self.projectiles:
            if item.particle_step == 0:
                tmp_rect = pg.Rect(0, 0, 80, 60)
                tmp_rect.center = item.end_point
                ellipse_surface = pg.Surface((80, 60))
                ellipse_surface.set_colorkey((0,0,0))
                ellipse_surface.set_alpha(64)
                pg.draw.ellipse(ellipse_surface, (255, 0, 0), (0, 0, 80, 60))
                pg.draw.ellipse(ellipse_surface, (153, 0, 0), (0, 0, 80, 60), 3)
                self.game.screen.blit(ellipse_surface, (item.end_point[0]-40, item.end_point[1]-30))

    def decide_action(self):
        self.move_towards_player()

    def move_towards_player(self):
        VELOCITY         = 5
        LERP_FACTOR      = 0.05
        minimum_distance = 190
        maximum_distance = 2000

        ppos = (self.game.player.x, self.game.player.y)
        fpos = (self.visualcx, self.visualcy)

        target_vector       = pg.math.Vector2(*ppos)
        follower_vector     = pg.math.Vector2(*fpos)
        new_follower_vector = pg.math.Vector2(*fpos)

        distance = follower_vector.distance_to(target_vector)
        if distance > minimum_distance+10:
            self.moving = True
            direction_vector    = (target_vector - follower_vector) / distance
            min_step            = max(0, distance - maximum_distance)
            max_step            = distance - minimum_distance
            #step_distance       = min(max_step, max(min_step, VELOCITY))
            step_distance       = min_step + (max_step - min_step) * LERP_FACTOR
            new_follower_vector = follower_vector + direction_vector * step_distance
        else:
            self.moving = False

        #update position
        self.visualcx = new_follower_vector.x
        self.visualcy = new_follower_vector.y
        self.x, self.y = self.visualcx-24, self.visualcy-96

        self.truex = self.x - self.X_OFFSET
        self.truey = self.y - self.Y_OFFSET
        self.rect.center = (self.x, self.y)
