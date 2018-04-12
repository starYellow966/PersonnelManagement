# -*- coding: utf-8 -*-
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8")

# print sys.path

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
from flask_login import login_required,fresh_login_required,current_user
import json


from models import organization

#new a blueprint
organizationBlueprint = Blueprint('organizationBlueprint', __name__, template_folder = '../templates', 
    static_folder = '../static', url_prefix = '/org');

'''组织管理首页(url:'/org')

:return : 首页
:date : 2018/3/13
'''
@fresh_login_required
@organizationBlueprint.route('/')
def index():
    #TODO: 组织管理首页未完成
    # return render_template('organizationindex.html');
    return render_template('organizationindex.html')

@fresh_login_required
@organizationBlueprint.route('/treeAll')
def treeAll():
    '''返回组织表中所有数据，
    格式是treeview接收的格式
    
    注意：organization.Organization.treeAll()要放在一个list再json.dumps，否则前端转换json失败

    Decorators:
        organizationBlueprint.route
    '''
    return json.dumps([organization.Organization.treeAll()])

@fresh_login_required
@organizationBlueprint.route('/listChildsByName')
def listChildsByParentName():
    '''根据节点名称返回它所有孩子节点
    
    Decorators:
        organizationBlueprint.route
    '''
    request.args['name']