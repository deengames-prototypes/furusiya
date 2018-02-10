import math

import colors
from model.config import config
from main_interface import message
from model.components.ai.monster import StunnedMonster
from model.components.fighter import Fighter
from model.systems.ai_system import AISystem


class Hammer:
    def __init__(self, owner):
        self.owner = owner

    def attack(self, target):
        if config.data.features.hammerKnocksBack and AISystem.has_ai(target):
            # The directional vector of knockback is (defender - attacker)
            dx = target.x - self.owner.x
            dy = target.y - self.owner.y
            knockback_amount = config.data.weapons.hammerKnockBackRange
            # copysign gets the sign of dx/dy. We just need that, not the magnitude
            if dx != 0:
                dx = int(math.copysign(1, dx)) * knockback_amount
                dy = 0
            elif dy != 0:
                dy = int(math.copysign(1, dy)) * knockback_amount
                dx = 0

            goal_x = target.x + dx
            goal_y = target.y + dy
            knockback_distance = 0
            display_message = "{} hits something and falls over!".format(target.name)
            extra_message = None

            while target.x != goal_x or target.y != goal_y:
                (old_x, old_y) = (target.x, target.y)
                hit_something = target.move_towards(goal_x, goal_y)
                if target.x == old_x and target.y == old_y:
                    # Didn't move: hit a solid wall
                    AISystem.get_ai(target).temporarily_switch_to(StunnedMonster(target))

                    # Take additional damage for hitting something; if (and only
                    # if) we actually flew backward one or more spaces.
                    if config.data.features.knockBackDamagesOnCollision and knockback_distance:
                        damage_percent = config.data.weapons.hammerKnockBackDamagePercent / 100
                        target_fighter = target.get_component(Fighter)
                        knockback_damage = int(damage_percent * target_fighter.max_hp)
                        target_fighter.take_damage(knockback_damage)
                        display_message += ' Takes {} additional damage!'.format(knockback_damage)

                        # Did we hit someone?
                        hit_someone = hit_something.get_component(Fighter) if hit_something else None
                        if hit_someone:
                            knockback_damage = int(damage_percent * hit_someone.max_hp)
                            hit_someone.take_damage(knockback_damage)
                            extra_message = "{} looks injured!".format(hit_something.name)
                    break
                else:
                    knockback_distance += 1

            message(display_message, colors.light_green)
            if extra_message:
                message(extra_message, colors.light_green)