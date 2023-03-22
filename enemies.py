import random
import arcade
import math

COW_SPEED = 0.8


class Cow(arcade.Sprite):
    """
    This class represents the cows on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

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

            if x_diff <= 500 and y_diff <= 500:
                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                self.change_x = math.cos(angle) * COW_SPEED
                self.change_y = math.sin(angle) * COW_SPEED
