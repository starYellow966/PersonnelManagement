# -*- coding: utf-8 -*-
from flask import Flask,Blueprint,render_template,request,redirect,url_for
from flask_httpauth import HTTPBasicAuth
import json

import sys
sys.path.append("..");#修改路径，为了引用models包
from models import segment,workshop;
#from segment import Segment;

#创建蓝图对象
org_manage = Blueprint('org_manage',__name__,template_folder='../templates',static_folder='../static',url_prefix='/org')
auth = HTTPBasicAuth()

'''将'/org/seg'路径绑定在segmentchart.html

其中segmentchart.html负责
'''
@org_manage.route('/seg')
def segmentIndex():
	return render_template('segmentchart.html')

'''路径'/seg/listAll'设置为提交获取全部段信息请求

第一步，通过调用Segment类方法listAllData()获取数据list
第二步，转成json，并返回给前端
'''
@org_manage.route('/seg/listAll',methods=['GET','POST'])
def listAllSegment():
	datas = segment.Segment.listAllData();#获取Segment表中所有数据,是一个list,list中是一个dict
	return json.dumps(datas),200;

@org_manage.route('/seg/query',methods=['POST'])
def querySegment():
	query = request.form['query'];
	if (query != ""):
		datas = segment.Segment.querySegment(query);
		return json.dumps(datas),200;
	return "",200;

'''路径'/seg/update'设置为提交修改段信息请求

第一步，将request.form['seg_date']的值从Date转换成时间戳
第二步，将request传来的其他data和时间戳封装在Segment对象seg中
第三步，调用Segment对象seg的成员函数updateSegmentById()更新数据库
第四步，数据库更新成功返回（响应码200+"successfully");反之，返回(200+"fail")
'''
@org_manage.route('/seg/update',methods=['POST'])
def updateSegment():
	#将时间转成时间戳存在seg_date
	import time
	seg_date = int(time.mktime(time.strptime(request.form['seg_date'], "%Y-%m-%d")));
	#封装成Segment对象
	seg = segment.Segment(request.form['id'],request.form['name'],request.form['dep_name'],
		seg_date,request.form['railway'],request.form['type']);
	
	if(seg.updateSegmentById()):
		return json.dumps(segment.Segment.listAllData()),200;
	else:
		return "fail",200;

'''路径'/seg/insert'设置为提交插入段信息请求

第一步，将request.form['seg_date']的值从Date转换成时间戳
第二步，将request传来的其他data和时间戳封装在Segment对象seg中
第三步，调用Segment对象seg的成员函数addSegment()向数据库插入段信息
第四步，数据库插入成功返回（响应码200+"successfully");反之，返回(200+"fail")
'''
@org_manage.route('/seg/insert',methods=['POST'])
def insertSegment():
	# print("reach middle level"); #测试
	#将时间转成时间戳存在seg_date
	import time
	seg_date = int(time.mktime(time.strptime(request.form['seg_date'], "%Y-%m-%d")));
	seg = segment.Segment(request.form['id'],request.form['name'],request.form['dep_name'],
		seg_date,request.form['railway'],request.form['type']);
	# print seg;
	if(seg.insertSegment()):
		return json.dumps(segment.Segment.listAllData()),200;
	else:
		return 'fail',200;


'''路径'/seg/delete'设置为提交删除段信息请求

第一步，将待删除的id字符串request.form['ids']的值（格式：1,2,3或者1）从字符串转换成数组
第二步，调用Segment类函数deleteSegment(Array)向数据库删除段信息
第三步，数据库删除成功返回（响应码200+"successfully");反之，返回(200+"fail")
'''
@org_manage.route('/seg/delete',methods=['POST'])
def deleteSegment():
	targets = request.form['ids'];
	if(segment.Segment.deleteSegment(str(targets).split(","))):
		return "successfully",200;
	else:
		return "fail",200;



'''将'/org/work'路径绑定在workshopchart.html

其中workshopchart.html负责
'''
@org_manage.route('/work')
def workshopindex():
	return render_template('workshopchart.html');

'''路径'/work/listAll'设置为提交获取全部段信息请求

第一步，通过调用Workshop类方法listAllData()获取数据list
第二步，转成json，并返回给前端
'''
@org_manage.route('/work/listAll',methods=['GET','POST'])
def listAllWorkshop():
	datas = workshop.Workshop.listAllData()
	return json.dumps(datas),200


'''路径'/work/update'设置为提交修改车间信息请求

第一步，封装成Workshop对象
第二步，调用Workshop对象work的成员函数updateWorkshopById()更新数据库
第三步，数据库更新成功返回（响应码200+"successfully");反之，返回(200+"fail")
'''
@org_manage.route('/work/update',methods=['POST'])
def updateWorkshop():
	#封装成Workshop对象
	work = workshop.Workshop(request.form['id'],request.form['name'],request.form['dep_name'],
		request.form['num'],request.form['type']);
	work.setSeg_id(request.form['seg_id']);
	if(work.updateWorkshopById()):
		return "successfully",200;
	else:
		return "fail",200;

'''路径'/work/insert'设置为提交插入车间信息请求

第一步，封装成Workshop对象
第二步，调用Workshop对象work的成员函数updateWorkshopById()更新数据库
第三步，数据库更新成功返回（响应码200+"successfully");反之，返回(200+"fail")
'''
@org_manage.route('/work/insert',methods=['POST'])
def insertWorkshop():
	form = request.form;
	#封装成Workshop对象
	work = workshop.Workshop(form['id'], form['name'], form['dep_name'], form['num'], form['type']);
	work.setSeg_id(form['seg_id']);
	if(work.insertWorkshop()):
		return 'successfully',200;
	else:
		return 'fail',200;


'''路径'/work/delete'设置为提交删除段信息请求

第一步，将待删除的id字符串request.form['ids']的值（格式：1,2,3或者1）从字符串转换成数组
第二步，调用Workshop类函数deleteWorkshop(Array)向数据库删除段信息
第三步，数据库删除成功返回（响应码200+"successfully");反之，返回(200+"fail")
'''
@org_manage.route('/work/delete',methods=['POST'])
def deleteWorkshop():
	# print("reach middle level");
	targets = request.form['ids'];
	print targets;
	if(workshop.Workshop.deleteWorkshop(str(targets).split(","))):
		return "successfully",200;
	else:
		return "fail",200;