import logging

import click

from feedme.recipe import RecipesDataFrame
from feedme.scrapers import MagimixScraper

from . import __version__

logging.basicConfig(filename='../../app.log', filemode='w',
                    format='%(levelname)s - %(message)s',
                    level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler())


@click.command()
@click.version_option(version=__version__)
def gen_recipes():
    """generate recipes"""
    recipes = MagimixScraper.get_all_recipes()[:5]
    recipes_df = RecipesDataFrame(recipes)
    click.secho("Your Menu!", fg="green")
    click.echo(recipes_df.pretty_str())
