import colors
from model.components.xp import XPComponent
from model.config import config
import model.weapons
from model.helper_functions.death_functions import player_death
from game import Game
from model.components.fighter import Fighter
from model.entities.game_object import GameObject
from model.skills.omnislash import OmniSlash


class Player(GameObject):
    def __init__(self):
        data = config.data.player
        super().__init__(0, 0, '@', 'player', colors.white, blocks=True)

        # Turn a name like "Sword" into the actual class instance
        weapon_name = data.startingWeapon
        weapon_init = getattr(model.weapons, weapon_name)

        Game.fighter_sys.set(
            self, Fighter(
                owner=self,
                hp=data.startingHealth,
                defense=data.startingDefense,
                power=data.startingPower,
                weapon=weapon_init(self),
                death_function=player_death
            )
        )

        Game.xp_sys.set(
            self, XPComponent(
                owner=self,
                xp=0,
                on_level_callback=self.on_level_callback,
                xp_required_base=config.data.player.expRequiredBase
            )
        )

        Game.draw_bowsight = False

        self.arrows = config.data.player.startingArrows

        self.stats_points = 0
        self.mounted = False
        self.moves_while_mounted = 0

        print("You hold your wicked-looking {} at the ready!".format(weapon_name))

    def on_level_callback(self):
        self.stats_points += config.data.player.statsPointsOnLevelUp

    def mount(self, horse):
        if config.data.features.horseIsMountable:
            self.x, self.y = horse.x, horse.y
            self.mounted = True
            horse.is_mounted = True

    def unmount(self, horse):
        if config.data.features.horseIsMountable:
            self.mounted = False
            horse.is_mounted = False

    def _get_health_for_resting(self, max_hp):
        return int(config.data.skills.resting.percent/100 * max_hp)

    def rest(self):
        fighter = Game.fighter_sys.get(self)
        hp_gained = self._get_health_for_resting(fighter.max_hp)
        fighter.heal(hp_gained)
        return 'rested'

    def calculate_turns_to_rest(self):
        fighter = Game.fighter_sys.get(self)
        turns_to_rest = int((fighter.max_hp - fighter.hp) / self._get_health_for_resting(fighter.max_hp))

        return turns_to_rest

    def move_or_attack(self, dx, dy):
        # TODO: Should this be part of the Fighter component?
        # the coordinates the player is moving to/attacking
        x = self.x + dx
        y = self.y + dy

        # try to find an attackable object there
        target = Game.area_map.get_blocking_object_at(x, y)
        if target is not None:
            Game.fighter_sys.get(self).attack(target)
            if config.data.skills.omnislash.enabled:
                OmniSlash.process(self, config.data.skills.omnislash.rehitPercent, (dx, dy))
        else:
            self.move(dx, dy)
            if self.mounted:
                if self.moves_while_mounted >= 1:
                    self.moves_while_mounted = 0
                else:
                    Game.current_turn = self
                    self.moves_while_mounted += 1
                Game.stallion.x, Game.stallion.y = self.x, self.y
            Game.renderer.recompute_fov = True
            return
