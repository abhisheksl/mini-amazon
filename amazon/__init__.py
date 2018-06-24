from flask import Flask

# Create the app
app = Flask('Amazon', template_folder='./amazon/templates')

# Import API to invoke and configure the app
from amazon import api
