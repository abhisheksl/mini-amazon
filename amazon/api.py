from flask import request, send_from_directory, jsonify, render_template

from amazon import app
from amazon.model import products as product_model


@app.route('/', methods=['GET'])
def index_page():
    return send_from_directory('./amazon/static', 'index.html')


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
            return send_from_directory('./amazon/static', 'index.html')

        elif op_type == 'update':

            name = request.form['name']
            updated_product = {'name': name,
                               'desc': request.form['desc'],
                               'price': request.form['price']
                               }
            product_model.update_product(name, updated_product)

            return send_from_directory('./amazon/static', 'index.html')

        return 'Product not found'
