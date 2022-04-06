from flask import Flask
from data import *
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    recipes = read_recipes_from_file('static/recipes.csv')
    title = "Home Page"
    return render_template("index.html", recipes=recipes, title=title)


@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_recipe(id):
    pass


@app.route('/save', methods=['POST'])
def save_recipe():
    pass


@app.route('/create', methods=['POST', 'GET'])
def create_recipe():
    title = "Add recipe"
    return render_template("create_recipe_form.html", title=title)


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_recipe(id):
    pass


@app.route('/update/<id>', methods=['POST', 'GET'])
def update_recipe(id):
    pass


if __name__ == '__main__':
    app.run()
