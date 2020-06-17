import logging
from typing import List, Tuple

from bs4 import BeautifulSoup
from feedme.config import MAGIMIX_URL
from feedme.ingredient import Ingredient
from feedme.recipe import Recipe, RecipeCache
from feedme.utils import url_to_soup


class MagimixScraper:
    """scrape recipes"""

    @staticmethod
    def get_all_recipes():
        cached_recipes = RecipeCache.get('magimix')
        if cached_recipes is None:
            rs = MagimixScraper.scrape_all()
            RecipeCache.set('magimix', rs)
            return rs
        return cached_recipes

    @staticmethod
    def scrape_all() -> List[Recipe]:
        logging.info('Starting scrape_all()..')
        num_pages = MagimixScraper._get_num_pages()
        page_urls = MagimixScraper._get_list_page_urls(num_pages)
        logging.info(f'\tTotal Number of recipe pages found = {len(page_urls)}')
        rs = []
        for i, url in enumerate(page_urls):
            rs += MagimixScraper.scrape_recipelist_page(url)
            logging.info(f'\t{i+1:02d}/{len(page_urls)}\tScraped recipelist page {url}')
        logging.info(f'Successfully scraped {len(rs)} recipes.')
        return rs

    @staticmethod
    def scrape_recipelist_page(url: str) -> List[Recipe]:
        soup = url_to_soup(url)
        recipe_urls = MagimixScraper._soup_to_recipe_urls(soup)[:2]
        rs = []
        for i, url in enumerate(recipe_urls):
            r = MagimixScraper.scrape_recipe_page(url)
            rs.append(r)
            logging.info(f'\t\t{i+1:02d}/{len(recipe_urls)}\t Scraped {r.name}')
        return rs

    @staticmethod
    def scrape_recipe_page(url: str) -> Recipe:
        soup = url_to_soup(url)

        prep_str = soup.find_all('p', string=lambda text: text is not None and 'PREPARATION' in text)[0].text
        prep_time = int(prep_str.split(' ')[-2])

        cooking_str = soup.find_all('p', string=lambda text: text is not None and 'COOKING' in text)[0].text
        cooking_time = int(cooking_str.split(' ')[-2])

        resting_str = soup.find_all('p', string=lambda text: text is not None and 'RESTING' in text)[0].text
        resting_time = int(resting_str.split(' ')[-2])

        name = soup.find_all('h1')[0].text
        rating_p = 5
        num_ratings = 1
        comments = ['mmmm delicious']
        programmes = []
        accessories = []
        difficulty = 1
        serves = (2, 4)

        ingredients_div = soup.find_all('div', class_='col-lg-4 no-padding col-sm-12')[0]
        ingredients = []
        for p in ingredients_div.find_all('p'):
            ingredients.append(MagimixScraper._text_to_ingredient(p.text))

        instructions_div = soup.find_all('div', class_='bloc-3 row')[0]
        instructions = []
        for li in instructions_div.find_all('li'):
            instructions.append(li.text)

        img_src = ''

        recipe = Recipe(
            name=name,
            prep_time=prep_time,
            cooking_time=cooking_time,
            resting_time=resting_time,
            rating=rating_p,
            num_ratings=num_ratings,
            comments=comments,
            accessories=accessories,
            programmes=programmes,
            difficulty=difficulty,
            serves=serves,
            ingredients=ingredients,
            instructions=instructions,
            img_src=img_src
        )
        return recipe

    @staticmethod
    def _soup_to_recipe_urls(soup: BeautifulSoup) -> List[str]:
        recipe_urls = []
        for div in soup.find_all('div', class_='bloc-recipe'):
            for a in div.find_all('a', href=True):
                if a.text:
                    recipe_urls.append(f"https://www.magimix.co.uk/{a['href']}")
        return recipe_urls

    @staticmethod
    def _split_out_quantity(text: str) -> Tuple[int, str]:
        leading_el, *other_els = text.split(' ')
        try:
            leading_int = int(leading_el)
            return leading_int, ' '.join(other_els)
        except ValueError:
            return 1, text

    @staticmethod
    def _split_out_extra_info(name: str) -> Tuple[str, str]:
        new_name, extra_info = name, ''
        if '(' in name:
            new_name, *rest = name.split('(')
            extra_info = ''.join(rest)[:-1]
        return new_name.strip(), extra_info.strip()

    @staticmethod
    def _text_to_ingredient(text: str) -> Ingredient:
        if ' g ' in text:
            units = 'g'
            quantity, name = text.split(' g ')
            quantity = int(quantity)
        else:
            units = 'items'
            quantity, name = MagimixScraper._split_out_quantity(text)
        name, extra_info = MagimixScraper._split_out_extra_info(name)
        ing = Ingredient(name=name.strip(), quantity=quantity,
                         units=units, extra_info=extra_info.strip())
        return ing

    @staticmethod
    def _get_num_pages() -> int:
        """Returns number of recipe pages"""
        soup = url_to_soup(MAGIMIX_URL)
        lis = [el for el in soup.find_all('ul', 'pagination page-list clearfix text-sm-center')[0].children]
        last_page_num = int(lis[-4].text.replace('\n', ''))
        return last_page_num

    @staticmethod
    def _get_list_page_urls(num_pages: int) -> List[str]:
        """Get page urls for each recipe list"""
        urls = ['https://www.magimix.co.uk/recipes']
        urls += [f'https://www.magimix.co.uk/recipes?p={i}' for i in range(2, num_pages + 1)]
        return urls


if __name__ == '__main__':
    logging.basicConfig(filename='../../app.log', filemode='w',
                        format='%(levelname)s - %(message)s',
                        level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    recipes_ = MagimixScraper.get_all_recipes()
