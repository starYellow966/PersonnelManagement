# -*- coding: utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask,Blueprint,render_template,request,redirect,url_for
import flask_excel as excel #excel操作工具包
import json

sys.path.append("..");#修改路径，为了引用models包
from models import organization;

#new a blueprint
organizationBlueprint = Blueprint('organizationBlueprint', __name__, template_folder = '../templates', static_folder = '../static', url_prefix = '/org');

'''组织管理首页(url:'/org')

:return : 首页
:date : 2018/3/13
'''
@organizationBlueprint.route('/')
def index():
    #TODO: 组织管理首页未完成
    return render_template('organizationindex.html');

'''获取所有上级组织的信息

:request.form['level'] : string，当前组织级别，分别为seg,work,team
:return : json,字段有{parent_id,parent_name}
'''
@organizationBlueprint.route('/listAllParent')
def listAllParent():
    # print "enter into listAllParent";
    level = request.args['level'];
    data = organization.Organization.listAllParent(level);
    if(data[0] != u'500'):
        return json.dumps(data),200;
    else:
        return json.dumps([]),500;

# '''字段查重
# :request.args['value']: 字段值
# :request.args['type']: 字段名
# :return : string 查重结果，200-没重复，500-重复
# '''
# @organizationBlueprint.route('/duplicateCheck', methods = ['GET'])
# def duplicateCheck():
#     return "hello",200;

'''组织管理之客运段管理页面(url:'/org/seg')

:return : segmentchart.html
:date : 2018/3/13
'''
@organizationBlueprint.route('/seg')
def segIndex():
    return render_template('segmentchart.html');

'''获取所有客运段信息

:return : json,字段有{id, name, type_id, type_name, parent_id, parent_name};
'''
@organizationBlueprint.route('/seg/listAllSegment', methods = ['POST', 'GET'])
def listAllSegment():
    data = organization.Organization.listAllSegment();#当查询失败时，返回结果是['500']
    # print data;
    if(data[0] != u'500'):
        return json.dumps(data),200;
    else:
        return json.dumps([]),500;


'''插入客运段信息
第一步，封装成Organization对象
第二步，id查重，重复提示信息加上id_error
第三步，name查重，重复提示信息加上name_error
第四步，只有在id,name都不重复才插入
:return : 返回提示信息string,可能出现的值有id_error(id重复),name_error(name重复),error(发生异常),success
:date : 2018/3/14
'''
@organizationBlueprint.route('/seg/insert', methods = ['GET'])
def insertSegment():
    seg = organization.Organization.createSegment(request.args['id'], request.args['name'], request.args['parent_name']);
    response_code = "";
    flag = True;#flag代表是否出现重复，true代表没有重复，false代表有重复
    if( seg == None):
        return 'error',200;
    if(seg.duplicateCheck('id') == False):
        response_code += 'id_error,';
        flag = False;
    if(seg.duplicateCheck('name') == False):
        response_code += 'name_error,';
        flag = False;
    #只有在没有重复才进行插入，避免插入重复值产生的异常
    if(flag):
        if seg.insertOrganization() == '500':
            #说明插入失败
            response_code += 'error';
        else:
            response_code += 'success';
    return response_code,200;

'''插入客运段信息

:return : 返回提示信息，可能出现的值有name_error(name重复),error(发生异常),success
:date : 2018/3/14
'''
@organizationBlueprint.route('/seg/update', methods = ['GET'])
def updateSegment():
    seg = organization.Organization.createSegment(request.args['id'], request.args['name'], request.args['parent_name']);
    if (seg == None):
        return 'error',200;
    response_code = "";
    flag = True;#flag代表是否出现重复，true代表没有重复，false代表有重复
    if(seg.duplicateCheck('name') == False):
        flag = False;
        response_code += 'name_error';
    #只有在没有重复才进行更新，避免更新重复值产生的异常
    if(flag):
        code = seg.updateOrganizationById();
        if code == '200':
            #说明插入失败
            response_code += 'success';
        else:
            response_code += 'error';
    return response_code,200;

'''删除客运段信息

:request : target_string是待删除的段编号组成的string,格式是1,2,3

:return : 返回提示信息
:date : 2018/3/14
'''
@organizationBlueprint.route('/seg/remove', methods = ['POST', 'GET'])
def removeSegment():
    # print request.form['target_string']
    response_code = organization.Organization.removeOrganizations((request.form['target_string']).split(','));
    if response_code == '200':
        return 'success',200;
    else:
        return 'failure,删除失败',500;

@organizationBlueprint.route('/seg/query', methods = ['GET','POST'])
def query():
    query = request.form['query'];
    if (query != ""):
        datas = organization.Organization.queryStatement(query,u'客运段');
        return json.dumps(datas),200;
    return "",200;

'''下载一个excel文件，是批量导入时指定文件

内含填写数据的格式，需要按照文件中的字段填写数据
FIXME: 提示用户需要关闭迅雷插件

:return : excel文件
'''
@organizationBlueprint.route('/seg/download')
def segmentDownload():
    #这个sheet名很重要，必须是类名，否则上传就会报错
    response = excel.make_response_from_array([[u'编号', u'名称', u'所属路局']], 
        "xls",file_name=u"段信息批量导入表",sheet_name='Organization');
    # print response;
    return response;

'''上传excel文件

TODO: 自动跳过重复信息
:return : 成功重定向到'/seg'；反之，错误提示
:date : 2018/3/14
'''
@organizationBlueprint.route('/seg/unload', methods = ['GET','POST'])
def segmentUnload():
    if request.method == 'POST':
        '''将excel中每行数据读取并封装成Segment对象
        
        :return ：Organization对象或者None
        '''
        def segment_init_func(row):
            seg = organization.Organization.createSegment(row[u'编号'], row[u'名称'], row[u'所属路局']);
            #当创建失败seg==None
            print seg;
            return seg;

        try:
            request.save_book_to_database(field_name='file',session=organization.Organization.getSession(),
                tables=[organization.Organization],initializers=[segment_init_func]);
            return "saved",200;
        except Exception as e:
            #FIXME：当sheet名不等于Organization时，会报‘No suitable database adapter found!’
            print e;
            return "文件上传失败，请检查excel文件，其中不能修改sheet名，编号不能重复";
    return "hello";

'''返回一个装有所有Segment表数据的excel文件

通过flask_excel.make_response_from_tables
:return : 含有Organization表所有数据的excel文件
'''
#验证了db.session没错
@organizationBlueprint.route("/seg/exportAll", methods=['GET'])
def doexport():
    return excel.make_response_from_tables(organization.Organization.getSession(), [organization.Organization], "xls")