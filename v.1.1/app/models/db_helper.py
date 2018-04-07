# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8';
db = SQLAlchemy(app)