from model.components.ai.monster import StunnedMonster


class FrostBomb:
    @staticmethod
    def process(area_map, player, ai_system, conf):
        center = conf.radius // 2
        for x in range(player.x - center, player.x + center):
            for y in range(player.y - center, player.y + center):
                entities = (
                    e
                    for e in area_map.get_entities_on(x, y)
                    if e.hostile
                )
                for entity in entities:
                    ai_system.set(entity, StunnedMonster(entity, conf.turnsToThaw))

