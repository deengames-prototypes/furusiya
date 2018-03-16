import colors
from game import Game
from model.entities.game_object import GameObject
from model.config import config


class Fire(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, '*', 'Fire', colors.red, blocks=False)

        Game.instance.event_bus.bind('on_entity_move', self.on_entity_move, self)
        Game.instance.event_bus.bind('on_turn_pass', self.on_turn_passed, self)

        self.turns_passed_alight = 0

    def on_entity_move(self, entity):
        if (entity.x, entity.y) == (self.x, self.y):
            fighter = Game.instance.fighter_system.get(entity)
            if fighter is not None:
                fighter.take_damage(config.data.enemies.fire.damage)
                self.die()

    def on_turn_passed(self):
        self.turns_passed_alight += 1
        if self.turns_passed_alight >= config.data.enemies.fire.selfExtinguishTurns:
            self.die()
        if config.data.enemies.fire.spreadProbability >= Game.instance.random.randint(1, 100):
            tile = Game.instance.area_map.mutate_position_if_walkable(self.x, self.y)
            if tile is not None:
                created_fire = Fire(*tile)
                Game.instance.area_map.entities.append(created_fire)
