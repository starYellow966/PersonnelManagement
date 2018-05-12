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
    static_folder = '../static');

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
@organizationBlueprint.route('/listall', methods=['GET'])
def list_all():
    '''返回所有组织信息
    
    Decorators:
        fresh_login_required
        organizationBlueprint.route
    
    Returns:
        [type] -- 类型，1代表需要组织详细信息，其他代表只需要组织编号和名字信息
    '''
    query_type = request.args['type']
    if(query_type == 1):
        return json.dumps([organization.Organization.listAll()])
    else:
        return json.dumps(organization.Organization.list_all_name())
@fresh_login_required
@organizationBlueprint.route('/insert', methods=['GET'])
def insert():
    oid = request.args.get('id')
    name = request.args.get('name')
    status = request.args.get('status')
    parent_id = request.args.get('parent_id')
    num = request.args.get('num')
    o = organization.Organization(oid, name, status, parent_id, num)
    # print o
    return o.insert()

@fresh_login_required
@organizationBlueprint.route('/remove', methods=['GET'])
def remove():
    id_list = request.args.get('id').split(',')
    print id_list
    return organization.Organization.remove(id_list)

@fresh_login_required
@organizationBlueprint.route('/query',methods=['GET'])
def query():
    oid = request.args.get('id')
    o = organization.Organization.queryById(oid)
    if(o is not None):
        result = o.__dict__
        del result['_sa_instance_state']
        return json.dumps(result)
    else:
        return '500'

@fresh_login_required
@organizationBlueprint.route('/update', methods=['GET'])
def update():
    oid = request.args.get('id')
    name = request.args.get('name')
    status = request.args.get('status')
    parent_id = request.args.get('parent_id')
    num = request.args.get('num')
    o = organization.Organization(oid, name, status, parent_id, num)
    print o
    return o.update()

@fresh_login_required
@organizationBlueprint.route('/listChildsByName')
def listChildsByParentName():
    '''根据节点名称返回它所有孩子节点
    
    Decorators:
        organizationBlueprint.route
    '''
    request.args['name']