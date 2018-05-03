# -*- coding: utf-8 -*-
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8");

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
from flask_login import login_required,fresh_login_required,current_user
import json

from models import dictionary,operate_log

#new a blueprint
dictionaryBlueprint = Blueprint('dictionaryBlueprint', __name__, template_folder = '../templates', static_folder = '../static', url_prefix = '/dict');

'''数据字典管理首页(url:'/dict')

:return : 首页
:date : 2018/3/17
'''
@dictionaryBlueprint.route('/')
@fresh_login_required
def index():
    return render_template('dictionaryindex.html');

'''返回所有数据字典类型的信息
用于响应页面的侧方标签栏的数据请求

:return : json,字段有{id, name}
:date : 2018/3/17
'''
@fresh_login_required
@dictionaryBlueprint.route('/listAll', methods = ['GET'])
def listAllType():
    '''返回dictionaryindex.html中侧方菜单的数据
    
    首先，获得所有字典类型数据
    然后，转成json传给前端，用于侧方菜单的数据
    
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    
    Returns:
        [json] -- 所有字典类型数据
    '''
    data = dictionary.DictionaryType.listAll();#listAll()失败时返回None
    if (data == None):
        data = []
    return json.dumps(data),200;

'''根据字典类型id返回同类型的所有字典数据
用于页面表格数据

:return : json,字段有{id, name}
:date : 2018/3/17
'''
@dictionaryBlueprint.route('/listDictByTypeId', methods = ['GET'])
@fresh_login_required
def listDictByTypeId():
    type_id = request.args['id']
    data = dictionary.Dictionary.listDictByTypeId(type_id)
    # operate_log.Log.createLog(current_user.name, request.remote_addr, u'Query', 
        # u'查询所有' + dictionary.DictionaryType.getNameById(type_id) + '数据',data == None)
    if (data == None):
        data = []
    return json.dumps(data),200;

@dictionaryBlueprint.route('/listDictByTypeName', methods = ['GET'])
@fresh_login_required
def listDictByTypeName():
    '''根据字典类型名字返回同类型的所有字典数据
    
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    '''
    type_name = request.args['type']
    data = dictionary.Dictionary.listDictByTypeName(type_name)
    if (data == None):
        data = []
    return json.dumps(data),200;

'''删除字典数据

:return : 响应码 success，failure
:date : 2018/3/17
'''
@dictionaryBlueprint.route('/remove', methods = ['GET'])
@fresh_login_required
def removeDict():
    # response_code = 'success'
    # try:
    #     if (dictionary.Dictionary.remove(request.args['target_string'])['message'] ==500):
    #         response_code = 'failure'
    # except Exception as e:
    #     response_code = 'failure'
    #     raise e
    # finally:
    return dictionary.Dictionary.remove(request.args['target_string'])['data']

'''更新字典数据

:return : 响应码 success,failure
:date : 2018/3/18
'''
@dictionaryBlueprint.route('/update', methods = ['POST'])
@fresh_login_required
def updateDict():
    # print "reach middle level";
    # response_code = 'success';
    # try:
    #     d = dictionary.Dictionary(request.form['id'], request.form['name'], None)
    #     if(d.update()['message'] == 500):
    #         response_code = 'failure';
    # except Exception as e:
    #     raise e
    #     response_code = 'failure'
    # finally:
    #     return response_code
    return dictionary.Dictionary(request.form['id'], request.form['name'], None).update()['data']

'''插入字典数据

:return : 响应码 success,failure,id_error
:date : 2018/3/18
'''
@dictionaryBlueprint.route('/insert', methods = ['GET'])
@fresh_login_required
def insertDict():
    # response_code = 'success';
    # try:
    #     d = dictionary.Dictionary(request.args['id'], request.args['name'], request.args['type_id']);
    #     response = d.insert();
    #     if(response == 500):
    #         response_code = 'failure';
    #     elif (response == 300):
    #         response_code = 'id_error';
    # except Exception as e:
    #     raise e;
    #     response_code = 'failure';
    # finally:
    #     return response_code;
    return dictionary.Dictionary(request.args['id'], request.args['name'], request.args['type_id']).insert()['data']

'''下载一个excel文件，是批量导入时指定文件

内含填写数据的格式，需要按照文件中的字段填写数据
FIXME: 提示用户需要关闭迅雷插件

:return : excel文件
'''
@dictionaryBlueprint.route('/download',methods = ['GET'])
def dictionaryDownload():
    id = request.args['id'];
    type_name = dictionary.DictionaryType.getNameById(id);
    #这个sheet名很重要，必须是类名，否则上传就会报错
    response = excel.make_response_from_array([[u'编号', u'名称']], 
        "xls",file_name= type_name + u"信息批量导入表",sheet_name='Dictionary');
    # print response;
    return response;

@dictionaryBlueprint.route('/unload', methods = ['POST'])
@fresh_login_required
def dictionaryUnload():
    '''上传excel文件
    
    TODO(hx): 自动跳过重复信息
    
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    
    Returns:
        [string] -- 成功重定向到'/seg'；反之，错误提示
    
    Raises:
        e -- 所有异常
    '''
    def dictionary_init_func(row):
        seg = dictionary.Dictionary(row[u'编号'], row[u'名称'], int(request.form['unload_type_id']));
        #当创建失败seg==None
        # print seg;
        return seg;
    insert_log = operate_log.Log.createLog(u'Batch', u'向' + dictionary.DictionaryType.getNameById(request.form['unload_type_id']) + u'批量导入')
    try:
        request.save_book_to_database(field_name='file',session=dictionary.Dictionary.getSession(),
            tables=[dictionary.Dictionary],initializers=[dictionary_init_func]);
        insert_log.insertLog()
        return redirect(url_for('dictionaryBlueprint.index'));
    except Exception as e:
        #FIXME：当sheet名不等于表名时，会报‘No suitable database adapter found!’
        raise e;
        insert_log.setStatus(False)
        insert_log.insertLog()
        return "文件上传失败，请检查excel文件，其中不能修改sheet名，编号不能重复";

'''返回一个装有所有Dictionary表数据的excel文件

通过flask_excel.make_response_from_tables
:return : 含有Organization表所有数据的excel文件
'''
#验证了db.session没错
@dictionaryBlueprint.route("/exportAll", methods=['GET'])
def doexport():
    return excel.make_response_from_tables(dictionary.Dictionary.getSession(), [dictionary.Dictionary], "xls")