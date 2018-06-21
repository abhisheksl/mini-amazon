from flask import Flask, request, send_from_directory, jsonify

app = Flask('Amazon')

products=[]
@app.route('/', methods=['GET'])
def index_page():
    return send_from_directory('static', 'index.html')


@app.route('/api/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        query = request.args['name']
        for prod in products:
            if prod['name'] == query:
                return jsonify(prod)
        return 'No match'

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        desc = request.form['desc']

        prod = {
            'name': name,
            'price': price,
            'desc':desc
        }
        products.append(prod)
        return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
