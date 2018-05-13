# -*- coding: utf-8 -*-
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8")

# print sys.path

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
from flask_login import login_required,fresh_login_required,current_user
import json

from modelss import Organization
from extensions import db

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
    return render_template('organization_index.html')

@fresh_login_required
@organizationBlueprint.route('/treeall')
def treeAll():
    '''返回组织表中所有数据，
    格式是treeview接收的格式
    
    注意：organization.Organization.treeAll()要放在一个list再json.dumps，否则前端转换json失败
    '''
    try:
        return json.dumps([Organization.treeAll()])
    except Exception as e:
        db.session.rollback()
        raise e
    

@fresh_login_required
@organizationBlueprint.route('/listall', methods=['GET'])
def list_all():
    '''返回所有组织信息
    Returns:
        [type] -- 类型，1代表需要组织详细信息，其他代表只需要组织编号和名字信息
    '''
    try:
        query_type = request.args['type']
        response = []
        if(query_type == 1):
            result = Organization.query.filter_by(isUse = 1).order_by(Organization.level, Organization.num).all()
            for x in result:
                response.append(x.to_json)
            return json.dumps([response])
        else:
            result = Organization.query.with_entities(Organization.id, Organization.name).filter_by(isUse = 1).order_by(Organization.level, Organization.num).all()
            for x in result:
                response.append({"id": x[0], "name": x[1]})
            return json.dumps(response)
    except Exception as e:
        db.session.rollback()
        raise e
    
@fresh_login_required
@organizationBlueprint.route('/insert', methods=['POST'])
def insert():
    try:
        org = Organization(**request.form)
        if((Organization.query.filter_by(id = org.id).first()) is not None):
            return 'id_error'
        if((Organization.query.filter_by(name = org.name).first()) is not None):
            return 'name_error'
        db.session.add(org)
        db.session.commit()
        return 'success'
    except Exception as e:
        db.session.rollback()
        raise e

@fresh_login_required
@organizationBlueprint.route('/<int:id>',methods=['GET'])
def query(id):
    try:
        org = Organization.query.filter_by(id = id).first()
        if(org is not None):
            return json.dumps(org.to_json())
        else:
            return '500'
    except Exception as e:
        raise e

@fresh_login_required
@organizationBlueprint.route('/update', methods=['POST'])
def update():
    try:
        org = Organization(**request.form)
        result = Organization.query.filter_by(id = request.form['id']).first()
        if(result is not None and org is not None):
            result.name = org.name
            result.num = org.num
            result.level = org.level
            result.status = org.status
            result.parent_id = org.parent_id
            db.session.add(result)
            db.session.commit()
        return 'success'
    except Exception as e:
        db.session.rollback()
        raise e
@fresh_login_required
@organizationBlueprint.route('/remove', methods=['POST'])
def remove():
    try:
        id_list = request.form['id'].split(',')
        for x in id_list:
            if(x is not None or len(x) > 0):
                org = Organization.query.filter_by(id = x).first()
                if(org is not None):
                    org.isUse = 0
                    db.session.add(org)
                    db.session.commit()
        return 'success'
    except Exception as e:
        db.session.rollback()
        raise e

@organizationBlueprint.route('/download',methods = ['GET'])
def download():
    '''创建一个excel文件，是批量导入时指定文件
    内含填写数据的格式，需要按照文件中的字段填写数据
    FIXME: 提示用户需要关闭迅雷插件
    
    Returns:
        [excel文件] -- 模板
    '''
    #这个sheet名很重要，必须是类名，否则上传就会报错
    response = excel.make_response_from_array([[u'编号', u'名称', u'是否为虚拟节点', u'所属上级',u'序号']], 
        "xls",file_name= u"组织机构批量导入表",sheet_name='Organization');
    # print response;
    return response

@organizationBlueprint.route('/upload', methods = ['POST'])
@fresh_login_required
def upload():
    '''上传excel文件
    
    TODO(hx): 自动跳过重复信息
    
    Decorators:
        organizationBlueprint.route
        fresh_login_required
    
    Returns:
        [string] -- 成功重定向到'/seg'；反之，错误提示
    
    Raises:
        e -- 所有异常
    '''
    def organization_init_func(row):
        parent = Organization.query.filter_by(name = row[u'所属上级']).first()
        if(parent is not None):
            o = Organization(row[u'编号'],row[u'名称'],(0 if row[u'是否为虚拟节点'] == u'是' else 0),parent.id, row[u'序号'])
            return (o if Organization.query.filter_by(id = o.id).first() is None or Organization.query.filter_by(name = o.name).first() else None)
        else:
            return None
    try:
        request.save_book_to_database(field_name='file',session=db.session,
            tables=[Organization],initializers=[organization_init_func]);
        return u'success'
    except Exception as e:
        #FIXME：当sheet名不等于表名时，会报‘No suitable database adapter found!’
        raise e
        return u'fail';


# @fresh_login_required
# @organizationBlueprint.route('/listChildsByName')
# def listChildsByParentName():
#     '''根据节点名称返回它所有孩子节点
    
#     Decorators:
#         organizationBlueprint.route
#     '''
#     request.args['name']