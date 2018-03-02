from model.components.ai.monster import FrozenMonster


class FrostBomb:
    @staticmethod
    def process(area_map, player, ai_system, config):
        center = config.radius // 2
        for x in range(player.x - center, player.x + center + 1):
            for y in range(player.y - center, player.y + center + 1):
                entities = (
                    e
                    for e in area_map.get_entities_on(x, y)
                    if e.hostile
                )
                for entity in entities:
                    ai_system.get(entity).temporarily_switch_to(FrozenMonster(entity, config.turnsToThaw))
