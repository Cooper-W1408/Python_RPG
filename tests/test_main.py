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

def test_inventory_add_remove():
    inv = Inventory()
    item = Item("Sword", "Potion")
    inv.add(item)
    assert item in inv.items
    inv.remove(item)
    assert item not in inv.items

def test_item_initialization():
    item = Item("Potion", "Heals", effect="heal")
    assert item.name == "Potion"
    assert item.effect == "heal"

def test_game_state_to_dict():
    state = game_state_to_dict()
    assert "character" in state
    assert "inventory" in state
    assert "solved_places" in state

def test_save_and_load_game(tmp_path):
    filename = tmp_path / "savegame.json"
    save_game(str(filename))
    data = load_game(str(filename))
    assert data is not None 
