from unittest.mock import Mock

from model.maps.area_map import AreaMap
from model.skills.frostbomb import FrostBomb
from model.systems.system import ComponentSystem


def test_process_freezes_enemies():
    radius, turns_to_thaw = 5, 5
    enemies_in_range = Mock(x=6, y=3), Mock(x=4, y=5)
    enemies_out_of_range = Mock(x=1, y=1), Mock(x=9, y=9)
    player = Mock(x=5, y=5)

    area_map = AreaMap(10, 10)
    area_map.entities = [*enemies_in_range] + [*enemies_out_of_range] + [player]

    ai_system = ComponentSystem()

    for entity in area_map.entities:
        ai_system.set(entity, Mock())

    conf = Mock(radius=radius, turnsToThaw=turns_to_thaw)

    FrostBomb.process(area_map, player, ai_system, conf)

    for enemy in enemies_in_range:
        assert ai_system.get(enemy).temporarily_switch_to.called

    for enemy in enemies_out_of_range:
        assert not ai_system.get(enemy).temporarily_switch_to.called
