from flask import request, send_from_directory, render_template, session

from amazon import app
from amazon.model import products as product_model
from amazon.model import users as user_model


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html', message="Flat 10% off with PayTM!")


# Entry point for Admins
@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html', value='Admin')


@app.route('/api/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        query = request.args['name']
        user_id = session['user_id']
        user_details = user_model.search_by_userid(user_id)
        username = user_details['name']
        matching_products = product_model.search_product(query)
        if username == 'admin':
            return render_template('admin_results.html', query=query, product=matching_products)
        else:
            return render_template('results.html', query=query, product=matching_products)

    elif request.method == 'POST':
        op_type = request.form['op_type']
        name = request.form['name']
        price = int(request.form['price'])
        desc = request.form['desc']

        prod = {
            'name': name,
            'price': price,
            'desc': desc
        }

        if op_type == 'add':

            product_model.add_product(prod)
            return render_template('index.html', message="Product added successfully!")

        elif op_type == 'update':

            product_id = request.form['product_id']
            matching_products = product_model.get_details(product_id)
            if request.form['name'] == '':
                new_name = matching_products['name']
            else:
                new_name = request.form['name']

            if request.form['desc'] == '':
                new_desc = matching_products['desc']
            else:
                new_desc = request.form['desc']

            if request.form['price'] == '':
                new_price = int(matching_products['price'])
            else:
                new_price = request.form['price']
            updated_product = {'name': new_name,
                               'desc': new_desc,
                               'price': new_price
                               }
            product_model.update_product(product_id, updated_product)

            return render_template('admin.html', message="Product updated successfully!")

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
            user_details = user_model.search_a_user(username)
            if username == 'admin':
                session['user_id'] = str(user_details['_id'])
                return render_template('admin.html', value=username)
            else:
                session['user_id'] = str(user_details['_id'])
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
            user_model.user_signup(name, username, password)
            user_details = user_model.search_a_user(username)
            session['user_id'] = str(user_details['_id'])
            return render_template('home.html', value=name)


@app.route('/api/cart', methods=['POST'])
def cart():
    # Add/Delete/Retrieve
    op_type = request.form['op_type']
    user_id = session['user_id']
    user_details = user_model.search_by_userid(user_id)
    if op_type == 'add':
        product_id = request.form['product_id']
        user_id = session['user_id']
        user_model.add_to_cart(user_id, product_id)
        return render_template('home.html', value=" ")

    elif op_type == 'retrieve':

        cart_item_id = user_model.retrieve_cart(session['user_id'])
        cart_items = []
        total = 0
        for p_id in cart_item_id:
            cart_item = product_model.get_details(p_id)
            cart_items.append(cart_item)
            cart_item['price']
            total += cart_item['price']
        user_details = user_model.search_by_userid(user_id)

        return render_template('cart.html',
                               products=cart_items,
                               name=user_details['name'],
                               total= total)
    elif op_type == 'delete':

        product_id = request.form['product_id']
        user_model.delete_from_cart(session['user_id'], product_id)

        cart_item_ids = user_model.retrieve_cart(user_id)

        cart_items = []
        for p_id in cart_item_ids:
            cart_items.append(product_model.get_details(p_id))

        return render_template('cart.html', products=cart_items, name=user_details['name'])

# Logout feature
@app.route('/logout', methods=['GET'])
def logout():
    del session['user_id']
    return render_template('index.html', message='10% off with PayTM')