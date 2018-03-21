# -*- coding: utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
from flask_login import login_required,fresh_login_required,current_user
import json

sys.path.append("..");#修改路径，为了引用models包
from models import operate_log

#new a blueprint
logBlueprint = Blueprint('logBlueprint', __name__, template_folder = '../templates', static_folder = '../static', url_prefix = '/log')

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