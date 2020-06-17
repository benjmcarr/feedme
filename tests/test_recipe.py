import pytest
from feedme.recipe import recipes_to_df
from feedme.scrapers import MagimixScraper


@pytest.fixture
def recipes():
    return MagimixScraper.get_all_recipes()


def test_recipes_to_dataframe(recipes):
    df = recipes_to_df(recipes)
