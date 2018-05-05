# -*- coding: utf-8 -*-
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8");

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
from flask_login import login_required,fresh_login_required,current_user
import json

from models import dictionary,operate_log,response_object
from extensions import db

#new a blueprint
dictionaryBlueprint = Blueprint('dictionaryBlueprint', __name__, template_folder = '../templates', static_folder = '../static', url_prefix = '/dict');


@dictionaryBlueprint.route('/')
@fresh_login_required
def index():
    '''数据字典管理首页(url:'/dict')
      
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    
    Returns:
        [html] -- 首页
    '''
    return render_template('dictionaryindex.html');

@fresh_login_required
@dictionaryBlueprint.route('/listAll', methods = ['GET'])
def list_all_type():
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
    if (data.data == None):
        data.data = []
    return json.dumps(data.data),200;


@dictionaryBlueprint.route('/listDictByTypeId', methods = ['GET'])
@fresh_login_required
def list_dictionarys_by_type_id():
    '''根据字典类型id返回同类型的所有字典数据
    
    用于页面表格数据
    
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    
    Returns:
        [json] -- 字段有{id, name}
    '''
    type_id = request.args['id']
    data = dictionary.Dictionary.listDictByTypeId(type_id)
    if (data.data == None):
        data.data = []
    return json.dumps(data.data),200;

@dictionaryBlueprint.route('/listDictByTypeName', methods = ['GET'])
@fresh_login_required
def list_dictionarys_by_type_name():
    '''根据字典类型名字返回同类型的所有字典数据
    
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    '''
    type_name = request.args['type']
    data = dictionary.Dictionary.listDictByTypeName(type_name)
    if (data.data == None):
        data.data = []
    return json.dumps(data.data),200

@dictionaryBlueprint.route('/remove', methods = ['GET'])
@fresh_login_required
def remove():
    '''删除字典数据
    
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    
    Returns:
        [str] -- 响应码 success，fail
    '''
    return dictionary.Dictionary.remove(request.args['target_string']).data

@dictionaryBlueprint.route('/update', methods = ['POST'])
@fresh_login_required
def update():
    '''更新字典数据
    
    [description]
    
    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    
    Returns:
        [str] -- 响应码 success，fail
    '''
    return dictionary.Dictionary(request.form['id'], request.form['name'], None).update().data


@dictionaryBlueprint.route('/insert', methods = ['GET'])
@fresh_login_required
def insert():
    '''插入字典数据

    Decorators:
        dictionaryBlueprint.route
        fresh_login_required
    
    Returns:
        [str] -- 响应码 success，fail, id_error
    '''
    return dictionary.Dictionary(request.args['id'], request.args['name'], request.args['type_id']).insert().data


@dictionaryBlueprint.route('/download',methods = ['GET'])
def dictionary_download():
    '''创建一个excel文件，是批量导入时指定文件
    
    内含填写数据的格式，需要按照文件中的字段填写数据
    FIXME: 提示用户需要关闭迅雷插件
    
    Decorators:
        dictionaryBlueprint.route
    
    Returns:
        [excel文件] -- 模板
    '''
    id = request.args['id'];
    type_name = dictionary.DictionaryType.get_name_by_id(id).data;
    #这个sheet名很重要，必须是类名，否则上传就会报错
    response = excel.make_response_from_array([[u'编号', u'名称']], 
        "xls",file_name= type_name + u"信息批量导入表",sheet_name='Dictionary');
    # print response;
    return response

@dictionaryBlueprint.route('/unload', methods = ['POST'])
@fresh_login_required
def dictionary_unload():
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
        return seg
    try:
        request.save_book_to_database(field_name='file',session=db.session,
            tables=[dictionary.Dictionary],initializers=[dictionary_init_func]);
        return redirect(url_for('dictionaryBlueprint.index'));
    except Exception as e:
        #FIXME：当sheet名不等于表名时，会报‘No suitable database adapter found!’
        raise e
        return "文件上传失败，请检查excel文件，其中不能修改sheet名，编号不能重复";

# '''返回一个装有所有Dictionary表数据的excel文件

# 通过flask_excel.make_response_from_tables
# :return : 含有Organization表所有数据的excel文件
# '''
# #验证了db.session没错
# @dictionaryBlueprint.route("/exportAll", methods=['GET'])
# def doexport():
#     return excel.make_response_from_tables(db.session, [dictionary.Dictionary], "xls")