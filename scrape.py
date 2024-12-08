import requests
from bs4 import BeautifulSoup


BASE_URL = "https://1000.menu"

def get_recipe_links():
    catalogs = ["salaty", "tortj", "klassicheskie-recepty-blud", "supj", "vjpechka", "vtoroe-bludo", "zakuski"]
    recipe_links = []
    for name_catalog in catalogs:
        url = f"{BASE_URL}/catalog/{name_catalog}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Ошибка при доступе к странице рецептов:", response.status_code)
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.select("a.h5"):
            href = link.get("href")
            if href and href.startswith("/cooking/"):
                recipe_links.append(BASE_URL + href)
    return recipe_links


def scrape_recipe_details(recipe_url):
    response = requests.get(recipe_url)
    if response.status_code != 200:
        print(f"Ошибка при доступе к {recipe_url}: {response.status_code}")
        return {}
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else "Без названия"
    ingredients = []
    for item in soup.select("div.ingredient.list-item"):
        ingredient_name = item.select_one("a.name").get_text(strip=True) if item.select_one("a.name") else None
        ingredients.append(f"{ingredient_name}")

    return {
        "title": title,
        "ingredients": ingredients,
        "url": recipe_url,
    }


def scrape_recipes():
    recipe_links = get_recipe_links()
    all_recipes = []

    for idx, link in enumerate(recipe_links):
        print(f"Собираем данные с рецепта {idx + 1}/{len(recipe_links)}: {link}")
        recipe = scrape_recipe_details(link)
        if recipe:
            all_recipes.append(recipe)

    return all_recipes

