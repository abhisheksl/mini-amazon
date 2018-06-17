from flask import Flask, request

app = Flask('Amazon')


@app.route('/', methods=['GET', 'POST'])
def index_page():
    return 'Welcome to Home Page!'


@app.route('/say_hello', methods=['GET', 'POST'])
def say_hello():
    if request.method == 'GET':
        return 'Hello World' + request.args['name'] +'your age is GET '+ request.args['age']

    if request.method == 'POST':
        return 'Hello ' + request.form['name']  +'your age is POST '+ request.form['age']



if __name__=='__main__':
    app.run(host='localhost', port=5000)
