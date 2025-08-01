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

def test_move_player(monkeypatch):
    import main
    main.current_location = "Town Square"
    main.locations = {
        "Town Square": {"UP": "Castle Gate"},
        "Castle Gate": {"DOWN": "Town Square"}
    }

    main.move_player("UP")
    assert main.current_location == "Castle Gate"

    main.move_player("DOWN")
    assert main.current_location == "Town Square"

def test_print_location(capsys):
    print_location()
    captured = capsys.readouterr()
    assert "You are standing" in captured.out or "You find yourself" in captured.out

def test_trigger_event(capsys):
    import main

    main.trigger_event("event_city_guard")

    captured = capsys.readouterr()
    assert "city guard" in captured.out.lower() or "guard" in captured.out.lower()

def test_combat(monkeypatch):

    player = Character()
    enemy = Enemy("Goblin", 10, "desc", 2)
    monkeypatch.setattr('builtins.input', lambda _: 'attack')
    combat(player, enemy)

    assert enemy.life <= 0 or player.life <= 0

def test_generic_event_success(capsys):
    def success_effect():
        print("Effect Triggered")

    result = generic_event("desc", 1, success_effect=success_effect, success_msg="Success")

    assert result is True

    captured = capsys.readouterr()
    assert "success" in captured.out.lower()
    assert "effect triggered" in captured.out.lower()

def test_generic_event_fail(capsys):
    def fail_effect():
        print("Effect Triggered")

    result = generic_event("desc", 100, fail_effect=fail_effect, fail_msg="Failed")

    assert result is True

    captured = capsys.readouterr()
    assert "Failed" in captured.out.lower()
    assert "effect triggered" in captured.out.lower()



