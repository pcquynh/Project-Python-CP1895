import os
from datetime import timedelta

from flask import Flask
from werkzeug.utils import secure_filename

from data import *
from user import *
from flask import render_template, request, redirect, flash, url_for, session, g

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "somerandomstring"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.permanent_session_lifetime = timedelta(minutes=5)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Create a list of users
users = [User(id=1, username='quynhpc', password='password'),
         User(id=2, username='admin', password='123456')]


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Wrong username or password. Please try again!')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/')
def index():
    if not g.user:
        return redirect(url_for('login'))
    recipes = read_recipes_from_file('static/recipes.csv')
    title = "Home Page"
    return render_template("index.html", recipes=recipes, title=title)


@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_recipe(id):
    if not g.user:
        return redirect(url_for('login'))
    delete_recipe_from_file('static/recipes.csv', id)
    flash('The recipe was removed successfully!')
    return redirect(url_for('index'))


@app.route('/save', methods=['POST'])
def save_recipe():
    if not g.user:
        return redirect(url_for('login'))
    recipe = {}
    if request.method == 'POST':
        recipe['id'] = generate_id()
        errorMessage = form_validation(request.form['name'],request.form['cook_time'],request.form['servings'],request.form['instructions'],request.form['ingredients'])
        if errorMessage:
            flash(errorMessage)
            return redirect(url_for('create_recipe'))
        else:
            recipe['name'] = request.form['name']
            recipe['cook_time'] = request.form['cook_time']
            recipe['servings'] = request.form['servings']
            recipe['instructions'] = request.form['instructions']
            recipe['ingredients'] = request.form['ingredients']

        # UPLOAD IMAGE

        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('create_recipe'))
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(url_for('create_recipe'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('upload_image filename: ' + filename)
            recipe['image'] = filename
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(url_for('create_recipe'))

        save_recipes_to_file('static/recipes.csv', recipe)

        flash('The recipe was saved successfully')
        return redirect(url_for('index'))


@app.route('/create', methods=['POST', 'GET'])
def create_recipe():
    if not g.user:
        return redirect(url_for('login'))
    title = "Add Recipe"
    return render_template("create_recipe_form.html", title=title)


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_recipe(id):
    if not g.user:
        return redirect(url_for('login'))
    title = "Edit Recipe"
    recipes = read_recipes_from_file('static/recipes.csv')
    recipe = recipes[find_recipe_index_by_id(recipes, id)]
    return render_template("edit_recipe_form.html", recipe=recipe, title=title)


@app.route('/update/<id>', methods=['POST', 'GET'])
def update_recipe(id):
    if not g.user:
        return redirect(url_for('login'))
    recipe = find_recipe_by_id('static/recipes.csv', id)
    if request.method == 'POST':
        recipe['id'] = request.form['id']
        recipe['name'] = request.form['name']
        recipe['cook_time'] = request.form['cook_time']
        recipe['servings'] = request.form['servings']
        recipe['instructions'] = request.form['instructions']
        recipe['ingredients'] = request.form['ingredients']

        # UPLOAD IMAGE

        if 'file' not in request.files or request.files['file'].filename == '':
            recipe['image'] = recipe['image']
            update_recipe_from_file('static/recipes.csv', recipe)
            flash('The recipe was updated successfully')
            return redirect(url_for('index'))

        elif request.files['file'] and allowed_file(request.files['file'].filename):
            filename = secure_filename(request.files['file'].filename)
            request.files['file'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('upload_image filename: ' + filename)
            recipe['image'] = filename
            update_recipe_from_file('static/recipes..csv', recipe)
            flash('The recipe was updated successfully')
            return redirect(url_for('index'))

        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(url_for('edit_recipe', id=request.form['id']))


def form_validation(name, cook_time, servings, instructions, ingredients):
    if name.strip() == "" or cook_time.strip() == "" or servings.strip() == "" or instructions.strip() == "" or ingredients.strip() == "":
        return "All * fields are required."


if __name__ == '__main__':
    app.run()
