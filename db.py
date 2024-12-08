import sqlite3
import time
from scrape import scrape_recipes


DATABASE = "recipes.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            ingredients TEXT,
            url TEXT UNIQUE,
            last_updated INTEGER
        )
    ''')

    conn.commit()
    conn.close()


def add_recipe(title, ingredients, url):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO recipes (title, ingredients, url, last_updated)
        VALUES (?, ?, ?, ?)
    ''', (title, ", ".join(ingredients), url, int(time.time())))

    conn.commit()
    conn.close()


def is_database_empty():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM recipes')
    count = cursor.fetchone()[0]

    conn.close()
    return count == 0


def update_database():
    print("Начинаем обновление базы данных...")
    recipes = scrape_recipes()
    for recipe in recipes:
        title = recipe['title']
        ingredients = recipe['ingredients']
        url = recipe['url']
        add_recipe(title, ingredients, url)
    print("Обновление базы данных завершено!")


def view_all_recipes():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, ingredients, url FROM recipes')
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Название: {row[1]}, Ингредиенты: {row[2]}, Ссылка: {row[3]}")
    else:
        print("База данных пуста.")

    conn.close()


def start_database():
    create_table()
    if is_database_empty():
        print("База данных пуста. Запускаем скраппинг и обновление данных.")
        update_database()
    else:
        print("База данных готова к работе.")

