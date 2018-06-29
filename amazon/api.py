from flask import request, send_from_directory, jsonify, render_template

from amazon import app
from amazon.model import products as product_model
from amazon.model import users as user_model


@app.route('/', methods=['GET'])
def index_page():
    return send_from_directory('./amazon/static/', 'index.html')


@app.route('/api/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        query = request.args['name']
        matching_products = product_model.search_product(query)
        return render_template('results.html', query=query, results=matching_products)

    elif request.method == 'POST':
        op_type = request.form['op_type']
        name = request.form['name']
        price = request.form['price']
        desc = request.form['desc']

        prod = {
            'name': name,
            'price': price,
            'desc': desc
        }

        if op_type == 'add':

            product_model.add_product(prod)
            return 'Product ' + name + ' added successfully!'

        elif op_type == 'update':

            name = request.form['name']
            updated_product = {'name': name,
                               'desc': request.form['desc'],
                               'price': request.form['price']
                               }
            product_model.update_product(name, updated_product)

            return 'Product details updated successfully!'

        return 'Product not found'


@app.route('/api/users', methods=['POST'])
#Login or Signup
def user():
    op_type = request.form['op_type']
    if op_type == 'login':
        username = request.form['username']
        password = request.form['password']
        success = user_model.authenticate(username, password)
        if success:
            if username == 'admin':
                return render_template('admin.html', value=username)
            else:
                return render_template('home.html', value=username)
        else:
            return '<h2> User not found </h2>'

    if op_type == 'signup':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        success = user_model.search_a_user(username)
        if success:
            return '<h2> Username already exists. Please use a new username </h2>'
        else:
            user_model.user_signup(name,username,password)
            return render_template('home.html', value=name)

