# -*- coding: utf-8 -*-
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8");

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
from flask_login import login_required,fresh_login_required,current_user
import json

from models import operate_log
from modelss import Change_Log,Employee,Organization,Dictionary
from extensions import db

#new a blueprint
logBlueprint = Blueprint('logBlueprint', __name__, template_folder = '../templates', static_folder = '../static')

@logBlueprint.route('/')
@fresh_login_required
def index():
    return render_template('logchart_display.html');

@logBlueprint.route('/listAll')
@fresh_login_required
def list_all_logs():
    # print current_user.name
    data = operate_log.Log.listLogsByUserName(current_user.name);
    if data == None :
        return json.dumps([]),200
    else:
        return json.dumps(data),200

@logBlueprint.route('/change/')
@fresh_login_required
def changeLog_index():
    return render_template('logchart_change.html')

@logBlueprint.route('/change/list')
def list_all_changelog():
    try:
        all_data = Change_Log.query.all()
        response = []
        for x in all_data:
            temp = {}
            temp.update(x.to_json())
            employee = Employee.query.filter_by(id = temp['employee_id']).first()
            # print employee
            temp['is_Practice'] = employee.is_Practice
            temp['name'] = (employee.name if employee is not None else None)
            temp['emp_type_name'] = (Dictionary.query.filter_by(id = employee.emp_type).first().name if employee is not None else None)
            temp['position'] = (Dictionary.query.filter_by(id = employee.position_id).first().name if employee is not None else None)
            temp['org'] = (Organization.query.filter_by(id = employee.org_id).first().name if employee is not None else None)
            temp['change_type'] = Change_Log.type_dictionary[temp['change_type']]
            response.append(temp)
        return json.dumps(response)
    except Exception as e:
        raise e

