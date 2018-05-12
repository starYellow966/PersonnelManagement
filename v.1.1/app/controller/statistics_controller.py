# -*- coding: utf-8 -*-

from models import employee,organization,dictionary
from flask import Flask,Blueprint,render_template,request,redirect,url_for,session
from flask_login import login_required,fresh_login_required,current_user
import json

statisticsBlueprint = Blueprint('statisticsBlueprint', __name__,template_folder = '../templates', 
    static_folder = '../static')


'''员工管理首页(url:'/org')

:return : 首页
:date : 2018/4/6
'''
@fresh_login_required
@statisticsBlueprint.route('/')
def index():
    return render_template('statistics_base.html')

@fresh_login_required
@statisticsBlueprint.route('/column', methods = ['GET'])
def get_column_data():
    return json.dumps(employee.Employee.statistics_column(request.args['type']).data)

@fresh_login_required
@statisticsBlueprint.route('/pie', methods = ['GET'])
def get_pie_data():
    return json.dumps(employee.Employee.statistics_pie(request.args['type']).data)