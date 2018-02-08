import colors
import config
import model.weapons
from death_functions import player_death
from main_interface import Game, message
from model.components.fighter import Fighter
from model.entities.game_object import GameObject


class Player(GameObject):
    def __init__(self):
        data = config.data.player
        super().__init__(0, 0, '@', 'player', colors.white, blocks=True)

        # Turn a name like "Sword" into the actual class instance
        weapon_name = data.startingWeapon
        weapon_init = getattr(model.weapons, weapon_name)

        self.set_component(
            Fighter(
                owner=self,
                hp=data.startingHealth,
                defense=data.startingDefense,
                power=data.startingPower,
                xp=0,
                weapon=weapon_init(self),
                death_function=player_death
            )
        )

        Game.draw_bowsight = False

        self.level = 1
        self.stats_points = 0
        self.arrows = config.data.player.startingArrows

        print("You hold your wicked-looking {} at the ready!".format(weapon_name))

    def gain_xp(self, amount):
        fighter = self.get_component(Fighter)

        fighter.xp += amount
        # XP doubles every level. 40, 80, 160, ...
        # First level = after four orcs. Yeah, low standards.
        xp_next_level = 2 ** (self.level + 1) * 10
        # DRY ya'ne
        while fighter.xp >= xp_next_level:
            self.level += 1
            self.stats_points += config.data.player.statsPointsOnLevelUp
            xp_next_level = 2 ** (self.level + 1) * config.data.player.expRequiredBase
            message("You are now level {}!".format(self.level))
            fighter.heal(fighter.max_hp)
