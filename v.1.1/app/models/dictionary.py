# -*- coding: utf-8 -*-
# 设置默认编码
import sys
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__);
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8';
db = SQLAlchemy(app);

class DictionaryType(db.Model):
    

    __tablename__ = 'DictionaryType';

    id = db.Column(db.Integer(), primary_key = True);

    name = db.Column(db.String(50), unique = True);


    def __init__(self, id, name):
        super(DictionaryType, self).__init__();
        self.id = id;
        self.name = name;

    def __repr__(self):
        return u'<DictionaryType %d %s>' %(self.id, self.name);


    '''返回所有字典类型
    
    发生异常时，打印异常信息，返回None代表服务器内部错误

    :return : list<dict> 或者 None
    :date :2018/3/17
    '''
    @classmethod
    def listAll(cls):
        '''返回所有字典类型
        
        Returns:
            [list<dict>] -- None 或者 所有字典类型
        
        Raises:
            e -- 发生异常时，返回None代表服务器内部错误
        '''
        typelist = [];
        try:
            results = DictionaryType.query.order_by(DictionaryType.id).all();
            for x in results:
                temp = x.__dict__;
                del temp['_sa_instance_state'];
                typelist.append(temp);
        except Exception as e:
            raise e;
            db.session.rollback();
            typelist = [];
        finally:
            return typelist;


    @classmethod
    def getNameById(cls, id):
        name = None;
        try:
            name = DictionaryType.query.filter_by(id = id).first().name;
        except Exception as e:
            raise e;
            name = None;
        finally:
            return name;

class Dictionary(db.Model):

    __tablename__ = 'Dictionary';

    id = db.Column(db.String(30), primary_key = True);

    name = db.Column(db.String(50), nullable = False);

    type_id = db.Column(db.Integer(), nullable = False);

    """docstring for Dictionary"""
    def __init__(self, id, name, type_id):
        super(Dictionary, self).__init__()
        self.id = id;
        self.name = name;
        self.type_id = type_id;

    def __repr__(self):
        return u'<Dictionary {0} {1} {2}>' .format(self.id, self.name, self.type_id);

    '''根据type_id返回同组的所有字典数据
    
    :param['type_id'] : 字典类型编号
    :return : list<dict> 或者 None
    :date :2018/3/17
    '''
    @classmethod
    def listDictByTypeId(cls, type_id):
        dictlist = [];
        try:
            results = Dictionary.query.filter_by(type_id = type_id).order_by(Dictionary.id).all();
            for x in results:
                temp = x.__dict__;
                del temp['_sa_instance_state'];
                dictlist.append(temp);
        except Exception as e:
            raise e;
            db.session.rollback();
            dictlist = None;
        finally:
            return dictlist;

    '''根据type_name返回同组的所有字典数据
    
    :param['type_name'] : 字典类型名称
    :return : list<dict> 或者 None
    :date :2018/3/17
    '''
    @classmethod
    def listDictByTypeName(cls, type_name):
        dictlist = None;
        try:
            type_id = DictionaryType.query.filter_by(name = type_name).first();
            dictlist = Dictionary.listDictByTypeId(type_id);
        except Exception as e:
            raise e;
            db.session.rollback();
            dictlist = None;
        finally:
            return dictlist;
    
    '''删除字典数据
    
    :param['id_string'] : 待删除id串，格式1,2,3
    :return : 响应码 200-成功，500-失败 
    '''
    @classmethod
    def remove(cls, id_string):
        response = 200;
        try:
            for id in id_string.split(','):
                d = Dictionary.query.filter_by(id = id).first();
                db.session.delete(d);
            db.session.commit();
        except Exception as e:
            raise e;
            db.session.rollback();
            response = 500;
        finally:
            return response;

    '''通过组织id来更新=信息，返回响应码

    :return : 响应码int 200-成功，500-失败
    :date :2018/3/18
    '''
    def updateDictionary(self):
        response = 200;
        try:
            Dictionary.query.filter_by(id = self.id).update({'name': self.name});
            db.session.commit();
        except Exception as e:
            print e;
            db.session.rollback();
            response = 500;
        finally:
            return response;

    '''id查重并插入，返回响应码

    :return : 响应码int 200-插入成功，500-插入失败（非id重复） 300-id重复
    :date :2018/3/18
    '''
    def insertDictionary(self):
        response = 200;
        try:
            if(Dictionary.query.filter_by(id = self.id).first() != None):
                response = 300;
            else:
                db.session.add(self);
                db.session.commit();
        except Exception as e:
            raise e;
            db.session.rollback();
            response = 500;
        finally:
            return response;

    @classmethod
    def getSession(cls):
        return db.session;
