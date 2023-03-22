import random
import arcade
import math
import projectiles

COW_SPEED = 0.8
SEAL_SPEED = 0.2
BULL_SPEED = 10

SPRITE_SCALING_COW = 0.3
SPRITE_SCALING_SEAL = 0.4
SPRITE_SCALING_BULL = 0.4



class Enemy(arcade.Sprite):
    """
    This class represents the cows on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """
    # Fields of Enemy class
    health = None
    move_speed = 0


    # Constructor
    def __init__(self, image, scale):
        super().__init__(image, scale)

    # Called to move the cow in the direction of the player
    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(30) == 0:

            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # if x_diff <= 500 and y_diff <= 500:
                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * self.move_speed
            self.change_y = math.sin(angle) * self.move_speed

class Cow(Enemy):
    health = 1
    def __init__(self):
        self.move_speed = COW_SPEED
        super().__init__("images/cow.png", SPRITE_SCALING_COW)

class Seal(Enemy):
    health = 1
    last_fire_time = 0
    def __init__(self):
        self.move_speed = SEAL_SPEED
        super().__init__("images/seal.png", SPRITE_SCALING_SEAL)
    
    def fire_ball(self, player_location):
        ball = projectiles.Seal_Projectile(player_location, self.position)
        return ball
    
class Bull(Enemy):
    health = 3
    charge_left = 0
    charging = False
    def __init__(self):
        self.move_speed = BULL_SPEED
        super().__init__("images/bull.png", SPRITE_SCALING_BULL)
    
    def charge(self, target_sprite):
        if self.charge_left >= 200 and not self.charging:
            self.charging = True
        
        if self.charge_left > 0 and self.charging:
            self.follow_sprite(target_sprite)
            self.charge_left -= 3
        else:
            self.charging = False
            self.charge_left += 1
