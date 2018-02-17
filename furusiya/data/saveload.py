import shelve


class SaveLoad:
    def __init__(self, game):
        self.game = game

    def save(self):
        # open a new empty shelve (possibly overwriting an old one) to write the game data
        with shelve.open('savegame', 'n') as savefile:
            savefile['tiles'] = self.game.area_map.tiles
            savefile['entities'] = self.game.area_map.entities
            savefile['player_index'] = self.game.area_map.entities.index(self.game.player)  # index of player in entities list
            savefile['inventory'] = self.game.inventory
            savefile['game_msgs'] = self.game.game_msgs
            savefile['game_state'] = self.game.game_state

    def load(self):
        # open the previously saved shelve and load the game data
        with shelve.open('savegame', 'r') as savefile:
            self.game.area_map.tiles = savefile['tiles']
            self.game.area_map.width = len(self.game.area_map.tiles)
            self.game.area_map.height = len(self.game.area_map.tiles[0])
            self.game.area_map.entities = savefile['entities']
            self.game.player = self.game.area_map.entities[savefile['player_index']]  # get index of player in objects list and access it
            self.game.inventory = savefile['inventory']
            self.game.game_msgs = savefile['game_msgs']
            self.game.game_state = savefile['game_state']