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
@employeeBlueprint.route('/scan/')
def scan_index():
    return render_template('employee_query.html')

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

# @employeeBlueprint.route('/getemployeebyid', methods=['GET'])
# def get_employeeByid():
#     '''保存当前选中员工的id，并根据员工编号返回该员工的信息
#     首先保存传来的员工id，用于单独标志图片上传
#     然后根据id返回员工信息
#     最后将一些外键从id转换成name
#     Decorators:
#         employeeBlueprint.route
#     '''
#     session['current_employee_id'] = request.args.get('id')
    
#     obj = employee.Employee.getEmployeeById(session['current_employee_id'])
#     if(obj is not None):
#         temp = obj.__dict__
#         del temp['_sa_instance_state']

#         # temp['org_name'] = organization.Organization.getNameById(temp['org_id']); #所属部门id转name
#         # temp['worktype'] = dictionary.Dictionary.getNameById(temp[''])
#         return json.dumps(temp)
#     return None,500

@fresh_login_required
@employeeBlueprint.route('/insertEmployee', methods=['POST'])
def insertEmployee():
    e = employee.Employee(**request.form)
    return 'hello'

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
    '''接收图片，并保存在服务器中，
       生成并返回对应服务器的url，

    Decorators:
        fresh_login_required
        employeeBlueprint.route
    
    Returns:
        [str] -- 图片存放路径
    
    Raises:
        Exception -- 当session['current_employee_id']等于None时
    '''
    file_url = ""
    if request.method == 'POST' and 'photo' in request.files:
        import time
        file = request.files['photo']
        file_name = str(current_user.id) + "_" + str(time.time()).split('.')[0] + "." + request.files['photo'].filename.split('.')[1]
        filename = photos.save(file, name = file_name)
        file_url = photos.url(filename)
        # session['photo_url'] = file_url
        # employee.Employee.updatePhoto(session['current_employee_id'], file_url)
    return file_url


@fresh_login_required
@employeeBlueprint.route('/scan/list_all')
def scan_list_all():
    employee_list = employee.Employee.list_all()
    result = []
    for x in employee_list:
        temp = x.__dict__
        del temp['_sa_instance_state']
        temp['org_name'] = organization.Organization.getNameById(temp['org_id'])
        temp['political_status'] = dictionary.Dictionary.getNameById(temp['political_status_id'])
        result.append(temp)
    print result
    return json.dumps(result)

@fresh_login_required
@employeeBlueprint.route('/detail', methods=['GET'])
def show_detail():
    e = employee.Employee.getEmployeeById(request.args.get('id'))
    # print e.political_status_id
    if( e is not None ):
        cur_employee = {
            'id': e.id, 
            'name': e.name, 
            'old_name': e.old_name,
            'photo_url': e.photo_url,
            'sex': e.sex,
            'id_num': e.id_num,
            'birthdate': e.birthdate,
            'work_date': e.work_date,
            'origin': e.origin,
            'phone1': e.phone1,
            'phone2': e.phone2,
            'address': e.address,
            'email': e.email,
            'others': e.others,
            'emp_type': dictionary.Dictionary.getNameById(e.emp_type),
            'org_name': organization.Organization.getNameById(e.org_id),
            'status': dictionary.Dictionary.getNameById(e.status_id),
            'political_status': dictionary.Dictionary.getNameById(e.political_status_id),
            'position': dictionary.Dictionary.getNameById(e.position_id),
            'nation': dictionary.Dictionary.getNameById(e.nation_id),
            'degree': dictionary.Dictionary.getNameById(e.degree_id),
            'techlevel': dictionary.Dictionary.getNameById(e.techlevel_id)}
        # print cur_employee
        return render_template('employee_detail.html',user = cur_employee)
    return 'error'

@employeeBlueprint.route('/query', methods = ['POST'])
def query_employee():
    '''负责根据id查询员工信息
    
    特点：根据一个或多个id进行查询
    
    Decorators:
        employeeBlueprint.route
    
    Returns:
        [json] -- 查询结果
    '''
    id_list = request.form['id'].split(',')
    result = []
    if(id_list is not None):
        for item in id_list:
            e = employee.Employee.getEmployeeById(item)
            temp = { 
                'id': e.id, 
                'name': e.name,
                'emp_type': dictionary.Dictionary.getNameById(e.emp_type),
                'org_name': organization.Organization.getNameById(e.org_id),
                'position': dictionary.Dictionary.getNameById(e.position_id),
                'status': dictionary.Dictionary.getNameById(e.status_id),
                }
            result.append(temp)
    return json.dumps(result) 
