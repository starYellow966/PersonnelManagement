# -*- coding: utf-8 -*-
import sys

reload(sys) 
sys.setdefaultencoding('utf8') 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesign?charset=utf8'
db = SQLAlchemy(app)

class Segment(db.Model):
	__tablename__ = 'Segment'
	#编号
	id = db.Column(db.String(10), primary_key=True)
	#名字
	name = db.Column(db.String(20), unique=True)
	#类型，就是客运段
	stype = db.Column(db.String(10), default='客运段')
	#部门名称
	dep_name = db.Column(db.String(20), nullable=False)
	#段成立时间(时间戳)
	seg_date = db.Column(db.Integer)
	# #段成立时间(时间格式如1999-10-10)
	# time = ''
	#所属铁路局
	railway = db.Column(db.String(20), nullable=False)

	def __init__(self,sid,name,dep_name,seg_date,railway,stype='客运段'):
		self.id = sid;
		self.name = name;
		self.stype = stype;
		self.dep_name = dep_name;
		self.seg_date = seg_date;
		self.railway = railway;

	def __repr__(self):
		return u'<Segment %s %s %s %s %d %s>' %(self.id,self.name,self.stype,self.dep_name,self.seg_date,self.railway);#字符串格式化符号
		#return '<Segment %s>' %self.id;


	'''返回一个list，装着Segment表的所有数据，其中list的成员是dict

	先查询，返回list(Segment对象)，然后将Segment对象转成dict再存放到list，返回这个list
	'''
	@classmethod
	def listAllData(cls):
		try:
			results = Segment.query.all();
		except Exception as e:
			db.session.rollback();
			db.session.close();
			return [];
		finally:
			db.session.close();
		segmentlist = [];
		for item in results:#循环处理
			temp = item.__dict__;
			del temp['_sa_instance_state'];#不删除这一项，后面转json会失败
			segmentlist.append(temp);
		return segmentlist;

	'''根据id更新段信息

	后端将数据封装在Segment对象中，此处只需调到db.session提交上去就可以
	时间：2018/2/23
	'''
	def updateSegmentById(self):
		flag = True;
		try:
			Segment.query.filter_by(id=self.id).update({"name": self.name, "stype": self.stype, "dep_name": self.dep_name, "seg_date": self.seg_date, "railway": self.railway});
			db.session.commit()
		except Exception as e:
			db.session.rollback();
			flag = False;
		finally:
			db.session.close();
			return flag;

	'''新增段信息

	数据封装在Segment对象中，此处只需调到db.session提交上去就可以
	时间：82018/2/23
	'''
	def insertSegment(self):
		flag = True;
		try:
			db.session.add(self);
			db.session.commit();
		except Exception as e:
			db.session.rollback();
			flag = False;
		finally:
			db.session.close();
			return flag;


	'''删除段信息

	参数targets : 一个待删除的id的list
	此处负责循环调用db.session去删除
	'''
	@classmethod
	def deleteSegment(cls,targets):
		flag = True;
		try:
			# print(targets);
			for item in targets:
				# print(item);
				s = Segment.query.filter_by(id=item).first();
				db.session.delete(s);
			db.session.commit();
		except Exception as e:
			print(e);
			db.session.rollback();
			flag = False;
		finally:
			db.session.close();
			return flag;