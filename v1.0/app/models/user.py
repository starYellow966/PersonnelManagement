# -*- coding: utf-8 -*-
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesign?charset=utf8'
app.config['SECRET_KEY'] = 'I do not how to use this variable now'

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class User(db.Model):
	__tablename__ = 'User'
	id = db.Column(db.String(20),primary_key=True)
	#因为安全的原因，明文密码不可以直接存储，必需经过hash后方可存入数据库。
	password_hash = db.Column(db.String(128),nullable=False)

	#当一个新的用户注册，或者更改密码时，就会调用hash_password()函数，将原始密码作为参数传入hash_password()函数。
	def hash_password(self,password):
		sef.password_hash = pwd_context.encrypt(password)

	#当验证用户密码时就会调用verify_password()函数,如果密码正确，就返回True，如果不正确就返回False。
	def verify_password(self,password):
		return pwd_context.verify(password,self.password_hash)

	def generate_auth_token(self,expiration=6000):
		s = Serializer(app.config['SECRET_KEY'],expires_in = expiration)
		return s.dumps({'id':self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except Exception as e:
			return None
		user = User.query.get(data['id'])
		return user

@auth.verify_password
def verify_password(username_or_token,password):
	#first try to authenticate by token
	u = User.verify_password(username_or_token)
	if not u:
		#try to authenticate with username/password
		u = User.query.filter_by(username=username_or_token).first()
		if not u or not u.verify_password(password):
			return False
	g.user = u

	return True