# -*- coding: utf-8 -*-
# import sys
# from models import employee,organization,dictionary

from flask import Flask,Blueprint,render_template,request,redirect,url_for,session,abort
from flask_login import login_required,fresh_login_required,current_user
from flask_uploads import UploadSet,IMAGES,configure_uploads
import json,time
import flask_excel as excel #excel操作工具包
from extensions import photos,db
from modelss import Employee,Organization,Dictionary,Change_Log


employeeBlueprint = Blueprint('employeeBlueprint', __name__,template_folder = '../templates', 
    static_folder = '../static')


'''
'''
@fresh_login_required
@employeeBlueprint.route('/')
def index():
    '''员工管理首页(url:'/org')
    '''
    return render_template('employee_manger.html')

@fresh_login_required
@employeeBlueprint.route('/scan/')
def scan_index():
    '''员工信息浏览页面
    '''
    return render_template('employee_query.html')

@fresh_login_required
@employeeBlueprint.route('/inside/')
def inside_index():
    '''员工内部变动页面
    '''
    return render_template('employee_inside.html')

@fresh_login_required
@employeeBlueprint.route('/formal/')
def formal_index():
    '''员工定职变动页面
    '''
    return render_template('employee_formal.html')


@fresh_login_required
@employeeBlueprint.route('/insert/')
def insert_index():
    '''新进员工页面
    '''
    return render_template('employee_insert.html')


@fresh_login_required
@employeeBlueprint.route('/batch/')
def batch_index():
    '''批量新进员工页面
    '''
    return render_template('employee_batch.html')

@fresh_login_required
@employeeBlueprint.route('/remove/')
def remove_index():
    '''减少员工页面
    '''
    return render_template('employee_remove.html')

@fresh_login_required
@employeeBlueprint.route('/formal/list/practice')
def list_all_practice():
    '''获得所有实习生数据
    '''
    try:
        data = Employee.query.with_entities(Employee.id, Employee.name, Employee.org_id, Employee.position_id, 
            Employee.emp_type, Employee.sex, Employee.degree_id, Employee.status_id, Employee.is_Practice).filter_by(is_Practice = 1, isUse = 1).all() #获得属于当前节点的员工信息
        response = []
        for x in data:
            temp = {"id": x[0],"name": x[1],'sex':x[5],'is_Practice':x[8]}
            variable = Organization.query.filter_by(id = x[2]).first()
            temp['org_name'] = (variable.name if variable is not None else None)
            variable = Dictionary.query.filter_by(id = x[3]).first()
            temp['position'] = (variable.name if variable is not None else None)
            variable = Dictionary.query.filter_by(id = x[4]).first()
            temp['emp_type_name'] = (variable.name if variable is not None else None)
            variable = Dictionary.query.filter_by(id = x[6]).first()
            temp['degree'] = (variable.name if variable is not None else None)
            variable = Dictionary.query.filter_by(id = x[7]).first()
            temp['status'] = (variable.name if variable is not None else None)
            response.append(temp)
        return json.dumps(response)
    except Exception as e:
        db.session.rollback()
        raise e


@fresh_login_required
@employeeBlueprint.route('/treeAll')
def treeAll():
    '''返回组织表中所有数据，
    格式是treeview接收的格式
    
    注意：organization.Organization.treeAll()要放在一个list再json.dumps，否则前端转换json失败
    '''
    try:
        return json.dumps([Employee.treeAll()])
    except Exception as e:
        db.session.rollback()
        raise e
    

@fresh_login_required
@employeeBlueprint.route('/removeEmployee', methods=['POST'])
def remove():
    '''删除员工操作
    '''
    try:
        # print request.form
        id_list = request.form['id'].split(',')
        for x in id_list:
            e = Employee.query.filter_by(id = x).update({'isUse': 0})
            # 变动日志
            log = Change_Log(request.form['type'], x, request.form['change_date'], request.form['executor'], request.form['others'])
            db.session.add(log)
        db.session.commit()
        return 'success'
    except Exception as e:
        db.session.rollback()
        # print e
        raise e
    


@fresh_login_required
@employeeBlueprint.route('/insertEmployee', methods=['POST'])
def insert():
    '''新增员工操作
    '''
    try:
        if(Employee.query.filter_by(id = request.form['id']).first() is not None):
            return 'id_error'
        e = Employee(**request.form)
        db.session.add(e)

        # 变动日志
        log = Change_Log('I', e.id, time.strftime('%Y-%m-%d',time.localtime(time.time())), current_user.name, None)
        db.session.add(log)
        db.session.commit()
        return 'success'
    except Exception as e:
        db.session.rollback()
        raise e

@fresh_login_required
@employeeBlueprint.route('/updateEmployee', methods=['POST'])
def update():
    '''更新员工操作
    '''
    try:
        Employee.query.filter_by(id = request.form['id']).update({
                'name': request.form['name'],
                'old_name': request.form['old_name'],
                'photo_url': request.form['photo_url'],
                'emp_type': request.form['emp_type'],
                'sex': request.form['sex'],
                'org_id': request.form['org_id'],
                'status_id': request.form['status_id'],
                'position_id': request.form['position_id'],
                'id_num': request.form['id_num'],
                'political_status_id': request.form['political_status_id'],
                'nation_id': request.form['nation_id'],
                'degree_id': request.form['degree_id'],
                'birthdate': request.form['birthdate'],
                'work_date': request.form['work_date'],
                'origin': request.form['origin'],
                'phone1': request.form['phone1'],
                'phone2': request.form['phone2'],
                'address': request.form['address'],
                'email': request.form['email'],
                'techlevel_id': request.form['techlevel_id'],
                'others': request.form['others']
                })
        db.session.commit()
        return 'success'
    except Exception as e:
        db.session.rollback()
        raise e

@fresh_login_required
@employeeBlueprint.route('/change/inside', methods=['POST'])
def inside_change():
    '''员工内部变动操作
    '''
    try:
        id_list = request.form['id'].split(',')
        for x in id_list:
            if x is not None and len(x) > 0:
                Employee.query.filter_by(id = x).update({
                    "org_id": request.form['org_id'],
                    "position_id": request.form['position_id']
                    })
                # 变动日志
                others = u'新部门为' + Organization.query.filter_by(id = request.form['org_id']).first().name + " ，新职位" + Dictionary.query.filter_by(id = request.form['position_id']).first().name + request.form['others']
                log = Change_Log('IC', x, time.strftime('%Y-%m-%d',time.localtime(time.time())), current_user.name, request.form['others'])
                db.session.add(log)
        db.session.commit()
        return 'success'
    except Exception as e:
        db.session.rollback()
        raise e

@fresh_login_required
@employeeBlueprint.route('/formal/update', methods = ['POST'])
def formal_update():
    '''员工定职管理操作
    '''
    try:
        print request.form
        update_dict = {'is_Practice': 0}
        if 'org_id' in request.form:
            update_dict['org_id'] = request.form['org_id']
        if 'position_id' in request.form:
            update_dict['position_id'] = request.form['position_id']
        id_list = request.form['id'].split(',')
        for x in id_list:
            if(x is not None and len(x) > 0):
                Employee.query.filter_by(id = x).update(update_dict)
                # 变动日志
                # others = request.form['others'] + ((u', 新部门' + Organization.query.filter_by(id = update_dict['org_id']).first().name) if update_dict.has_key('org_id') else '') + ((u', 新职位' + Dictionary.query.filter_by(id = update_dict['position_id']).first().name) if update_dict.has_key('position_id') else '')
                log = Change_Log('F', x, time.strftime('%Y-%m-%d',time.localtime(time.time())), current_user.name, request.form['others'])
                db.session.add(log)
        db.session.commit()
        return 'success'
    except Exception as e:
        db.session.rollback()
        raise e

@fresh_login_required
@employeeBlueprint.route('/uploadPhoto', methods=['POST'])
def upload_photo():
    '''接收图片，并保存在服务器中，
       生成并返回对应服务器的url，
    Returns:
        [str] -- 图片存放路径
    '''
    try:
        file_url = ""
        if request.method == 'POST' and 'photo' in request.files:
            import time
            file = request.files['photo']
            file_name = str(current_user.id) + "_" + str(time.time()).split('.')[0] + "." + request.files['photo'].filename.split('.')[1]
            filename = photos.save(file, name = file_name)
            file_url = photos.url(filename)
        return file_url
    except Exception as e:
        db.session.rollback()
        raise e
    


@fresh_login_required
@employeeBlueprint.route('/scan/list_all')
def scan_list_all():
    '''获取所有员工信息
    '''
    try:
        response = []
        for x in Employee.query.filter_by(isUse = 1).order_by(Employee.id).all():
            temp = x.to_json()
            variable = Organization.query.filter_by(id = temp['org_id']).first()
            temp['org_name'] = (variable.name if variable is not None else None)
            
            variable = Dictionary.query.filter_by(id = temp['political_status_id']).first()
            temp['political_status'] = (variable.name if variable is not None else None)
            
            variable = Dictionary.query.filter_by(id = temp['emp_type']).first()
            temp['emp_type_name'] = (variable.name if variable is not None else None)
            
            variable = Dictionary.query.filter_by(id = temp['position_id']).first()
            temp['position'] = (variable.name if variable is not None else None)
            
            variable = Dictionary.query.filter_by(id = temp['degree_id']).first()
            temp['degree'] = (variable.name if variable is not None else None)
            
            variable = Dictionary.query.filter_by(id = temp['status_id']).first()
            temp['status'] = (variable.name if variable is not None else None)

            variable = Dictionary.query.filter_by(id = temp['nation_id']).first()
            temp['nation'] = (variable.name if variable is not None else None)
            response.append(temp)
        return json.dumps(response)
    except Exception as e:
        db.session.rollback()
        raise e

@fresh_login_required
@employeeBlueprint.route('/detail', methods=['GET'])
def show_detail():
    try:
        temp = Employee.query.filter_by(id = request.args['id']).first()
        if temp is not None:
            temp = temp.to_json()
            temp['sex'] = u'男' if temp['sex'] == 1 else (u'女' if temp['sex'] == 0 else None)

            variable = Organization.query.filter_by(id = temp['org_id']).first()
            temp['org_name'] = (variable.name if variable is not None else None)

            variable = Dictionary.query.filter_by(id = temp['political_status_id']).first()
            temp['political_status'] = (variable.name if variable is not None else None)

            variable = Dictionary.query.filter_by(id = temp['emp_type']).first()
            temp['emp_type_name'] = (variable.name if variable is not None else None)

            variable = Dictionary.query.filter_by(id = temp['position_id']).first()
            temp['position'] = (variable.name if variable is not None else None)

            variable = Dictionary.query.filter_by(id = temp['degree_id']).first()
            temp['degree'] = (variable.name if variable is not None else None)

            variable = Dictionary.query.filter_by(id = temp['status_id']).first()
            temp['status'] = (variable.name if variable is not None else None)

            variable = Dictionary.query.filter_by(id = temp['nation_id']).first()
            temp['nation'] = (variable.name if variable is not None else None)

            variable = Dictionary.query.filter_by(id = temp['techlevel_id']).first()
            temp['techlevel'] = (variable.name if variable is not None else None)
            temp['is_Practice'] = u'是' if temp['is_Practice'] == 1 else u'否'
            return render_template('employee_detail.html',user = temp)
        else:
            abort(404)
    except Exception as e:
        db.session.rollback()
        raise e

@employeeBlueprint.route('/query', methods = ['POST'])
def query_employee():
    '''负责根据id查询员工信息    
    特点：根据一个或多个id进行查询
    '''
    try:
        response = []
        for x in request.form['id'].split(','):
            if x is not None and len(x) > 0:
                '''FIXME：非空判断'''
                temp = Employee.query.filter_by(id = x).first().to_json()
                variable = Organization.query.filter_by(id = temp['org_id']).first()
                temp['org_name'] = (variable.name if variable is not None else None)
                variable = Dictionary.query.filter_by(id = temp['status_id']).first()
                temp['status'] = (variable.name if variable is not None else None)
                variable = Dictionary.query.filter_by(id = temp['emp_type']).first()
                temp['emp_type_name'] = (variable.name if variable is not None else None)
                variable = Dictionary.query.filter_by(id = temp['position_id']).first()
                temp['position'] = (variable.name if variable is not None else None)
                response.append(temp)
        return json.dumps(response)
    except Exception as e:
        db.session.rollback()
        raise e


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
        '''专门针对批量新增功能，创建一个employee对象
        
        因为row中的key是字段名用中文表达，所以需要进行字段名转换
        
        Arguments:
            **row {dict} -- excel文件的一行数据
        '''
        # 直接映射表，这些字段可以直接转换
        direct_references = {u'工号': 'id', u'姓名': 'name', u'曾用名': 'old_name',u'籍贯': 'origin', 
            u'身份证号': 'id_num', u'联系电话': 'phone1',u'家庭住址': 'address', u'出生日期': 'birthdate', 
            u'电子邮箱':'email',u'入职日期': 'work_date', u'备注': 'others'}
        # Dictionary类映射表，与字典数据有关的字段
        dictionary_references = {u'用工性质': 'emp_type', u'职名': 'position_id', 
            u'人员状态': 'status_id',u'民族': 'nation_id', u'技能等级': 'techlevel_id', 
            u'学历': 'degree_id',u'政治面貌': 'political_status_id'}
        data = {}
        for x in row:
            if x in direct_references:
                data[direct_references[x]] = row[x]
            elif x in dictionary_references:
                d = Dictionary.query.filter_by(name = row[x]).first()
                data[dictionary_references[x]] = (d.id if d is not None else None)
            elif x == u'所属部门':
                o = Organization.query.filter_by(name = row[x]).first()
                data['org_id'] = (o.id if o is not None else None)
            elif x == u'性别':
                data['sex'] = (1 if row[x] == u'男' else 0)
            elif x == u'是否实习':
                data['is_Practice'] = (1 if row[x] == u'是' else 0)
        return Employee(**data)
    try:
        request.save_book_to_database(field_name='file',session=db.session,
            tables=[Employee],initializers=[employee_init_func]);
    except Exception as e:
        #FIXME：当sheet名不等于表名时，会报‘No suitable database adapter found!’
        message = 'fail,请检查excel文件，其中不能修改sheet名，工号不能重复'
        db.session.rollback()
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