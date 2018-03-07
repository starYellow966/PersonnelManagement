# -*- coding: utf-8 -*-
#上面注释是为了告诉Python解释器，按照UTF-8编码读取源代码
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

from flask import Flask,render_template,Blueprint,request
from flask_httpauth import HTTPBasicAuth
import flask_excel as excel #excel操作工具包
from orgManagement import org_manage
from models import segment
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = 'i do not know how to use this one'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesign?charset=utf8'
db = SQLAlchemy(app)

#注册蓝图
app.register_blueprint(org_manage)


@app.route("/")
def hello():
    return render_template('index.html')

# @app.route("/download", methods=['GET'])
# def download_file():
# 	response = excel.make_response_from_array([['id','name','stype','dep_name','seg_date','railway']], "xls",file_name="export_data");#如果是谷歌浏览器，不能有迅雷插件
# 	print response;
# 	return response;

# @app.route("/import", methods=['GET', 'POST'])
# def doimport():
#     if request.method == 'POST':
#         def segment_init_func(row):
#         	#将datetime时间转成时间戳存在seg_date
#         	import time,datetime
#         	t = row['seg_date'].timetuple();
#         	seg_date = int(time.mktime(t));
#         	print type(row['id'])
#         	print type(row['name'])
#         	print type(row['dep_name'])
#         	print type(row['railway'])
#         	seg = segment.Segment(row['id'], row['name'],row['dep_name'], seg_date, row['railway'],row['stype']);
#         	print seg;
#         	return seg
#         #Warning：注意导入的xls文件中只能有一个sheet，同时sheet名字为数据库表名
#         request.save_book_to_database(
#             field_name='file', session=db.session,
#             tables=[segment.Segment],
#             initializers=[segment_init_func])
#         return "Saved"
#     return '''
#     <!doctype html>
#     <title>Upload an excel file</title>
#     <h1>Excel file upload (xls, xlsx, ods please)</h1>
#     <form action="" method=post enctype=multipart/form-data><p>
#     <input type='file' name='file'><input type='submit' value='Upload'>
#     </form>
#     '''
# #验证了db.session没错
# @app.route("/export", methods=['GET'])
# def doexport():
#     return excel.make_response_from_tables(db.session, [segment.Segment], "xls")

if __name__ == '__main__':
	excel.init_excel(app) # required since version 0.0.7
	app.run(debug=True)