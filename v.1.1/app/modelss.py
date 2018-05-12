# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class User(UserMixin,db.Model):
    '''系统登录用户
    
    Extends:
        UserMixin
        db.Model
    '''

    __tablename__ = 'User'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(),primary_key = True)

    name = db.Column(db.String(64), unique = True)

    pw_hash = db.Column(db.String(100), nullable = False)

    def __init__(self, name, password):
        self.name = name;
        self.set_password(password)


    def __repr__(self):
        return '<User {0}>' .format(self.name)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password) 


class DictionaryType(db.Model):
    '''数据字典类型
    
    Extends:
        db.Model
    '''

    __tablename__ = 'DictionaryType'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(), primary_key = True)

    name = db.Column(db.String(50), unique = True)

    isUse = db.Column(db.Integer(), default = 1)


    def __init__(self, id, name, **kw):
        self.id = id
        self.name = name

    def __repr__(self):
        return u'<DictionaryType %d %s>' %(self.id, self.name)

    def to_json(self):
        json_object = {
            'id': self.id,
            'name': self.name,
            'isUse': self.isUse
            }
        return json_object


class Dictionary(db.Model):

    __tablename__ = 'Dictionary'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(30), primary_key = True)

    name = db.Column(db.String(50), nullable = False)

    type_id = db.Column(db.Integer(), nullable = False)

    isUse = db.Column(db.Integer(), default = 1)

    """docstring for Dictionary"""
    def __init__(self, id, name, type_id):
        self.id = (''.join(id) if isinstance(id, list) else id)
        self.name = (''.join(name) if isinstance(name,list) else name)
        self.type_id = (''.join(type_id) if isinstance(type_id,list) else type_id)

    def __repr__(self):
        return u'<字典数据 id:{0} name:{1} >' .format(self.id, self.name)

    def to_json(self):
        json_object = {
            'id': self.id,
            'name': self.name,
            'type_id': self.type_id,
            'isUse': self.isUse
            }
        return json_object
    