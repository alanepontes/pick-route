#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools.app_config import AppConfig

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

config_db = AppConfig('db-development', 'config.ini')
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}/{}'.format(config_db['dialect'], config_db['driver'], config_db['user'], config_db['pass'], config_db['host'], config_db['name'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app)

