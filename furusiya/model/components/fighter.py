import colors
import config
from model.components.base import Component
from model.game_object import GameObject
from model.item import Item
from main_interface import Game, message


class Fighter(Component):
    """
    combat-related properties and methods (monster, player, NPC).
    """
    def __init__(self, owner, hp, defense, power, xp, weapon=None, death_function=None):
        super().__init__(owner)
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp
        self.death_function = death_function
        self.weapon = weapon
        self.bow_crits = 0

    def take_damage(self, damage):
        # apply damage if possible
        if damage > 0:
            self.hp -= damage

            # check for death. if there's a death function, call it
            if self.hp <= 0:
                # Drop arrows if necessary
                if config.data.features.limitedArrows and self.owner.ai:  # It's a monster
                    num_arrows = config.data.enemies.arrowDropsOnKill
                    arrows = GameObject(self.owner.x, self.owner.y, '|',
                                        '{} arrows'.format(num_arrows), colors.brass, blocks=False, item=Item())
                    Game.objects.append(arrows)
                    arrows.send_to_back()

                function = self.death_function
                if function is not None:
                    function(self.owner)

    def attack(self, target, damage_multiplier=1, is_critical=False):
        # a simple formula for attack damage
        damage = int(self.power * damage_multiplier) - target.fighter.defense

        if damage > 0:
            # make the target take some damage
            message(self.owner.name.capitalize() + ' attacks ' + target.name +
                    ' for ' + str(damage) + ' hit points. {}'.format("Critical strike!" if is_critical else ""))
            target.fighter.take_damage(damage)
        else:
            message(self.owner.name.capitalize() + ' attacks ' + target.name +
                    ' but it has no effect!')

        # Regardless of damage, apply weapon effects
        if self.weapon:
            self.weapon.attack(target)

    def heal(self, amount):
        # heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp