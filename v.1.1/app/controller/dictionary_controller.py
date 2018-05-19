# -*- coding: utf-8 -*-
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8");

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
from flask_login import login_required,fresh_login_required,current_user
import json
from modelss import DictionaryType, Dictionary
from extensions import db

#new a blueprint
dictionaryBlueprint = Blueprint('dictionaryBlueprint', __name__, template_folder = '../templates', static_folder = '../static');


@dictionaryBlueprint.route('/')
@fresh_login_required
def index():
    return render_template('dictionary_index.html');

@fresh_login_required
@dictionaryBlueprint.route('/types', methods = ['GET'])
def list_all_type():
    '''返回dictionaryindex.html中侧方菜单的数据
    
    首先，获得所有字典类型数据
    然后，转成json传给前端，用于侧方菜单的数据

    Returns:
        [json] -- 所有字典类型数据
    '''
    try:
        data = []
        type_list = DictionaryType.query.filter_by(isUse = 1).order_by(DictionaryType.id).all()
        for x in type_list:
            data.append(x.to_json())
        return json.dumps(data)
    except Exception as e:
        # abort(500)
        raise e
    


@dictionaryBlueprint.route('/dictionarys/<int:type_id>', methods = ['GET'])
@fresh_login_required
def list_dictionarys_by_type_id(type_id):
    '''根据字典类型id返回同类型的所有字典数据
       用于页面表格数据

    Returns:
        [json] -- 字段有{id, name}
    '''
    try:
        response = []
        result = Dictionary.query.filter_by(isUse = 1, type_id = type_id).order_by(Dictionary.id).all()
        for x in result:
            response.append(x.to_json())
        return json.dumps(response)
    except Exception as e:
        raise e

@dictionaryBlueprint.route('/insert', methods = ['POST'])
@fresh_login_required
def insert():
    try:
        if(Dictionary.query.filter_by(id = request.form['id']).first() == None):
            dictionary = Dictionary(**request.form)
            db.session.add(dictionary)
            db.session.commit()
            return u'success'
        else:
            return 'id_error'
    except Exception as e:
        db.session.rollback()
        raise e

@dictionaryBlueprint.route('/update', methods = ['POST'])
@fresh_login_required
def update():
    try:
        dictionary = Dictionary.query.filter_by(id = request.form['id']).first()
        if(dictionary != None):
            dictionary.name = request.form['name']
            db.session.add(dictionary)
            db.session.commit()
            return u'success'
        else:
            return 'fail'
    except Exception as e:
        db.session.rollback()
        raise e

@dictionaryBlueprint.route('/remove', methods = ['POST'])
@fresh_login_required
def remove():
    try:
        target_list = request.form['target_string'].split(',')
        for x in target_list:
            if(x is not None and len(x) > 0):
                d = Dictionary.query.filter_by(id = x).first()
                d.isUse = 0
                db.session.add(d)
                db.session.commit()
        return 'success'
    except Exception as e:
        raise e


@dictionaryBlueprint.route('/download/<int:type_id>',methods = ['GET'])
def download(type_id):
    '''创建一个excel文件，是批量导入时指定文件
    内含填写数据的格式，需要按照文件中的字段填写数据
    FIXME: 提示用户需要关闭迅雷插件
    
    Returns:
        [excel文件] -- 模板
    '''
    type_name = DictionaryType.query.filter_by(id = type_id).first().name
    #这个sheet名很重要，必须是类名，否则上传就会报错
    response = excel.make_response_from_array([[u'编号', u'名称', u'字典类型名']], 
        "xls",file_name= u"数据字典批量导入表",sheet_name='Dictionary');
    # print response;
    return response

@dictionaryBlueprint.route('/upload', methods = ['POST'])
@fresh_login_required
def upload():
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
        dtype = DictionaryType.query.filter_by(name = row[u'字典类型名']).first()
        if(dtype is not None):
            d = Dictionary(row[u'编号'], row[u'名称'], dtype.id)
            return (d if Dictionary.query.filter_by(id = d.id).first() is None else None)
        else:
            return None
    try:
        request.save_book_to_database(field_name='file',session=db.session,
            tables=[Dictionary],initializers=[dictionary_init_func]);
        return u'success'
    except Exception as e:
        #FIXME：当sheet名不等于表名时，会报‘No suitable database adapter found!’
        raise e
        return u'fail';


@dictionaryBlueprint.route('/listDictByTypeName', methods = ['GET'])
@fresh_login_required
def list_dictionarys_by_type_name():
    '''根据字典类型名字返回同类型的所有字典数据
    
    '''
    variable = DictionaryType.query.filter_by(isUse = 1, name = request.args['type']).first()
    type_id = (variable.id if variable is not None else None)
    if type_id is not None:
        response = []
        for x in Dictionary.query.with_entities(Dictionary.id, Dictionary.name).filter_by(isUse = 1, type_id = type_id).all():
            response.append({"id":x[0], "name":x[1]})
        return json.dumps(response)
    return '500'


# '''返回一个装有所有Dictionary表数据的excel文件

# 通过flask_excel.make_response_from_tables
# :return : 含有Organization表所有数据的excel文件
# '''
# #验证了db.session没错
# @dictionaryBlueprint.route("/exportAll", methods=['GET'])
# def doexport():
#     return excel.make_response_from_tables(db.session, [dictionary.Dictionary], "xls")