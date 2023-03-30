"""
Sprite Follow Player 2

This calculates a 'vector' towards the player and randomly updates it based
on the player's location. This is a bit more complex, but more interesting
way of following the player.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_follow_simple_2
"""

from cmath import sin, sqrt
from helper_functions import distance
import random
import arcade
import math
import os
from pygame import mixer
import pygame

from enemies import *
from projectiles import *


# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COW = 0.3
SPRITE_SCALING_LARGE_BANANA = 0.15
SPRITE_SCALING_SMALL_BANANA = 0.05

# Starting number of cows
COW_COUNT = 5

# GUI Values
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Follow Player Simple Example 2"

# Speed Constants
SPRITE_SPEED = 3
PLAYER_SPEED = 5
UPDATES_PER_FRAME = 5

# Player stats constants
STARTING_PLAYER_HEALTH = 100

# The number of smaller objects the splinter projectile creates upon impact with an enemy
SPLINTER_BOUNCES = 5

# Used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

UPGRADE_TYPES = ["Basic", "Splinter", "Rapid_Fire"]

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]
class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = SPRITE_SCALING_PLAYER

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        # main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        #main_path = ":resources:images/animated_characters/zombie/zombie"
        #main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]


class Upgrade(arcade.Sprite):
    type = None
    def __init__(self, image, scale, type):
        super().__init__(image, scale)
        self.type = type

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.projectile_list = None
        self.enemy_projectile_list = None
        self.upgrade_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.weapon_selected = None
        self.health = None
        self.bombs_left = None
        self.last_fire = None

        # Set up the key presses
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        self.frames_since_direction_change = 0

        # Set mouse location
        self.mouse_x = 0
        self.mouse_y = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        # Initalize timer
        self.time = None

        # Initialize sound
        mixer.init()
        pygame.mixer.init()

        arcade.set_background_color(arcade.color.AMAZON)

        # Plays music
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Game Track.mp3'), loops=-1)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.upgrade_list = arcade.SpriteList()
        self.enemy_projectile_list = arcade.SpriteList()

        # Score
        self.score = 0
        self.weapon_selected = "Basic"
        self.health = STARTING_PLAYER_HEALTH
        self.bombs_left = 2
        self.last_fire = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 300
        self.player_list.append(self.player_sprite)

        self.time = 0

        # Create the cows
        for i in range(COW_COUNT):
            # Create the cow instance
            cow = Cow()

            # Position the cow
            cow.center_x = random.randrange(SCREEN_WIDTH)
            cow.center_y = random.randrange(SCREEN_HEIGHT)

            if distance([cow.center_x, cow.center_y], self.player_sprite.position) > 50:
                self.enemy_list.append(cow)



    def banana_bomb(self, start_position):
        if self.bombs_left > 0:
            self.bombs_left -= 1
            for angle in range(0, 12, 1):
                start_x = start_position[0]
                start_y = start_position[1]
                projectile = Basic_Projectile(start_x + math.cos(angle/2), start_y + math.sin(angle/2), start_position)
                self.projectile_list.append(projectile)

    def generate_upgrades(self):
        # Randomly generating upgrades
        if random.randrange(700) == 0 and len(self.upgrade_list) < 2:
            upgrade_type = UPGRADE_TYPES[random.randrange(len(UPGRADE_TYPES))]
            if upgrade_type == "Splinter":
                upgrade = Upgrade("images/banana_item.png", SPRITE_SCALING_LARGE_BANANA, "Splinter")

            elif upgrade_type == "Basic":
                upgrade = Upgrade("images/carrot_item.png", SPRITE_SCALING_CARROT, "Basic")

            upgrade.center_x = random.randrange(SCREEN_WIDTH)
            upgrade.center_y = random.randrange(SCREEN_HEIGHT)

            # Adding the upgrade to upgrad_list
            self.upgrade_list.append(upgrade)

    def generate_enemies(self):
        # Randomly generating Cows
        if random.randrange(60) == 0:
            cow = Cow()
            cow.center_x = random.randrange(SCREEN_WIDTH)
            cow.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the cow to the lists if not super close to player
            if distance([cow.center_x, cow.center_y], self.player_sprite.position) > 50:
                self.enemy_list.append(cow)

        # Randomly generating Seals
        if self.time > 10 and random.randrange(500) == 0:
                seal = Seal()
                seal.center_x = random.randrange(SCREEN_WIDTH)
                seal.center_y = random.randrange(SCREEN_HEIGHT)
                self.enemy_list.append(seal)

        # Randomly generating Seals
        if self.time > 20 and random.randrange(900) == 0:
                bull = Bull()
                bull.center_x = random.randrange(SCREEN_WIDTH)
                bull.center_y = random.randrange(SCREEN_HEIGHT)
                self.enemy_list.append(bull)

    def fire_seal_projectiles(self):
        for enemy in self.enemy_list:
            if type(enemy) is Seal:
                time_since_fire = self.time - enemy.last_fire_time
                if time_since_fire > 4:
                    self.enemy_projectile_list.append(enemy.fire_ball(self.player_sprite.position))
                    enemy.last_fire_time = self.time

    def check_all_collisions(self):
              # Checking sprite collisions
        hit_list = arcade.SpriteList()
        # Checking if a projectile hit a cow
        for cow in self.enemy_list:
            if len(arcade.check_for_collision_with_list(cow, self.projectile_list)) > 0:
                hit_list.append(cow)
                cow.health -= 1
        # Checking if a player has been hit by an enemy
        player_hit = len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0
        if player_hit and self.health > 0:
            self.health -= 1
            arcade.set_background_color(arcade.color.AMERICAN_ROSE)
        else:
            arcade.set_background_color(arcade.color.AMAZON)

        # Checking for projectile collisions and deleting the projectiles if they have collided
        for projectile in self.projectile_list:
           if len(arcade.check_for_collision_with_list(projectile, hit_list)) > 0:
               projectile.kill()

               # Special case with the splinter projectile -> creates more moving in random directions
               if type(projectile) is Splinter_Projectile:
                    for i in range (projectile.splinters_left):
                        random_x = random.randrange(-100, 100)
                        random_y = random.randrange(-100, 100)

                        target_x = projectile.center_x + random_x
                        target_y= projectile.center_y + random_y

                        splinter_projectile = Splinter_Projectile("images/banana.png", SPRITE_SCALING_SMALL_BANANA, target_x, target_y, projectile.position, 0)
                        self.projectile_list.append(splinter_projectile)
        for projectile in self.enemy_projectile_list:
           if len(arcade.check_for_collision_with_list(projectile, self.player_list)) > 0:
               self.health -= 10
               arcade.set_background_color(arcade.color.AMERICAN_ROSE)
               projectile.kill()


        # Check for collisions between player and upgrade
        for upgrade in self.upgrade_list:
            if arcade.check_for_collision(upgrade, self.player_sprite):
                self.weapon_selected = upgrade.type
                upgrade.kill()

        # Loop through each colliding sprite, remove it, and add to the score.
        for enemy in hit_list:
            if enemy.health <= 0:
                enemy.kill()
                self.score += 1
    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.enemy_list.draw()
        self.player_list.draw()
        self.projectile_list.draw()
        self.upgrade_list.draw()
        self.enemy_projectile_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text("Weapon Selected: " + self.weapon_selected, 550,20, arcade.color.WHITE, 14)
        arcade.draw_text("Health: " + self.health.__str__(), 10, 550, arcade.color.RED, 14)

        # Basic loss condition. TODO do this with scenes instead
        if self.health <= 0:
            self.clear()
            arcade.draw_text("YOU LOSE", 300, 300, arcade.color.RED, 30)

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.w_pressed and not self.s_pressed:
            self.player_sprite.change_y += PLAYER_SPEED
        elif self.s_pressed and not self.w_pressed:
            self.player_sprite.change_y += -PLAYER_SPEED
        if self.a_pressed and not self.d_pressed:
            self.player_sprite.change_x += -PLAYER_SPEED
        elif self.d_pressed and not self.a_pressed:
            self.player_sprite.change_x += PLAYER_SPEED


    def on_update(self, delta_time):
        # Updating time and the player sprite
        self.time += delta_time
        self.player_list.update()

        # Update the players animation
        self.player_list.update_animation()

        self.check_all_collisions()

        min_distance = 1000000
        for enemy in self.enemy_list:
            if distance(self.player_sprite.position, enemy.position) < min_distance:
                min_distance = distance(self.player_sprite.position, enemy.position)
        if  min_distance > 300 and self.health < 100:
            self.health += 1

        for enemy in self.enemy_list:
            if type(enemy) is Cow:
                enemy.follow_sprite(self.player_sprite)
            if type(enemy) is Seal:
                enemy.follow_sprite(self.enemy_list[random.randrange(len(self.enemy_list))])
            if type(enemy) is Bull:
                enemy.charge(self.player_sprite)



        # Making every projectile move towards target
        for projectile in self.projectile_list:
            projectile.move()

        for projectile in self.enemy_projectile_list:
            projectile.move()

        # Spawning enemies
        self.generate_enemies()

        # Creates upgrades
        self.generate_upgrades()

        self.fire_seal_projectiles()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            self.w_pressed = True
            self.update_player_speed()
        elif key == arcade.key.A:
            self.a_pressed = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.s_pressed = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.d_pressed = True
            self.update_player_speed()

        if key == arcade.key.SPACE:
            weapon_delta_time = self.time - self.last_fire
            if self.weapon_selected == "Basic" and weapon_delta_time > 0.3 :
                projectile = Basic_Projectile(self.mouse_x, self.mouse_y, self.player_sprite.position)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('pop.mp3'))
            elif self.weapon_selected == "Splinter" and weapon_delta_time > 1:
                projectile = Splinter_Projectile("images/banana.png", SPRITE_SCALING_LARGE_BANANA, self.mouse_x, self.mouse_y, self.player_sprite.position, SPLINTER_BOUNCES)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('throw.mp3'))
            self.projectile_list.append(projectile)
            self.last_fire = self.time

        if key == arcade.key.M:
            pygame.mixer.Channel(1).pause()

        if key == arcade.key.P:
            self.banana_bomb(self.player_sprite.position)
        
        if key == arcade.key.ENTER and self.health == 0:
            self.__init__()
            self.setup()

        if key == arcade.key.ESCAPE:
            print("Program terminated manually!")
            arcade.exit()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y


    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = False
            self.update_player_speed()
        elif key == arcade.key.A:
            self.a_pressed = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.s_pressed = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.d_pressed = False
            self.update_player_speed()

def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
