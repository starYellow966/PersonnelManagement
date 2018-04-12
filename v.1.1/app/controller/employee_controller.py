# -*- coding: utf-8 -*-
# import sys
from models import employee,organization,dictionary

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
    return render_template('employee_manger.html')

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

@employeeBlueprint.route('/getemployeebyid', methods=['GET'])
def get_employeeByid():
    '''保存当前选中员工的id，并根据员工编号返回该员工的信息
    首先保存传来的员工id，用于单独标志图片上传
    然后根据id返回员工信息
    最后将一些外键从id转换成name
    Decorators:
        employeeBlueprint.route
    '''
    session['current_employee_id'] = request.args.get('id')
    
    obj = employee.Employee.getEmployeeById(session['current_employee_id'])
    temp = obj.__dict__
    del temp['_sa_instance_state']

    # temp['org_name'] = organization.Organization.getNameById(temp['org_id']); #所属部门id转name
    # temp['worktype'] = dictionary.Dictionary.getDictionaryById(temp[''])

    return json.dumps(temp)

@fresh_login_required
@employeeBlueprint.route('/updateemployee', methods=['POST'])
def update_employee():
    e = employee.Employee(request.form['id'], request.form['name'], request.form['sex'], 
        request.form['org_id'])
    response_code = e.update_employee()
    if(response_code == 200 ):
        return 'successfully'
    else:
        return 'fail'

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