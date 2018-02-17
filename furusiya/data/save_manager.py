import shelve


class SaveManager:
    def __init__(self, game):
        self.game = game

    def save(self):
        # open a new empty shelve (possibly overwriting an old one) to write the game data
        with shelve.open('savegame', 'n') as savefile:
            for attr_name, value in self.game.__dict__.items():
                if attr_name.startswith('__') or attr_name in self.game._dont_pickle:
                    continue
                savefile[attr_name] = value

    def load(self):
        # open the previously saved shelve and load the game data
        with shelve.open('savegame', 'r') as savefile:
            for attr_name, value in savefile.items():
                setattr(self.game, attr_name, value)
