import pytest
from feedme.ingredient import Ingredient


@pytest.fixture
def two_same_ings():
    ing1 = Ingredient(name='apple', units='g', quantity=100, extra_info='')
    ing2 = Ingredient(name='apple', units='g', quantity=200, extra_info='')
    return ing1, ing2


def test_add_ingredients(two_same_ings):
    ing1, ing2 = two_same_ings
    ing3 = ing1 + ing2
    assert ing3.name == 'apple'
    assert ing3.units == 'g'
    assert ing3.quantity == 300
    assert ing3.extra_info == ''


def test_minus_ingredients(two_same_ings):
    ing1, ing2 = two_same_ings
    ing3 = ing2 - ing1
    assert ing3.name == 'apple'
    assert ing3.units == 'g'
    assert ing3.quantity == 100
    assert ing3.extra_info == ''
