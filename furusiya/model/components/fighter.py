import colors
from model.config import config
from model.components.base import Component
from model.factories import item_factory
from game import Game
from model.helper_functions.message import message


class Fighter(Component):
    """
    combat-related properties and methods (monster, player, NPC).
    """
    def __init__(self, owner, hp, defense, power, weapon=None, death_function=None, hostile=False):
        super().__init__(owner)
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function
        self.weapon = weapon
        self.bow_crits = 0

        self.hostile = hostile
        self.take_damage_strategy = self.default_take_damage_strategy

    def take_damage(self, damage):
        # apply damage if possible
        if damage > 0:
            self.take_damage_strategy(damage)

    def default_take_damage_strategy(self, damage):
        self.hp -= damage
        # check for death
        if self.hp <= 0:
            self.die()

    def attack(self, target, damage_multiplier=1, is_critical=False):
        # a simple formula for attack damage
        target_fighter = Game.fighter_system.get(target)
        damage = int(self.power * damage_multiplier) - target_fighter.defense

        msg = f'{self.owner.name.capitalize()} attacks {target.name}'
        if damage > 0:
            # make the target take some damage
            msg += f' for {damage} hit points.' + (' Critical strike!' if is_critical else '')
            target_fighter.take_damage(damage)
        else:
            msg += ' but it has no effect!'

        message(msg)

        # Regardless of damage, apply weapon effects
        if self.weapon:
            self.weapon.attack(target)

    def heal(self, amount):
        # heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def die(self):
        # Drop arrows if it's a monster
        if config.data.features.limitedArrows and Game.ai_system.has(self.owner):
            num_arrows = config.data.enemies.arrowDropsOnKill
            arrows = item_factory.create_item(
                self.owner.x, self.owner.y,
                '|',
                f'{num_arrows} arrows',
                colors.brass
            )

            Game.area_map.entities.append(arrows)
            arrows.send_to_back()

        # if there's a death function, call it
        death_function = self.death_function
        if death_function is not None:
            death_function(self.owner)
