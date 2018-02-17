from model.item import Item
from model.maps.area_map import AreaMap
from model.maps.generators import map_generator
from model.systems.fighter_system import FighterSystem

class TestMapGenerator:

    def test_generate_monsters_generates_enough_monsters(self):
        expected_monsters = 7        
        area_map = AreaMap(5, 5)
        
        # Act
        map_generator.generate_monsters(area_map, expected_monsters)

        # Assert
        assert len(area_map.entities) == expected_monsters

        for monster in area_map.entities:
            assert FighterSystem.get_fighter(monster) is not None

    def test_generate_items_generates_enough_items(self):
        expected_items = 10
        area_map = AreaMap(7, 7)

        map_generator.generate_items(area_map, expected_items)

        # Assert
        assert len(area_map.entities) == expected_items

        for item in area_map.entities:
            assert item.get_component(Item) is not None
