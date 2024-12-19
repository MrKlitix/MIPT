import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

BASE_URL = "https://1000.menu"

def get_recipe_links():
    catalogs = ["salaty", "tortj", "klassicheskie-recepty-blud", "supj", "vjpechka", "vtoroe-bludo", "zakuski"]
    recipe_links = []
    for name_catalog in catalogs:
        url = f"{BASE_URL}/catalog/{name_catalog}"
        logger.info(f"Запрашиваем URL: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Ошибка при доступе к {url}: {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.select("a.h5"):
            href = link.get("href")
            if href and href.startswith("/cooking/"):
                recipe_links.append(BASE_URL + href)
    logger.info(f"Найдено {len(recipe_links)} ссылок на рецепты")
    return recipe_links


def scrape_recipe_details(recipe_url):
    response = requests.get(recipe_url)
    if response.status_code != 200:
        logger.error(f"Ошибка при доступе к {recipe_url}: {response.status_code}")
        return {}
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else "Без названия"
    ingredients = []
    for item in soup.select("div.ingredient.list-item"):
        ingredient_name = item.select_one("a.name").get_text(strip=True) if item.select_one("a.name") else None
        if ingredient_name:
            ingredients.append(ingredient_name)

    logger.debug(f"Получен рецепт: {title} с {len(ingredients)} ингредиентами")
    return {
        "title": title,
        "ingredients": ingredients,
        "url": recipe_url,
    }


def scrape_recipes():
    logger.info("Начало сбора рецептов")
    recipe_links = get_recipe_links()
    all_recipes = []

    for idx, link in enumerate(recipe_links):
        logger.info(f"Собираем данные с рецепта {idx + 1}/{len(recipe_links)}: {link}")
        recipe = scrape_recipe_details(link)
        if recipe:
            all_recipes.append(recipe)

    logger.info(f"Сбор завершен. Получено {len(all_recipes)} рецептов.")
    return all_recipes
