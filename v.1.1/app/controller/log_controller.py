# -*- coding: utf-8 -*-
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8");

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
from flask_login import login_required,fresh_login_required,current_user
import json

from models import operate_log
from modelss import Change_Log,Employee,Organization,Dictionary,General_Log
from extensions import db

#new a blueprint
logBlueprint = Blueprint('logBlueprint', __name__, template_folder = '../templates', static_folder = '../static')

@logBlueprint.route('/')
@fresh_login_required
def index():
    return render_template('logchart_sys.html');

@logBlueprint.route('/listAll')
@fresh_login_required
def list_all_logs():
    try:
        result = General_Log.query.all()
        response = []
        for x in result:
            response.append(x.to_json())
        # print response
        return json.dumps(response)
    except Exception as e:
        db.session.rollback()
        raise e

@logBlueprint.route('/change/')
@fresh_login_required
def changeLog_index():
    return render_template('logchart_change.html')

@logBlueprint.route('/change/list')
@fresh_login_required
def list_all_changelog():
    try:
        all_data = Change_Log.query.all()
        response = to_chart_json(all_data)
        return json.dumps(response)
    except Exception as e:
        db.session.rollback()
        raise e


@logBlueprint.route('/change/query', methods = ['POST'])
@fresh_login_required
def list_detail_query():
    try:
        months = request.form['months'] + "%"
        from sqlalchemy import and_
        result = Change_Log.query.filter(and_(Change_Log.change_date.like(months), Change_Log.change_type == request.form['type'])).all()
        response = to_chart_json(result)
        # print response
        return json.dumps(response)
    except Exception as e:
        db.session.rollback()
        raise e

def to_chart_json(all_data):
    try:
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
        return response
    except Exception as e:
        raise e