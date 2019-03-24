from flask import Flask

application = Flask(__name__)

from flask_app import routes
