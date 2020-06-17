import logging
import pickle
import time
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional

import pandas as pd

from feedme.config import RECIPE_CACHE_PATH
from feedme.ingredient import Ingredient
from tabulate import tabulate


@dataclass
class Recipe:
    name: str
    prep_time: int
    cooking_time: int
    resting_time: int
    rating: int
    num_ratings: int
    comments: List[str]
    accessories: List[str]
    programmes: List[str]
    difficulty: int
    serves: Tuple[int, int]
    ingredients: List[Ingredient]
    instructions: List[str]
    img_src: str


class RecipesDataFrame(pd.DataFrame):
    def __init__(self, recipes: List[Recipe], **kwargs):
        super().__init__([asdict(r) for r in recipes], **kwargs)

    def pretty_str(self) -> str:
        df = self.copy()
        df['ingredients'] = [[ing['name'] for ing in ings] for ings in df['ingredients']]
        df = df.drop(columns=['instructions', 'comments', 'ingredients', 'programmes', 'accessories',
                              'num_ratings', 'img_src'])
        recipes_str = tabulate(df, headers=df.columns)
        return recipes_str


class RecipeCache:
    @staticmethod
    def get(source: str = 'magimix', lifespan: int = 7) -> Optional[List[Recipe]]:
        """Fetches all recipes in cache of given source that are 'in-date'.

        Args:
            source: where recipes come from, currently only option is 'magimix'
            lifespan: number of days the cache is in date
        """
        # todo: set lifespan check
        for f in (RECIPE_CACHE_PATH / source).iterdir():
            if f.suffix == '.pkl':
                logging.info(f'Found {source} recipes in cache.')
                with open(f, 'rb') as pkl_file:
                    recipes = pickle.load(pkl_file)
                return recipes
        logging.info(f'Could not find any {source} recipes in cache.')

    @staticmethod
    def set(source: str, recipes: List[Recipe]) -> None:
        """Sets a new entry in the cache.

        Args:
            source: where recipes come from, currently only option is 'magimix'
            recipes: recipes to cache
        """
        timestamp_in_days = round(time.time() / 60 / 60 / 24)
        save_path = RECIPE_CACHE_PATH / source / f'{timestamp_in_days}.pkl'
        logging.info(f'Setting {source} recipes to cache location {save_path}')
        with open(save_path, 'wb+') as pkl:
            pickle.dump(recipes, pkl)
