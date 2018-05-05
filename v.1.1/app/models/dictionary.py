# -*- coding: utf-8 -*-
# 设置默认编码
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8");
# import sys
# print sys.getdefaultencoding()

from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from operate_log import Log
from flask_login import current_user
from extensions import db
from response_object import ResponseObject

class DictionaryType(db.Model):
    

    __tablename__ = 'DictionaryType'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(), primary_key = True)

    name = db.Column(db.String(50), unique = True)

    isUse = db.Column(db.Integer(), default = 1)


    def __init__(self, id, name):
        super(DictionaryType, self).__init__()
        self.id = id;
        self.name = name

    def __repr__(self):
        return u'<DictionaryType %d %s>' %(self.id, self.name)


    '''返回所有字典类型
    
    发生异常时，打印异常信息，返回None代表服务器内部错误

    :return : list<dict> 或者 None
    :date :2018/3/17
    '''
    @classmethod
    def listAll(cls):
        '''返回所有字典类型
        
        Returns:
            [dict] -- 提示信息，有2个字段
                      message {str} -- 操作结果，200-成功；500-失败
                      data    {str} -- 详细的数据,默认[]
        
        Raises:
            e -- 发生异常时，返回None代表服务器内部错误
        '''
        response = ResponseObject(data = [])
        try:
            results = DictionaryType.query.filter_by(isUse = 1).order_by(DictionaryType.id).all();
            # print results
            for x in results:
                temp = x.__dict__;
                del temp['_sa_instance_state'];
                response.data.append(temp);
        except Exception as e:
            db.session.rollback()
            response.set_fail()
            raise e
        finally:
            return response


    @classmethod
    def get_name_by_id(cls, id):
        response = ResponseObject()
        try:
            response.data = DictionaryType.query.filter_by(id = id).first().name;
        except Exception as e:
            response.set_fail()
            raise e
        finally:
            return response

class Dictionary(db.Model):

    __tablename__ = 'Dictionary'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(30), primary_key = True)

    name = db.Column(db.String(50), nullable = False)

    type_id = db.Column(db.Integer(), nullable = False)

    isUse = db.Column(db.Integer(), default = 1)

    """docstring for Dictionary"""
    def __init__(self, id, name, type_id):
        super(Dictionary, self).__init__()
        self.id = id
        self.name = name
        self.type_id = type_id

    def __repr__(self):
        return u'<字典数据 id:{0} name:{1} >' .format(self.id, self.name)

    @classmethod
    def listDictByTypeId(cls, type_id):
        '''根据type_id返回同类型的所有字典数据

        Arguments:
            id_string {string} -- 待删除id串，格式1,2,3
        
        Returns:
            [dict] -- 提示信息，有2个字段
                      message {str} -- 操作结果，200-成功；500-失败
                      data    {str} -- 详细的数据
        
        Raises:
            e -- 数据库操作异常
        '''
        response = ResponseObject(data = [])
        # dictlist = []
        try:
            results = Dictionary.query.filter_by(isUse = 1, type_id = type_id).order_by(Dictionary.id).all();
            # print results
            for x in results:
                temp = {}
                temp.update(x.__dict__)
                del temp['_sa_instance_state']
                response.data.append(temp)
        except Exception as e:
            print e
            db.session.rollback()
            response.set_fail()
            # raise e
        finally:
            # print response.data
            return response

    @classmethod
    def listDictByTypeName(cls, type_name):
        '''根据type_name返回同组的所有字典数据
        
        Arguments:
            id_string {string} -- 待删除id串，格式1,2,3
        
        Returns:
            [dict] -- 提示信息，有2个字段
                      message {str} -- 操作结果，200-成功；500-失败
                      data    {str} -- 详细的数据,默认[]
        
        Raises:
            e -- 数据库操作异常
        '''
        response = ResponseObject(data = [])
        try:
            type_id = DictionaryType.query.filter_by(isUse = 1, name = type_name).first().id
            if type_id is not None:
                response = Dictionary.listDictByTypeId(type_id)
        except Exception as e:
            db.session.rollback()
            response.set_fail()
            print e
            raise e
        finally:
            return response
    
    
    @classmethod
    def remove(cls, id_string):
        '''删除字典数据
        
        可删除一个或者多个字典数据
        
        Arguments:
            id_string {string} -- 待删除id串，格式1,2,3
        
        Returns:
            [dict] -- 提示信息，有2个字段
                      message {str} -- 操作结果，200-成功；500-失败
                      data    {str} -- 详细的提示信息，默认是success
        
        Raises:
            e -- 数据库操作异常
        '''
        response = ResponseObject()
        try:
            for id in id_string.split(','):
                # d = Dictionary.query.filter_by(id = id).update({'isUse': 0})
                db.session.delete(Dictionary.query.filter_by(id = id).first())
            db.session.commit()
        except Exception as e:
            response.set_fail()
            print e
            raise e
        finally:
            Log.createLog('Delete', u'删除字典数据id{' + id_string + u"}").insertLog(1 if response.message == 200 else 0)
            return response

    def update(self):
        '''通过组织id来更新name，返回提示信息
        
        Returns:
            [dict] -- 提示信息，有2个字段
                      message {str} -- 操作结果，200-成功；500-失败
                      data    {str} -- 详细的提示信息，默认是success
        
        Raises:
            e -- 数据库操作异常
        '''
        response = ResponseObject()
        try:
            Dictionary.query.filter_by(id = self.id).update({'name': self.name})
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            response.set_fail()
            raise e
        finally:
            Log.createLog('Delete', u'修改后的字典数据为{ id:' + self.id + ',name:' + self.name + '}').insertLog(1 if response.message == 200 else 0)
            return response


    def insert(self):
        '''id查重并插入，返回响应码
        
        Returns:
            [dict] -- 提示信息，有2个字段
                      message {str} -- 操作结果，200-成功；500-失败
                      data    {str} -- 详细的提示信息，默认是success
        
        Raises:
            e -- 数据库操作异常
        '''
        response = ResponseObject()
        try:
            if(Dictionary.query.filter_by(id = self.id).first() != None):
                response.set_fail('id_error')
            else:
                db.session.add(self)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            response.set_fail()
            raise e
        finally:
            Log.createLog('Delete', u'插入数据{id:' + self.id + ',name:' + self.name + ',type:' + DictionaryType.get_name_by_id(self.type_id).data + '}'
                ).insertLog(1 if response.message == 200 else 0)
            return response

    @classmethod
    def getDictionaryById(cls, id):
        '''根据id获得字典对象
        
        Returns:
            [dict] -- 提示信息，有2个字段
                      message {str} -- 操作结果，200-成功；500-失败
                      data    {str} -- 详细的提示信息，默认是success
        
        Raises:
            e -- 数据库操作异常
        '''
        response = ResponseObject(data = [])
        try:
            response.data = Dictionary.query.filter_by(id = id).first()
        except Exception as e:
            response.set_fail(None)
            db.session.rollback()
            raise e
        finally:
            return response.data

    @classmethod
    def getNameById(cls, id):
        '''根据id获得字典对象名字
        
        Returns:
            [dict] -- 提示信息，有2个字段
                      message {str} -- 操作结果，200-成功；500-失败
                      data    {str} -- 详细的提示信息，默认是success
        
        Raises:
            e -- 数据库操作异常
        '''
        response = ResponseObject()
        try:
            response.data = Dictionary.query.filter_by(id = id).first().name
        except Exception as e:
            response.set_fail(None)
            db.session.rollback()
            raise e
        finally:
            return response
