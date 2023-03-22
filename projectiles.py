import random
import arcade
import math
from math import sqrt

BASIC_PROJECTILE_SPEED = 4
SEAL_PROJECTILE_SPEED = 5
SPRITE_SCALING_CARROT = 0.05

class Basic_Projectile(arcade.Sprite):
    target_x = None
    target_y = None
    player_location = (0,0)
    image = "images/carrot.png"
    scale = SPRITE_SCALING_CARROT

    def __init__(self, target_x, target_y, player_location):
        super().__init__(self.image, self.scale)
        self.position = player_location
        self.target_x = target_x
        self.target_y = target_y
        self.player_location = player_location

    def move(self):   
        player_x = self.player_location[0]
        player_y = self.player_location[1]
        
        delta_x = self.target_x - player_x
        delta_y = self.target_y - player_y

        magnitude = abs(sqrt((delta_x * delta_x) + (delta_y * delta_y)))

        unit_x = delta_x / magnitude
        unit_y = delta_y / magnitude

        self.change_x = unit_x * BASIC_PROJECTILE_SPEED
        self.change_y = unit_y * BASIC_PROJECTILE_SPEED

        self.center_x += self.change_x
        self.center_y += self.change_y

class Splinter_Projectile(arcade.Sprite):
    target_x = None
    target_y = None
    spawn_location = (0,0)
    splinters_left = None

    def __init__(self, image, scale, target_x, target_y, spawn_location, splinters_left):
        super().__init__(image, scale)
        self.position = spawn_location
        self.target_x = target_x
        self.target_y = target_y
        self.splinters_left = splinters_left
        self.spawn_location = spawn_location

    def move(self):
        
        spawn_x = self.spawn_location[0]
        spawn_y = self.spawn_location[1]
        
        delta_x = self.target_x - spawn_x
        delta_y = self.target_y - spawn_y

        magnitude = abs(sqrt((delta_x * delta_x) + (delta_y * delta_y)))

        unit_x = delta_x / magnitude
        unit_y = delta_y / magnitude

        self.change_x = unit_x * 4
        self.change_y = unit_y * 4

        self.center_x += self.change_x
        self.center_y += self.change_y

class Seal_Projectile(arcade.Sprite):
    target_x = None
    target_y = None
    start_location = (0,0)
    image = "images/red_ball.png"
    scale = 0.1

    def __init__(self, player_location, start_location):
        super().__init__(self.image, self.scale)
        self.position = start_location
        self.target_x = player_location[0]
        self.target_y = player_location[1]
        self.start_location = start_location

    def move(self):   
        start_x = self.start_location[0]
        start_y = self.start_location[1]
        
        delta_x = self.target_x - start_x
        delta_y = self.target_y - start_y

        magnitude = abs(sqrt((delta_x * delta_x) + (delta_y * delta_y)))

        unit_x = delta_x / magnitude
        unit_y = delta_y / magnitude

        self.change_x = unit_x * SEAL_PROJECTILE_SPEED
        self.change_y = unit_y * SEAL_PROJECTILE_SPEED

        self.center_x += self.change_x
        self.center_y += self.change_y