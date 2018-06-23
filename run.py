from flask import Flask, request, send_from_directory, jsonify
from pymongo import MongoClient


app = Flask('Amazon')

client = MongoClient('localhost', port=27017)
db = client['pymlb2-amazon']

@app.route('/', methods=['GET'])
def index_page():
    return send_from_directory('static', 'index.html')


@app.route('/api/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        query = {'name': request.args['name']}
        matching_products = db['products'].find(query)
        for p in matching_products:
            p['_id'] = str(p['_id'])
            return jsonify(p)
        return 'No product found'

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

            db['products'].insert_one(prod)
            return send_from_directory('static', 'index.html')

        elif op_type == 'update':

                filter = {'name' : request.form['name']}
                update = {
                    '$set': prod
                }
                db['products'].update_one(filter=filter, update=update, upsert=True)
                return send_from_directory('static', 'index.html')

        return 'Product not found'


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
