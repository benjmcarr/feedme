from feedme.scrapers import MagimixScraper
from feedme.recipe import Recipe


def test_scrape_all():
    recipes = MagimixScraper.scrape_all()


def test_scrape_recipe():
    # url = 'https://www.magimix.co.uk/recipes/Shortbread'
    url = 'https://www.magimix.co.uk/recipes/Traditional-brioche'
    recipe = MagimixScraper.scrape_recipe_page(url)
    assert type(recipe) is Recipe
    assert recipe.name == 'Shortbread'


def test_get_all():
    recipes = MagimixScraper.get_all_recipes()

