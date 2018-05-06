# -*- coding: utf-8 -*-
# import sys
from models import employee,organization,dictionary

from flask import Flask,Blueprint,render_template,request,redirect,url_for,session
from flask_login import login_required,fresh_login_required,current_user
from flask_uploads import UploadSet,IMAGES,configure_uploads
import json
import flask_excel as excel #excel操作工具包
from extensions import photos,db

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
@employeeBlueprint.route('/change/')
def change_index():
    return render_template('employee_change.html')

@fresh_login_required
@employeeBlueprint.route('/formal/')
def formal_index():
    return render_template('employee_formal.html')

# @fresh_login_required
# @employeeBlueprint.route('/formal')
# def formal_update():
#     return employee.Employee.formal_update(**request.form).data

@fresh_login_required
@employeeBlueprint.route('/change/insert')
def insert_index():
    return render_template('employee_insert.html')


@fresh_login_required
@employeeBlueprint.route('/change/batch')
def batch_index():
    return render_template('employee_batch.html')

@fresh_login_required
@employeeBlueprint.route('/change/remove')
def remove_index():
    return render_template('employee_remove.html')

@fresh_login_required
@employeeBlueprint.route('/formal/list/practice')
def list_all_practice():
    data = employee.Employee.list_all_practice().data
    for x in data:
        x['org_name'] = organization.Organization.getNameById(x['org_id'])
        x['position'] = dictionary.Dictionary.getNameById(x['position_id']).data
        x['emp_type_name'] = dictionary.Dictionary.getNameById(x['emp_type']).data
    return json.dumps(data)


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

@fresh_login_required
@employeeBlueprint.route('/removeEmployee', methods=['POST'])
def remove():
    return employee.Employee.remove(request.form['id'].split(',')).message
    


@fresh_login_required
@employeeBlueprint.route('/insertEmployee', methods=['POST'])
def insert():
    # print request.form
    e = employee.Employee(**request.form)
    return e.insert().data

@fresh_login_required
@employeeBlueprint.route('/updateEmployee', methods=['POST'])
def update():
    e = employee.Employee(**request.form)
    # print e.__dict__
    return e.update().data

@fresh_login_required
@employeeBlueprint.route('/change/inside', methods=['POST'])
def inside_change():
    return employee.Employee.inside_change(**request.form).data

@fresh_login_required
@employeeBlueprint.route('/formal/update', methods = ['POST'])
def formal_update():
    print request.form
    return employee.Employee.formal_update(**request.form).data

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
    return file_url


@fresh_login_required
@employeeBlueprint.route('/scan/list_all')
def scan_list_all():
    employee_list = employee.Employee.list_all().data
    for x in employee_list:
        x['org_name'] = organization.Organization.getNameById(x['org_id'])
        x['political_status'] = dictionary.Dictionary.getNameById(x['political_status_id']).data
        x['emp_type_name'] = dictionary.Dictionary.getNameById(x['emp_type']).data
        x['position'] = dictionary.Dictionary.getNameById(x['position_id']).data
        x['degree'] = dictionary.Dictionary.getNameById(x['degree_id']).data
        x['status'] = dictionary.Dictionary.getNameById(x['status_id']).data
    return json.dumps(employee_list)

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
            'sex': u'男' if e.sex == 1 else u'女',
            'id_num': e.id_num,
            'birthdate': e.birthdate,
            'work_date': e.work_date,
            'origin': e.origin,
            'phone1': e.phone1,
            'address': e.address,
            'email': e.email,
            'others': e.others,
            'emp_type': dictionary.Dictionary.getNameById(e.emp_type).data,
            'org_name': organization.Organization.getNameById(e.org_id),
            'status': dictionary.Dictionary.getNameById(e.status_id).data,
            'political_status': dictionary.Dictionary.getNameById(e.political_status_id).data,
            'position': dictionary.Dictionary.getNameById(e.position_id).data,
            'nation': dictionary.Dictionary.getNameById(e.nation_id).data,
            'degree': dictionary.Dictionary.getNameById(e.degree_id).data,
            'techlevel': dictionary.Dictionary.getNameById(e.techlevel_id).data,
            'is_Practice': u'是' if e.is_Practice == 1 else u'否'}
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
    id_list = request.form['id'].split(',') #id的格式是1,3,4, 注意最后多余的逗号
    result = []
    if(id_list is not None):
        for item in id_list:
            e = employee.Employee.getEmployeeById(item)
            if e is not None:
                temp = {}
                temp.update(e.__dict__)
                del temp['_sa_instance_state']
                temp['emp_type_name'] = dictionary.Dictionary.getNameById(e.emp_type).data
                temp['org_name'] = organization.Organization.getNameById(e.org_id)
                temp['position'] = dictionary.Dictionary.getNameById(e.position_id).data
                temp['status'] = dictionary.Dictionary.getNameById(e.status_id).data
                result.append(temp)
    return json.dumps(result) 


@employeeBlueprint.route('/change/batch/download',methods = ['GET'])
def batch_download():
    array = request.args['request_str'].split(',')
    #这个sheet名很重要，必须是类名，否则上传就会报错
    response = excel.make_response_from_array([array], 
        "xls",file_name= u"人员信息批量导入表",sheet_name='Employee')
    return response

@employeeBlueprint.route('/change/batch/upload', methods = ['POST'])
@fresh_login_required
def batch_unload():
    '''上传excel文件
    
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    
    Raises:
        e -- 所有异常
    '''
    message = 'success'
    def employee_init_func(row):
        # print type(row)
        #当创建失败seg==None
        return employee.Employee.create_employee_cn(**row)
    try:
        request.save_book_to_database(field_name='file',session=db.session,
            tables=[employee.Employee],initializers=[employee_init_func]);
    except Exception as e:
        #FIXME：当sheet名不等于表名时，会报‘No suitable database adapter found!’
        message = 'fail,请检查excel文件，其中不能修改sheet名，工号不能重复'
        print e
        raise e
    finally:
        return message



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