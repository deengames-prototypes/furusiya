import colors
from constants import DELTA_UP, DELTA_DOWN, DELTA_LEFT, DELTA_RIGHT
from game import Game
from model.entities.game_object import GameObject
from model.config import config


class Fire(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, '*', 'Fire', colors.red, blocks=False)

        Game.instance.events.bind('on_entity_move', self.on_entity_move)
        Game.instance.events.bind('on_turn_pass', self.on_turn_passed)

        self.turns_passed_alight = 0

    def on_entity_move(self, entity):
        if (entity.x, entity.y) == (self.x, self.y):
            Game.instance.fighter_system.get(entity).take_damage(config.data.enemies.fire.damage)
            self.die()

    def on_turn_passed(self):
        self.turns_passed_alight += 1
        if self.turns_passed_alight >= config.data.enemies.fire.selfExtinguishTurns:
            self.die()
        if config.data.enemies.fire.spreadProbability >= Game.instance.random.randint(1, 100):
            dx, dy = Game.instance.random.choice([DELTA_UP, DELTA_DOWN, DELTA_LEFT, DELTA_RIGHT])
            created_fire = Fire(self.x + dx, self.y + dy)
            Game.instance.area_map.entities.append(created_fire)

    def die(self):
        super().die()
        Game.instance.events.unbind('on_entity_move', self.on_entity_move)
        Game.instance.events.unbind('on_turn_pass', self.on_turn_passed)
