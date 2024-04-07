from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from dotenv import dotenv_values

CONF = dotenv_values('api/.env')

from .module import RATP_API

api = RATP_API()

app = Flask(__name__)
app.config['SECRET_KEY'] = CONF['SECRET']

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = CONF['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SWAGGER (API DOC)
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "RATP API",
    "version": "1.0",
    "description": "A REST API for the RATP - Iledefrance mobilités",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
}
swagger = Swagger(app)

from .routes import *