from model.systems.fighter_system import FighterSystem


class Whirlwind:
    # modified copypasta from cast_fireball
    # TODO: DRY?
    @staticmethod
    def process(player, radius, area_map):
        for obj in area_map.entities:
            if obj.distance(player.x, player.y) <= radius and FighterSystem.has_fighter(obj) and obj is not player:
                FighterSystem.get_fighter(player).attack(obj)
