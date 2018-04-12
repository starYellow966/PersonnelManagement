# -*- coding: utf-8 -*-
# 设置默认编码
import sys
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import  Required
from flask_wtf import FlaskForm
from extensions import db
# app = Flask(__name__);
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8';
# db = SQLAlchemy(app);

class User(UserMixin,db.Model):

    __tablename__ = 'User'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(),primary_key = True)

    name = db.Column(db.String(64), unique = True)

    password = db.Column(db.String(64), nullable = False)

    def __init__(self, name, password):
        self.name = name;
        self.password = password


    def __repr__(self):
        return '<User {0}>' .format(self.name)


#登录表单
class Login_Form(FlaskForm):
    name=StringField(u'用户名',validators=[Required(message=u'用户名不能为空')])
    pwd=PasswordField(u'密码',validators=[Required(message=u'密码不能为空')])
    remember_me = BooleanField('Remember_me', default = False)
    submit=SubmitField(u'登录')