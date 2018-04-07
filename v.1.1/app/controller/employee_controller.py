# -*- coding: utf-8 -*-
import sys
sys.path.append("..");#修改路径，为了引用models包
from models import employee

from flask import Flask,Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,fresh_login_required,current_user
from flask_uploads import UploadSet,IMAGES,configure_uploads
import json

employeeBlueprint = Blueprint('employeeBlueprint', __name__,template_folder = '../templates', 
    static_folder = '../static', url_prefix = '/employee')

'''员工管理首页(url:'/org')

:return : 首页
:date : 2018/4/6
'''
@fresh_login_required
@employeeBlueprint.route('/')
def index():
    #TODO: 组织管理首页未完成
    # return render_template('organizationindex.html');
    return render_template('employeeindex.html')

@fresh_login_required
@employeeBlueprint.route('/treeAll')
def treeAll():
    '''返回组织表中所有数据，
    格式是treeview接收的格式
    
    注意：organization.Organization.treeAll()要放在一个list再json.dumps，否则前端转换json失败

    Decorators:
        organizationBlueprint.route
    '''
    return json.dumps([employee.Employee.treeAll()])
