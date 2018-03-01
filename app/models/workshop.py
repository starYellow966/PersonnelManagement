# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from segment import Segment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,IntegerField
from wtforms import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesign?charset=utf8'
db = SQLAlchemy(app)

class Workshop(db.Model):
	"""车间"""

	__tablename__ = 'Workshop'
	#id，显示项
	id = db.Column(db.String(10),primary_key=True)
	#车间名称，显示项
	name = db.Column(db.String(20),unique=True)
	#类型，显示项
	wtype = db.Column(db.String(10),default='车间')
	#部门名称，显示项
	dep_name = db.Column(db.String(20),nullable=False)
	#所属客运段id,隐藏项 外键约束不会设置，但在数据库设置了
	# seg_id = db.Column(db.String(10),db.ForeignKey('Segment.id'))
	seg_id = db.Column(db.String(10),nullable=False)
	#所属客运段名称，显示项
	seg_name = ""
	#序号，显示项
	num = db.Column(db.Integer,nullable=True)
	
	#给这个Workshop模型添加一个seg_name属性（关系表），U，backref为定义反向引用，可以通过‘Segment.workshops’这个模型（表）访问这个表的所有内容
	# segname = db.relationship('Segment',backref = db.backref('workshops'),lazy='select')
	
	def __init__(self, id,name,dep_name,num,wtype="车间"):
		# print "enter into __init__"
		self.id = id
		self.name = name
		self.wtype = wtype
		self.dep_name = dep_name
		self.num = num

	def setSeg_id(self,sid):
		# print sid;
		self.seg_id = sid;
		self.seg_name = Segment.query.filter(Segment.id == self.seg_id).first().name

	def setSeg_name(self,name):
		self.seg_name = name
		self.seg_id = Segment.query.filter(Segment.name == self.seg_name).first().id
	def __repr__(self):
		return u'<Workshop %s %s %s %s %s %s>' %(self.id,self.name,self.wtype,self.dep_name,self.seg_id,self.seg_name) #字符串格式化符号


	'''返回值=装着所有Workshop数据的list(返回值可直接转为json)

	2018/2/28
	第一步：先查询，查询结果是一个list(Workshop对象)
	第二步：将Workshop对象转成dict，目的是为了让返回值可直接转为json
	'''
	@classmethod
	def listAllData(cls):
	#实现第一步
		try:
			results = Workshop.query.all()
		except Exception as e:
			db.session.rollback()
			db.session.close()
			return []
		finally:
			db.session.close()
		#实现第二步
		workshoplist = []
		for item in results:
			temp = item.__dict__
			#隐藏项，增加项
			#item虽是Workshop对象，却没有调用__init__函数，故此seg_name值为空
			temp['seg_name'] = Segment.query.filter(Segment.id == item.seg_id).first().name #用name代替id显示
			del temp['_sa_instance_state'] #不删除这项，workshoplist没法转为json
			del temp['seg_id'] #不宜暴露
			workshoplist.append(temp)
		return workshoplist

	'''根据id更新车间信息

	2018/2/28
	前提：数据封装在Workshop对象中
	'''
	def updateWorkshopById(self):
		flag = True;
		try:
			# print self;
			Workshop.query.filter_by(id=self.id).update({"name": self.name, "wtype": self.wtype, "dep_name": self.dep_name, "seg_id": self.seg_id, "num": self.num});
			db.session.commit()
		except Exception as e:
			db.session.rollback();
			flag = False;
		finally:
			db.session.close();
			return flag;
	
	'''插入车间信息

	2018/2/28
	前提：数据封装在Workshop对象中
	'''
	def insertWorkshop(self):
		flag = True;
		try:
			db.session.add(self);
			db.session.commit();
		except Exception as e:
			print e;
			db.session.rollback();
			flag = False;
		finally:
			db.session.close();
			return flag;

	'''删除车间信息

	2018/2/28
	参数targets : 一个待删除的id的list
	'''
	@classmethod
	def deleteWorkshop(cls,targets):
		flag = True;
		try:
			for item in targets:
				w = Workshop.query.filter_by(id = item).first();
				db.session.delete(w);
			db.session.commit();
		except Exception as e:
			print e;
			db.session.rollback();
			flag = False;
		finally:
			db.session.close();
			return flag;

'''表单类

2018/3/1
'''
class WorkshopForm(FlaskForm):
	id = StringField('编号');
	name = StringField('车间名称');
	type = StringField('类型');
	dep_name = StringField('部门名称');
	seg_name = SelectField('所属客运段',render_kw={"data-live-search":"true"}); #开启搜索框
	num = IntegerField('序号');
	submit = SubmitField('提交更改');

	# '''id值查重

	# 2018/3/1
	# '''
	# def validate_id(self,field):
	# 	#查重
	# 	if(Workshop.query.filter_by(id = field.data).first()):
	# 		return ValidationError('id alreadyly in use');

	
		