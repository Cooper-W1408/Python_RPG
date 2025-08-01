import pytest
from main import Character, Enemy, Inventory, Item, game_state_to_dict, load_game_state, save_game, load_game, move_player, print_location, trigger_event, combat, generic_event

def test_character_initialization():
    c = Character()
    assert hasattr(c, 'inventory')

def test_enemy_initialization():
    e = Enemy("Goblin", 30, "desc", 4)
    assert e.name == "Goblin"
    assert e.life == 30
    assert e.attack == 4

def test_character_to_dict(monkeypatch):
    c = Character()
    monkeypatch.setattr(c, "inventory", Inventory())
    result = c.to_dict()
    assert isinstance(result, dict)

def test_character_from_dict():
    c = Character()
    data = {"inventory": []}
    c.from_dict(data)
    assert hasattr(c, "inventory")