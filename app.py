from flask import Flask
from data import *

app = Flask(__name__)


@app.route('/')
def index():
    pass


@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_recipe(id):
    pass


@app.route('/save', methods=['POST'])
def save_recipe():
    pass


@app.route('/create', methods=['POST', 'GET'])
def create_recipe():
    pass


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_recipe(id):
    pass


@app.route('/update/<id>', methods=['POST', 'GET'])
def update_recipe(id):
    pass








if __name__ == '__main__':
    app.run()
