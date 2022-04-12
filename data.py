import csv
from datetime import datetime


def read_recipes_from_file(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        list_recipes = []
        for row in reader:
            list_recipes.append(row)
    return list_recipes


def write_recipes_to_file(file_name, recipes):
    with open(file_name, mode='w') as file:
        fieldnames = ['id', 'name', 'cook_time', 'servings', 'instructions', 'ingredients', 'image']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(recipes)


def save_recipes_to_file(file_name, recipe):
    with open(file_name, mode='a') as file:
        fieldnames = ['id', 'name', 'cook_time', 'servings', 'instructions', 'ingredients', 'image']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(recipe)


def update_recipe_from_file(file_name, recipe):
    recipes = read_recipes_from_file(file_name)
    index = find_recipe_index_by_id(recipes, recipe['id'])
    recipes[index] = recipe
    write_recipes_to_file(file_name, recipes)


def delete_recipe_from_file(file_name, recipe_id):
    recipes = read_recipes_from_file(file_name)
    deleted_recipe_index = find_recipe_index_by_id(recipes, recipe_id)
    recipes.pop(deleted_recipe_index)
    write_recipes_to_file(file_name, recipes)


def generate_id():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def find_recipe_by_id(file_name, recipe_id):
    recipes = read_recipes_from_file(file_name)
    index = find_recipe_index_by_id(recipes, recipe_id)
    return recipes[index]


def find_recipe_index_by_id(recipes, recipe_id):
    for i in range(len(recipes)):
        if recipes[i]['id'] == recipe_id:
            return i
