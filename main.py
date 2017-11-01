import libtcodpy as tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

font_path = 'arial10x10.png'
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD  # the layout may need to change with a different font file
tcod.console_set_custom_font(font_path, font_flags)

window_title = 'Python 3 libtcod tutorial'
fullscreen = False
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, fullscreen)

#while not tcod.console_is_window_closed():
tcod.console_put_char(0, 1, 1, '@', tcod.BKGND_NONE)
tcod.console_flush()

input("Press enter key to close")
