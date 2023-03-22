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

from enemies import *

#from itsdangerous import NoneAlgorithm

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COW = 0.3
SPRITE_SCALING_CARROT = 0.05
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
COW_SPEED = 0.8
BASIC_PROJECTILE_SPEED = 4

# Player stats constants
STARTING_PLAYER_HEALTH = 100


# The number of smaller objects the splinter projectile creates upon impact with an enemy
SPLINTER_BOUNCES = 5

# Used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

UPGRADE_TYPES = ["Basic", "Splinter"]

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


# THis is the basic enemy class. We are calling it cow for now but it is just an enemy that takes 1 hit and follows the player
# Basic projectile class. Shoots in the direction of the mouse starting at the player
class Basic_Projectile(arcade.Sprite):
    target_x = None
    target_y = None
    player_location = (0,0)

    def __init__(self, image, scale, target_x, target_y, player_location):
        super().__init__(image, scale)
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
        self.cow_list = None
        self.projectile_list = None
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

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.cow_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.upgrade_list = arcade.SpriteList()

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
            cow = Cow("cow.png", SPRITE_SCALING_COW)

            # Position the cow
            cow.center_x = random.randrange(SCREEN_WIDTH)
            cow.center_y = random.randrange(SCREEN_HEIGHT)

            if distance([cow.center_x, cow.center_y], self.player_sprite.position) > 50:
                self.cow_list.append(cow)
        
            

    def banana_bomb(self, start_position):
        if self.bombs_left > 0:
            self.bombs_left -= 1
            for angle in range(0, 12, 1):
                start_x = start_position[0]
                start_y = start_position[1]
                projectile = Basic_Projectile("banana.png", SPRITE_SCALING_LARGE_BANANA, start_x + math.cos(angle/2), start_y + math.sin(angle/2), start_position)
                self.projectile_list.append(projectile)

    def on_draw(self):
        """ Draw everything """
        self.clear()            
        self.cow_list.draw()
        self.player_list.draw()
        self.projectile_list.draw()
        self.upgrade_list.draw()

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
        self.time += delta_time
        """ Movement and game logic """
        self.player_list.update()

        # Update the players animation
        self.player_list.update_animation()
    
        for cow in self.cow_list:
            cow.follow_sprite(self.player_sprite)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.SpriteList()
        for cow in self.cow_list:
            if len(arcade.check_for_collision_with_list(cow, self.projectile_list)) > 0:
                hit_list.append(cow)
        
        player_hit = len(arcade.check_for_collision_with_list(self.player_sprite, self.cow_list)) > 0
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

                        splinter_projectile = Splinter_Projectile("banana.png", SPRITE_SCALING_SMALL_BANANA, target_x, target_y, projectile.position, 0)
                        self.projectile_list.append(splinter_projectile)

        # Check for collisions between player and upgrade
        for upgrade in self.upgrade_list:
            if arcade.check_for_collision(upgrade, self.player_sprite):
                self.weapon_selected = upgrade.type
                upgrade.kill()



        # Loop through each colliding sprite, remove it, and add to the score.
        for cow in hit_list:
            cow.kill()
            self.score += 1
        
        # Making every projectile move towards target
        for projectile in self.projectile_list:
            projectile.move()
            

        # Randomly generating Cows
        if random.randrange(50) == 0:
            cow = Cow("cow.png", SPRITE_SCALING_COW)
            cow.center_x = random.randrange(SCREEN_WIDTH)
            cow.center_y = random.randrange(SCREEN_HEIGHT)
            
            # Add the cow to the lists if not super close to player
            if distance([cow.center_x, cow.center_y], self.player_sprite.position) > 50:
                self.cow_list.append(cow)

        # Randomly generating upgrades
        if random.randrange(700) == 0:
            upgrade_type = UPGRADE_TYPES[random.randrange(len(UPGRADE_TYPES))]
            if upgrade_type == "Splinter":
                upgrade = Upgrade("banana_item.png", SPRITE_SCALING_LARGE_BANANA, "Splinter")
                
            elif upgrade_type == "Basic":
                upgrade = Upgrade("carrot_item.png", SPRITE_SCALING_CARROT, "Basic")
            
            upgrade.center_x = random.randrange(SCREEN_WIDTH)
            upgrade.center_y = random.randrange(SCREEN_HEIGHT)

            # Adding the upgrade to upgrad_list
            self.upgrade_list.append(upgrade)

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
                projectile = Basic_Projectile("carrot.png", SPRITE_SCALING_CARROT, self.mouse_x, self.mouse_y, self.player_sprite.position)
            elif self.weapon_selected == "Splinter" and weapon_delta_time > 1:
                projectile = Splinter_Projectile("banana.png", SPRITE_SCALING_LARGE_BANANA, self.mouse_x, self.mouse_y, self.player_sprite.position, SPLINTER_BOUNCES)
            self.projectile_list.append(projectile)
            
            self.last_fire = self.time


        if key == arcade.key.P:
            self.banana_bomb(self.player_sprite.position)
        
        if key == arcade.key.ENTER and self.health == 0:
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
