#!/usr/bin/env python
import tcod
 
# ######################################################################
# Global Game Settings
# ######################################################################
# Windows Controls
FULLSCREEN = False
SCREEN_WIDTH = 80  # characters wide
SCREEN_HEIGHT = 50  # characters tall
LIMIT_FPS = 20  # 20 frames-per-second maximum
# Game Controls
TURN_BASED = True  # turn-based game
 
player_x = 0
player_y = 0
 
def initialize_game():
    global player_x, player_y
    
    # Setup player
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT // 2
 
    # Setup Font
    font_filename = 'arial10x10.png'
    tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
 
    # Initialize screen
    title = 'Python 3 + Libtcod tutorial'
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)
 
    # Set FPS
    tcod.sys_set_fps(LIMIT_FPS)
 
 
# ######################################################################
# User Input
# ######################################################################
def get_key_event(turn_based=None):
    if turn_based:
        # Turn-based game play; wait for a key stroke
        key = tcod.console_wait_for_keypress(True)
    else:
        # Real-time game play; don't wait for a player's key stroke
        key = tcod.console_check_for_keypress()
    return key
 
 
def handle_keys():
    global player_x, player_y
 
    key = get_key_event(TURN_BASED)
 
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
 
    elif key.vk == tcod.KEY_ESCAPE:
        return True  # exit game
 
    # movement keys
    if tcod.console_is_key_pressed(tcod.KEY_UP) or key.c == ord('w'):
        player_y -= 1
 
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN) or key.c == ord('s'):
        player_y += 1
 
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT) or key.c == ord('a'):
        player_x -= 1
 
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT) or key.c == ord('d'):
        player_x += 1
 
 
#############################################
# Main Game Loop
#############################################
 
 
def main():
    initialize_game()
    global player_x, player_y
 
    exit_game = False
    while not tcod.console_is_window_closed() and not exit_game:
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_put_char(0, player_x, player_y, '@', tcod.BKGND_NONE)
        tcod.console_flush()
        tcod.console_put_char(0, player_x, player_y, ' ', tcod.BKGND_NONE)
 
        exit_game = handle_keys()
 
 
main()