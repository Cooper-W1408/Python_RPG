import pytest
from main import Character, Enemy

def test_character_initialization():
    c = Character()
    assert hasattr(c, 'inventory')

def test_enemy_initialization():
    e = Enemy("Goblin", 30, "desc", 4)
    assert e.name == "Goblin"
    assert e.life == 30
    assert e.attack == 4

