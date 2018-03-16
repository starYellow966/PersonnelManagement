# -*- coding: utf-8 -*-
#上面注释是为了告诉Python解释器，按照UTF-8编码读取源代码
import sys 
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask,render_template,Blueprint,request
# from flask_httpauth import HTTPBasicAuth
import flask_excel as excel #excel操作工具包
from controller import organizationBlueprint
from models import organization
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = 'i do not know how to use this one'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8';
# db = SQLAlchemy(app)
# 
# 注册蓝图
app.register_blueprint(organizationBlueprint);

'''人事管理首页

:return : index.html
:date : 2018/3/13
'''
@app.route('/')
def index():
    return render_template('index.html');

'''上传excel文件

TODO: 自动跳过重复信息
:return : 成功重定向到'/seg'；反之，错误提示
:date : 2018/3/14
'''
# @app.route('/unload', methods = ['GET','POST'])
# def segmentUnload():
#     if request.method == 'POST':
#         '''将excel中每行数据读取并封装成Segment对象
        
#         :return ：Organization对象或者None
#         '''
#         def segment_init_func(row):
#             seg = organization.Organization.createSegment(row[u'编号'], row[u'名称'], row[u'所属路局']);
#             #当创建失败seg==None
#             print seg;
#             return seg;

#         try:
#             request.save_book_to_database(field_name='file',session=db.session,
#                 tables=[organization.Organization],initializers=[segment_init_func]);
#             return "saved",200;
#         except Exception as e:
#             #FIXME：当sheet名不等于Organization时，会报‘No suitable database adapter found!’
#             print e;
#             return "文件上传失败，请检查excel文件，其中不能修改sheet名，编号不能重复";
#     return '''
#     <!doctype html>
#     <title>Upload an excel file</title>
#     <h1>Excel file upload (xls, xlsx, ods please)</h1>
#     <form action="" method=post enctype=multipart/form-data><p>
#     <input type=file name=file><input type=submit value=Upload>
#     </form>
#     '''


if __name__ == '__main__':
    excel.init_excel(app); # required since version 0.0.7
    app.run(debug = True);