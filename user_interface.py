import arcade

# GUI Values
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# UI CONSTANTS
HEALTH_BAR_LEFT = 10
HEALTH_BAR_RIGHT = 150
HEALTH_BAR_TOP = 590
HEALTH_BAR_BOTTOM = 565
WEAPON_BOX_SIZE = 75
UI_FONT = 'fonts/joystix.ttf'
UI_FONT_SIZE = 18

# UI colors
UI_BG_COLOR = arcade.color.BLACK
UI_BORDER_COLOR = arcade.color.BLACK
HEALTH_COLOR = arcade.color.RED
UI_BORDER_COLOR_ACTIVE = arcade.color.TUSCAN_BROWN
TEXT_COLOR = arcade.color.WHEAT

import arcade


def show_health_bar(current, max_amount, color):
    # draw bg
    arcade.draw_lrtb_rectangle_filled(HEALTH_BAR_LEFT, HEALTH_BAR_RIGHT,
                                      HEALTH_BAR_TOP, HEALTH_BAR_BOTTOM, UI_BG_COLOR)

    # converting stat to pixel
    health_bar_width = HEALTH_BAR_RIGHT - HEALTH_BAR_LEFT
    ratio = current / max_amount
    current_width = health_bar_width * ratio
    updated_bar_right = current_width + HEALTH_BAR_LEFT

    # drawing the bar
    arcade.draw_lrtb_rectangle_filled(HEALTH_BAR_LEFT, updated_bar_right, HEALTH_BAR_TOP, HEALTH_BAR_BOTTOM,
                                      color)
    arcade.draw_lrtb_rectangle_outline(10, updated_bar_right, HEALTH_BAR_TOP - 1, HEALTH_BAR_BOTTOM + 1,
                                       UI_BORDER_COLOR, 3)

def show_score(score):
    text_surf = f"Score: {score}"
    x = SCREEN_WIDTH - 200
    y = 20
    text_rect = arcade.draw_text(text_surf, x, y, TEXT_COLOR, anchor_x="right", anchor_y="bottom",
                                 font_size=UI_FONT_SIZE, font_name=UI_FONT, align="right", bold=False,
                                 italic=False, width=10)

def selection_box(x, y):
    arcade.draw_rectangle_filled(x, y, WEAPON_BOX_SIZE, WEAPON_BOX_SIZE, UI_BG_COLOR)
    arcade.draw_rectangle_outline(x, y, WEAPON_BOX_SIZE, WEAPON_BOX_SIZE, UI_BORDER_COLOR_ACTIVE)

def weapon_overlay(weapon_graphics, center_x, center_y, weapon_index):
    selection_box(center_x, center_y)
    weapon_img = weapon_graphics[weapon_index]
    arcade.draw_texture_rectangle(center_x, center_y, WEAPON_BOX_SIZE, WEAPON_BOX_SIZE, weapon_img)


