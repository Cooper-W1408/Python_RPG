import pytest
from tests.main import Character

def test_character_initialization():
    c = Character()
    assert hasattr(c, 'inventory')