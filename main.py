from cmath import sin, sqrt
import time
import os

from helper_functions import *
from enemies import *
from projectiles import *
from user_interface import *


# --- Constants ---
SPRITE_SCALING_PLAYER = 0.8
SPRITE_SCALING_COW = 0.3
SPRITE_SCALING_LARGE_BANANA = 0.15
SPRITE_SCALING_SMALL_BANANA = 0.05
SPRITE_SCALING_WEAPON = 0.15
SPRITE_SCALING_WALL = 0.5

# Starting number of cows
COW_COUNT = 5

# GUI Values
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "CS 205 Final Project"

# Speed Constants
SPRITE_SPEED = 3
PLAYER_SPEED = 2.2
UPDATES_PER_FRAME = 7

# Player stats constants
STARTING_PLAYER_HEALTH = 100

# The number of smaller objects the splinter projectile creates upon impact with an enemy
SPLINTER_BOUNCES = 5

# Used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

UPGRADE_TYPES = ["Basic", "Splinter", "Boomerang"]

WEAPON_EQUIPPED_TEXTURES = {
    "Basic": "images/carrot_gun.png",
    "Splinter": "images/banana_gun.png",
    "Boomerang": "images/yoyo.png"
}

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

        # Default to face-down
        self.character_face_direction = "down"

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = SPRITE_SCALING_PLAYER

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # Damage Timer/Cooldown for Player
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 0.2
        self.health = STARTING_PLAYER_HEALTH

        # Initialize flicker variables
        self.flicker_frames = 0
        self.flicker_duration = 0  # in seconds
        self.flicker_alpha = 255

        # Images from Kenney.nl's Sokoban Pack
        main_path = "images/littlePlayer"

        # Load textures for idle standing
        self.idle_texture = arcade.load_texture(f"{main_path}_idle.png")

        # Load textures for walking left and right
        self.walk_textures_LR = []
        for i in range(3):
            texture = load_texture_pair(f"{main_path}_walkLR_{i}.png")
            self.walk_textures_LR.append(texture)

        # Load textures for walking down
        self.walk_textures_down = []
        for i in range(3):
            texture = arcade.load_texture(f"{main_path}_down_{i}.png")
            self.walk_textures_down.append(texture)

        # Load textures for walking up
        self.walk_textures_up = []
        for i in range(3):
            texture = arcade.load_texture(f"{main_path}_up_{i}.png")
            self.walk_textures_up.append(texture)

    def flicker(self, duration):
        self.flicker_duration = duration
        self.flicker_frames = int(self.flicker_duration / (1 / 60))
        self.flicker_alpha = 255

    def damage_player(self, amount):
        if self.vulnerable:
            self.health -= amount
            self.flicker(duration=0.1)
            self.vulnerable = False
            self.hurt_time = time.time()
            if self.health <= 0:
                self.kill()

            # Hurt sounds, randomly generated
            randint = random.randint(1, 9)
            pygame.mixer.Channel(3).set_volume(0.2)
            if randint == 1:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt1.mp3'))
            elif randint == 2:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt2.mp3'))
            elif randint == 3:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt3.mp3'))
            elif randint == 4:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt4.mp3'))
            elif randint == 5:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt5.mp3'))
            elif randint == 6:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt6.mp3'))
            elif randint == 7:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt7.mp3'))
            elif randint == 8:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt8.mp3'))
            elif randint == 9:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds/hurt9.mp3'))

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and (self.character_face_direction == "right" or self.character_face_direction == "down"
                                  or self.character_face_direction == "up"):
            self.character_face_direction = "left"
        elif self.change_x > 0 and (self.character_face_direction == "left" or self.character_face_direction == "down"
                                    or self.character_face_direction == "up"):
            self.character_face_direction = "right"

        # Figure out if we need to flip face down or up
        if self.change_y < 0 and (self.character_face_direction == "up" or self.character_face_direction == "left"
                                  or self.character_face_direction == "right"):
            self.character_face_direction = "down"
        elif self.change_y > 0 and (self.character_face_direction == "down" or self.character_face_direction == "left"
                                    or self.character_face_direction == "right"):
            self.character_face_direction = "up"

        # Walking Animations
        if self.character_face_direction == "right":
            # Idle Animation (Right)
            if self.change_x == 0 and self.change_y == 0:
                self.texture = self.walk_textures_LR[0][0]
            else:
                # Walking right animation
                self.cur_texture += 1
                if self.cur_texture > 2 * UPDATES_PER_FRAME:
                    self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                self.texture = self.walk_textures_LR[frame][0]

        if self.character_face_direction == "left":
            # Idle Animation (Left)
            if self.change_x == 0 and self.change_y == 0:
                self.texture = self.walk_textures_LR[0][1]
            else:
                # Walking left animation
                self.cur_texture += 1
                if self.cur_texture > 2 * UPDATES_PER_FRAME:
                    self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                self.texture = self.walk_textures_LR[frame][1]

        if self.character_face_direction == "down":
            # Idle Animation (Down)
            if self.change_x == 0 and self.change_y == 0:
                self.texture = self.walk_textures_down[1]
            else:
                # Walking down animation
                self.cur_texture += 1
                if self.cur_texture > 2 * UPDATES_PER_FRAME:
                    self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                self.texture = self.walk_textures_down[frame]

        if self.character_face_direction == "up":
            # Idle Animation (Up)
            if self.change_x == 0 and self.change_y == 0:
                self.texture = self.walk_textures_up[1]
            else:
                # Walking up animation
                self.cur_texture += 1
                if self.cur_texture > 2 * UPDATES_PER_FRAME:
                    self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                self.texture = self.walk_textures_up[frame]

class WeaponEquipped(arcade.Sprite):
    def __init__(self, image, scale):
        # Set up parent class
        super().__init__(image, scale)

        # Default to face-down
        self.character_face_direction = "down"

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # Load textures for weapon facing left and right
        self.weapon_textures_LR = []
        texture = load_texture_pair(image)
        self.weapon_textures_LR.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and (self.character_face_direction == "right" or self.character_face_direction == "down"
                                  or self.character_face_direction == "up"):
            self.character_face_direction = "left"
        elif self.change_x > 0 and (self.character_face_direction == "left" or self.character_face_direction == "down"
                                    or self.character_face_direction == "up"):
            self.character_face_direction = "right"

        # Figure out if we need to flip face down or up
        if self.change_y < 0 and (self.character_face_direction == "up" or self.character_face_direction == "left"
                                  or self.character_face_direction == "right"):
            self.character_face_direction = "down"
        elif self.change_y > 0 and (self.character_face_direction == "down" or self.character_face_direction == "left"
                                    or self.character_face_direction == "right"):
            self.character_face_direction = "up"

        # Movement Animations
        if self.character_face_direction == "right":
            self.texture = self.weapon_textures_LR[0][1]
            # Ensure the sprite appears
            self.alpha = 255

        if self.character_face_direction == "left":
            self.texture = self.weapon_textures_LR[0][0]
            self.alpha = 255

        if self.character_face_direction == "down":
            # Make the sprite disappear
            self.alpha = 0

        if self.character_face_direction == "up":
            self.alpha = 0


class Upgrade(arcade.Sprite):
    type = None

    def __init__(self, image, scale, type):
        super().__init__(image, scale)
        self.type = type

class MyGame(arcade.Window):

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
        self.weapon_list = None
        self.wall_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.weapon_selected = None
        self.weapon_index = 0
        self.weapon_sprite = None
        self.bombs_left = None
        self.last_fire = None

        # Physics engine to prevent player from colliding with edge walls
        self.physics_engine = None

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

        # Set up the UI
        self.font = arcade.load_font(UI_FONT)
        self.weapon_graphics = None

        # Initalize timer
        self.time = None

        # Initialize sound & play music
        mixer.init()
        pygame.mixer.init()
        pygame.mixer.Channel(6).play(pygame.mixer.Sound('sounds/Game Track.mp3'), loops=-1)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.upgrade_list = arcade.SpriteList()
        self.enemy_projectile_list = arcade.SpriteList()
        self.weapon_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Score
        self.score = 0
        self.weapon_selected = "Basic"
        self.bombs_left = 2
        self.last_fire = 0

        # Set up the player
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 300
        self.player_list.append(self.player_sprite)

        # Set up the players weapon sprite
        self.weapon_sprite = WeaponEquipped(WEAPON_EQUIPPED_TEXTURES["Basic"], SPRITE_SCALING_WEAPON)
        self.weapon_list.append(self.weapon_sprite)

        self.time = 0

        # Drawing the walls for the bottom and top
        for i in range(20):
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING_WALL)
            wall.center_x = i*64
            wall.center_y = -25
            self.wall_list.append(wall)
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING_WALL)
            wall.center_x = i*64
            wall.center_y = 625
            self.wall_list.append(wall)
        for i in range(10):
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING_WALL)
            wall.center_x = -25
            wall.center_y = i*64
            self.wall_list.append(wall)
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING_WALL)
            wall.center_x = 825
            wall.center_y = i*64
            self.wall_list.append(wall)

        # Add walls and player to the physics
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # convert weapon dictionary into list
        self.weapon_graphics = []
        for weapon in WEAPON_EQUIPPED_TEXTURES:
            path = WEAPON_EQUIPPED_TEXTURES[weapon]
            weapon = arcade.load_texture(path)
            self.weapon_graphics.append(weapon)

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
                projectile = Basic_Projectile(start_x + math.cos(angle / 2), start_y + math.sin(angle / 2),
                                              start_position)
                self.projectile_list.append(projectile)

    def generate_upgrades(self):
        upgrade = None  # initialize with a default value, this fixes upgrade called before init error
        # Randomly generating upgrades
        if random.randrange(700) == 0 and len(self.upgrade_list) < 2:
            upgrade_type = UPGRADE_TYPES[random.randrange(len(UPGRADE_TYPES))]
            if upgrade_type == "Splinter":
                upgrade = Upgrade("images/banana_item.png", SPRITE_SCALING_LARGE_BANANA, "Splinter")
            elif upgrade_type == "Basic":
                upgrade = Upgrade("images/carrot_item.png", SPRITE_SCALING_CARROT, "Basic")
            elif upgrade_type == "Boomerang":
                upgrade = Upgrade("images/yoyo_upgrade.png", 0.15, "Boomerang")

            if upgrade:  # check if upgrade has a value
                upgrade.center_x = random.randrange(SCREEN_WIDTH)
                upgrade.center_y = random.randrange(SCREEN_HEIGHT)

                # Adding the upgrade to upgrade_list
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

    def wave_value(self):
        value = sin(time.time())
        if value >= 0:
            return 255
        else:
            return 0

    def cooldowns(self):
        current_time = time.time()
        if not self.player_sprite.vulnerable:
            if current_time - self.player_sprite.hurt_time >= self.player_sprite.invulnerability_duration:
                self.player_sprite.vulnerable = True

    def check_all_collisions(self):
        # Checking sprite collisions
        hit_list = arcade.SpriteList()
        # Checking if a projectile hit a cow
        for enemy in self.enemy_list:
            if len(arcade.check_for_collision_with_list(enemy, self.projectile_list)) > 0:
                hit_list.append(enemy)
                enemy.health -= 1
        # Checking if a player has been hit by an enemy
        player_hit = len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0
        if player_hit and self.player_sprite.health > 0:
            self.player_sprite.damage_player(3)
            arcade.set_background_color(arcade.color.RUBY)
        else:
            arcade.set_background_color(arcade.color.AMAZON)

        # Checking for projectile collisions and deleting the projectiles if they have collided
        for projectile in self.projectile_list:
            if len(arcade.check_for_collision_with_list(projectile, hit_list)) > 0:
                if type(projectile) is not Boomerang_Projectile:
                    projectile.kill()

                # Special case with the splinter projectile -> creates more moving in random directions
                if type(projectile) is Splinter_Projectile:
                    for i in range(projectile.splinters_left):
                        random_x = random.randrange(-100, 100)
                        random_y = random.randrange(-100, 100)

                        target_x = projectile.center_x + random_x
                        target_y = projectile.center_y + random_y

                        splinter_projectile = Splinter_Projectile("images/banana.png", SPRITE_SCALING_SMALL_BANANA,
                                                                  target_x, target_y, projectile.position, 0)
                        self.projectile_list.append(splinter_projectile)

            if type(projectile) is Boomerang_Projectile:
                projectile.player_location = self.player_sprite.position
                if arcade.check_for_collision(projectile, self.player_sprite) and projectile.time_left <= 0:
                    projectile.kill()

        for projectile in self.enemy_projectile_list:
            if len(arcade.check_for_collision_with_list(projectile, self.player_list)) > 0:
                self.player_sprite.damage_player(10)
                projectile.kill()

        # Check for collisions between player and upgrade
        for upgrade in self.upgrade_list:
            if arcade.check_for_collision(upgrade, self.player_sprite):
                self.weapon_selected = upgrade.type
                if self.weapon_selected == "Splinter":
                    self.weapon_index = 1
                elif self.weapon_selected == "Boomerang":
                    self.weapon_index = 2
                else:
                    self.weapon_index = 0
                upgrade.kill()

        # Loop through each colliding sprite, remove it, and add to the score.
        for enemy in hit_list:
            if enemy.health <= 0:
                enemy.kill()
                self.score += 1

    def draw_UI(self):
        self.show_health_bar(self.player_sprite.health, STARTING_PLAYER_HEALTH, HEALTH_COLOR)
        self.weapon_overlay(45, 45, self.weapon_index)

    def on_draw(self):

        # Draw the main elements
        self.clear()
        self.enemy_list.draw()
        self.player_list.draw()
        self.projectile_list.draw()
        self.upgrade_list.draw()
        self.enemy_projectile_list.draw()
        self.weapon_list.draw()
        self.wall_list.draw()
        show_health_bar(self.player_sprite.health, STARTING_PLAYER_HEALTH, HEALTH_COLOR)
        weapon_overlay(self.weapon_graphics, 45, 45, self.weapon_index)

        # Puts text on the screen for score and health
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 90, arcade.color.WHITE, 13)
        # arcade.draw_text("Weapon Selected: " + self.weapon_selected, 550, 20, arcade.color.WHITE, 14)
        arcade.draw_text("Health: " + self.player_sprite.health.__str__(), 10, 550, arcade.color.RED, 12)

        # Basic loss condition
        if self.player_sprite.health <= 0:
            self.clear()
            arcade.draw_text("YOU LOSE", 270, 350, arcade.color.RED, 40)
            arcade.draw_text("Final Score: " + str(self.score), 240, 250, arcade.color.WHITE, 40)
            pygame.mixer.Channel(0).pause()
            pygame.mixer.Channel(3).pause()
            pygame.mixer.Channel(6).pause()

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        # Add weapon sprite, this ensures the weapon stays with the player
        # We change the weapon position whenever the player position changes
        self.weapon_sprite.change_x = 0
        self.weapon_sprite.change_y = 0

        # Multiple cases to prevent diagonal movement from being faster than up/down/left/right movement
        # Speeds are reduced for diagonal movement by 1/sqrt(2) for each axis per the pythagorean theorem.
        if self.w_pressed and not self.s_pressed:
            if self.w_pressed and self.a_pressed:
                self.player_sprite.change_y += (1 / sqrt(2)) * PLAYER_SPEED
                self.weapon_sprite.change_y += (1 / sqrt(2)) * PLAYER_SPEED
                self.player_sprite.change_x += (1 / sqrt(2)) * -PLAYER_SPEED
                self.weapon_sprite.change_x += (1 / sqrt(2)) * -PLAYER_SPEED
            elif self.w_pressed and self.d_pressed:
                self.player_sprite.change_y += (1 / sqrt(2)) * PLAYER_SPEED
                self.weapon_sprite.change_y += (1 / sqrt(2)) * PLAYER_SPEED
                self.player_sprite.change_x += (1 / sqrt(2)) * PLAYER_SPEED
                self.weapon_sprite.change_x += (1 / sqrt(2)) * PLAYER_SPEED
            else:
                self.player_sprite.change_y += PLAYER_SPEED
                self.weapon_sprite.change_y += PLAYER_SPEED
        elif self.s_pressed and not self.w_pressed:
            if self.s_pressed and self.a_pressed:
                self.player_sprite.change_y += (1 / sqrt(2)) * -PLAYER_SPEED
                self.weapon_sprite.change_y += (1 / sqrt(2)) * -PLAYER_SPEED
                self.player_sprite.change_x += (1 / sqrt(2)) * -PLAYER_SPEED
                self.weapon_sprite.change_x += (1 / sqrt(2)) * -PLAYER_SPEED
            elif self.s_pressed and self.d_pressed:
                self.player_sprite.change_y += (1 / sqrt(2)) * -PLAYER_SPEED
                self.weapon_sprite.change_y += (1 / sqrt(2)) * -PLAYER_SPEED
                self.player_sprite.change_x += (1 / sqrt(2)) * PLAYER_SPEED
                self.weapon_sprite.change_x += (1 / sqrt(2)) * PLAYER_SPEED
            else:
                self.player_sprite.change_y += -PLAYER_SPEED
                self.weapon_sprite.change_y += -PLAYER_SPEED
        elif self.a_pressed and not self.d_pressed:
            self.player_sprite.change_x += -PLAYER_SPEED
            self.weapon_sprite.change_x += -PLAYER_SPEED
        elif self.d_pressed and not self.a_pressed:
            self.player_sprite.change_x += PLAYER_SPEED
            self.weapon_sprite.change_x += PLAYER_SPEED

    def on_update(self, delta_time):

        # Updating time, physics, and the player sprite
        self.time += delta_time
        self.player_list.update()
        self.physics_engine.update()

        # Update the players animation
        self.player_list.update_animation()

        # Update the players weapon animation and position
        self.weapon_list.update_animation()
        self.weapon_sprite.center_x = self.player_sprite.center_x
        self.weapon_sprite.center_y = self.player_sprite.center_y - 12

        # Check for collisions between the player and the upgrade list
        upgrade_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.upgrade_list)

        # Update the player's weapon sprite and weapon_selected based on the upgrades
        for upgrade in upgrade_hit_list:
            if upgrade.type == "Basic":
                self.weapon_sprite.weapon_textures_LR = [load_texture_pair(WEAPON_EQUIPPED_TEXTURES["Basic"])]
            elif upgrade.type == "Splinter":
                self.weapon_sprite.weapon_textures_LR = [load_texture_pair(WEAPON_EQUIPPED_TEXTURES["Splinter"])]
            elif upgrade.type == "Boomerang":
                self.weapon_sprite.weapon_textures_LR = [load_texture_pair(WEAPON_EQUIPPED_TEXTURES["Boomerang"])]

        self.cooldowns()
        self.check_all_collisions()

        # Flicker animation for when player takes damage
        if self.player_sprite.flicker_frames > 0:
            if self.player_sprite.flicker_frames % 2 == 0:
                self.player_sprite.alpha = 0
                self.weapon_sprite.alpha = 0
            else:
                self.player_sprite.alpha = self.player_sprite.flicker_alpha
            self.player_sprite.flicker_alpha = 255 - self.player_sprite.flicker_alpha
            self.player_sprite.flicker_frames -= 1
            if self.player_sprite.flicker_frames == 0:
                self.player_sprite.alpha = 255
                self.weapon_sprite.alpha = 255

        min_distance = 1000000
        for enemy in self.enemy_list:
            if distance(self.player_sprite.position, enemy.position) < min_distance:
                min_distance = distance(self.player_sprite.position, enemy.position)
        if min_distance > 300 and self.player_sprite.health < 70:
            self.player_sprite.health += 1

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
            projectile_created = False  # Initialize the flag as False
            weapon_delta_time = self.time - self.last_fire
            if self.weapon_selected == "Basic" and weapon_delta_time > 0.3:
                projectile = Basic_Projectile(self.mouse_x, self.mouse_y, self.player_sprite.position)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/pop.mp3'))
                projectile_created = True
            elif self.weapon_selected == "Splinter" and weapon_delta_time > 2:
                projectile = Splinter_Projectile("images/banana.png", SPRITE_SCALING_LARGE_BANANA, self.mouse_x,
                                                 self.mouse_y, self.player_sprite.position, SPLINTER_BOUNCES)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/throw.mp3'))
                projectile_created = True
            elif self.weapon_selected == "Boomerang" and weapon_delta_time > 0.7:
                projectile = Boomerang_Projectile(self.mouse_x, self.mouse_y, self.player_sprite.position)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/boomerang.wav'))
                projectile_created = True

            if projectile_created:  # Only append the projectile and perform other operations if the flag is True
                self.projectile_list.append(projectile)
                self.last_fire = self.time

        if key == arcade.key.N:
            pygame.mixer.Channel(6).pause()
        if key == arcade.key.M:
            pygame.mixer.Channel(6).play(pygame.mixer.Sound('sounds/Game Track.mp3'), loops=-1)

        if key == arcade.key.P:
            self.banana_bomb(self.player_sprite.position)

        if key == arcade.key.ENTER and self.player_sprite.health == 0:
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
    # Short delay added to give brief time for initialization, sometimes keyboard inputs don't work without this
    time.sleep(0.05)

    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()