# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesign?charset=utf8'
db = SQLAlchemy(app)

class User(db.model):
	__tablename__ = 'User'
	id = db.Column(db.String(20),primary_key=True)
	#因为安全的原因，明文密码不可以直接存储，必需经过hash后方可存入数据库。
	password_hash = db.Column(db.String(30),nullable=False)

	#当一个新的用户注册，或者更改密码时，就会调用hash_password()函数，将原始密码作为参数传入hash_password()函数。
	def hash_password(self,password):
		sef.password_hash = pwd_context.encrypt(password)

	#当验证用户密码时就会调用verify_password()函数,如果密码正确，就返回True，如果不正确就返回False。
	def verify_password(self,password):
		return pwd_context.verify(password,self.password_hash)