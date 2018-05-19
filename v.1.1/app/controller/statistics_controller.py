# -*- coding: utf-8 -*-

from models import employee,organization,dictionary
from flask import Flask,Blueprint,render_template,request,redirect,url_for,session
from flask_login import login_required,fresh_login_required,current_user
import json
from extensions import db
from modelss import Employee,Organization,Dictionary,Change_Log
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
@statisticsBlueprint.route('/change/')
def change_index():
    return render_template('statistics_changelog.html')

@fresh_login_required
@statisticsBlueprint.route('/column/<column_name>', methods = ['GET'])
def statistics_column(column_name):
    try:
        return json.dumps(get_column_data(column_name))
    except Exception as e:
        raise e

@fresh_login_required
@statisticsBlueprint.route('/pie/<column_name>', methods = ['GET'])
def statistics_pie(column_name):
    try:
        response = get_column_data(column_name)
        total_count = db.session.execute('select count(1) from Employee where isUse=1').fetchall()[0][0]
        for x in response:
            x['value'] = round(x['value']* 100.0 / total_count, 1)
        return json.dumps(response)
    except Exception as e:
        raise e

@fresh_login_required
@statisticsBlueprint.route('/change/list', methods = ['GET'])
def statistics_changelog():
    try:
        result = Change_Log.query.with_entities(Change_Log.change_date, Change_Log.change_type).all()
        response = []
        for x in result:
            

        sql = 'select change_type, count(*) from gdesignV1_1.Change_Log group by change_type'
        result = db.session.execute(sql).fetchall()
        return json.dumps([dict(result)])
    except Exception as e:
        raise e

def get_column_data(column_name):
    '''获得柱状图统计数据
    '''
    color = ['#3A68D3', '#9F2626', '#2A962A', '#3895BF', '#4267BE', '#4F7DE7', '#7A3C9C', '#B97944', 
            '#782A56', '#484848', '#FFFF33', '#FF3333', '#FFCC33', '#009966', '#99CC00']
    try:
        sql = 'select {0}, count(*) from Employee where isUse=1 group by {0} order by count(*) desc'.format(column_name)
        result = db.session.execute(sql).fetchall()
        index = 0
        response = []
        for x in result:
            temp = {'name':'', 'value':'', 'color':color[index]}
            index = (index + 1) % len(color) #循环区颜色
            if column_name == 'sex':
                temp['name'] = u'男' if x[0] == 1 else u'女'
            else:
                variable = None
                if column_name == 'org_id':
                    variable = Organization.query.filter_by(id = x[0]).first()
                else:
                    variable = Dictionary.query.filter_by(id = x[0]).first()
                if variable is not None:
                    temp['name'] = variable.name
                else:
                    continue
            temp['value'] = x[1]
            response.append(temp)
        return response
    except Exception as e:
        raise e