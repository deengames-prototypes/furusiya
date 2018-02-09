import colors
from model.config import config
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

    def move_or_attack(self, dx, dy):
        # TODO: Should this be part of the Fighter component?
        # the coordinates the player is moving to/attacking
        x = self.x + dx
        y = self.y + dy

        # try to find an attackable object there
        for obj in Game.area_map.get_entities_on(x, y):
            if obj.has_component(Fighter):
                target = obj
                break
        else:
            self.move(dx, dy)
            Game.renderer.recompute_fov = True
            return

        self.get_component(Fighter).attack(target)

    def _xp_next_level(self):
        return 2 ** (self.level + 1) * config.data.player.expRequiredBase

    def gain_xp(self, amount):
        # TODO: make this a component and eventually remove this class?
        fighter = self.get_component(Fighter)

        fighter.xp += amount
        # XP doubles every level. 40, 80, 160, ...
        # First level = after four orcs. Yeah, low standards.
        # DRY ya'ne
        while fighter.xp >= self._xp_next_level():
            self.level += 1
            self.stats_points += config.data.player.statsPointsOnLevelUp
            message("You are now level {}!".format(self.level))
            fighter.heal(fighter.max_hp)
