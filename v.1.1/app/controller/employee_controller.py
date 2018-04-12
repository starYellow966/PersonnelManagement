# -*- coding: utf-8 -*-
# import sys
from models import employee

from flask import Flask,Blueprint,render_template,request,redirect,url_for,session
from flask_login import login_required,fresh_login_required,current_user
from flask_uploads import UploadSet,IMAGES,configure_uploads
import json
from extensions import photos

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

@employeeBlueprint.route('/saveemployeeid', methods=['GET'])
def save_employee_id():
    '''保存当前选中员工的id，并返回该员工的信息
    
    Decorators:
        employeeBlueprint.route
    '''
    session['current_employee_id'] = request.args.get('id')
    obj = employee.Employee.getEmployeeById(session['current_employee_id'])
    temp = obj.__dict__
    del temp['_sa_instance_state']
    return json.dumps(temp)

@fresh_login_required
@employeeBlueprint.route('/uploadPhoto', methods=['POST'])
def upload_photo():
    '''接受图片，并保存到指定路径，数据库存放图片的路径，
    通过session['current_employee_id']确定员工
    
    [description]
    
    Decorators:
        fresh_login_required
        employeeBlueprint.route
    
    Returns:
        [str] -- 图片存放路径
    
    Raises:
        Exception -- 当session['current_employee_id']等于None时
    '''
    if session['current_employee_id'] is None:
        raise Exception
    file_url = ""
    if request.method == 'POST' and 'photo' in request.files:
        import time
        file = request.files['photo']
        file_name = str(current_user.id) + "_" + str(time.time()).split('.')[0] + "." + request.files['photo'].filename.split('.')[1]
        filename = photos.save(file, name = file_name)
        file_url = photos.url(filename)
        employee.Employee.updatePhoto(session['current_employee_id'], file_url)
    return file_url