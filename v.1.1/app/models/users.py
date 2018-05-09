# -*- coding: utf-8 -*-
# 设置默认编码
import sys
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import  Required, ValidationError
from flask_wtf import FlaskForm
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):

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


#登录表单
class Login_Form(FlaskForm):
    name = StringField(u'用户名',validators=[Required(message=u'用户名不能为空')])
    pwd = PasswordField(u'密码',validators=[Required(message=u'密码不能为空')])
    # remember_me = BooleanField('Remember_me', default = False)
    submit=SubmitField(u'登录')

    def validate_name(self, field):
        # print 'validate_name'
        name = field.data
        user = User.query.filter_by(name = name).count()
        if user == 0 :
            raise ValidationError(u"此用户不存在")