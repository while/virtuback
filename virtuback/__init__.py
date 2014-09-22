from flask import Flask

# Create WSGI application
app = Flask(__name__)

# Import API definition
from virtuback import api

