# -*- coding: utf-8 -*-
# 设置默认编码
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8");

from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from users import User
import time
from flask_login import current_user
from extensions import db
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8'
# db = SQLAlchemy(app)

class Log(db.Model):
    '''操作日志表
    
    负责连接数据库，查询Log表或向Log表插入数据
    TODO(HX): 可能还需要添加事件执行是否成功的字段，暂且放在info字段中
    
    Extends:
        db.Model
    
    Variables:
        __tablename__ {str} -- 表名
        id {int} -- 日志编号，自增
        user_name {string} -- 操作者名字
        ip_address {string} -- 操作的ip地址
        event_type {string} -- 事件类型，query,insert,delete,update
        info {string} -- 事件详情
        date_time {int} -- 操作时间戳
        result {int} -- 操作结果 1---成功；2---失败
    '''

    __tablename__ = 'Log'

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(),primary_key = True)

    user_name = db.Column(db.String(50), nullable = False)

    ip_address = db.Column(db.String(20), nullable = False)

    event_type = db.Column(db.String(20), nullable = False)

    info = db.Column(db.String(100), nullable = True)

    date_time = db.Column(db.Integer, nullable = True)

    result = db.Column(db.Integer(), default = 1)

    def __init__(self, event_type, info, user_name, ip_address):
        self.event_type = event_type
        self.info = info
        self.user_name = user_name
        self.ip_address = ip_address
        self.date_time = int(time.time())
    
    # def __init__(self, func):
    #     self._func = func

    def __repr__(self):
        return u'<Log {} {} {} {} {} {}>' .format(self.id, 
            self.user_name, self.ip_address, self.event_type, self.info, self.date_time)
        
    # def __call__(self, *args, **kw):
    #     if 'event_type' in kw:
    #         self.event_type = ''.join(kw['event_type'])
    #     if 'info' in kw:
    #         self.info = ''.join(kw['info'])
    #     self.user_name = current_user.name
    #     self.ip_address = request.remote_addr
    #     self.date_time = int(time.time())
    #     try:
    #         self._func(args, kw)
    #     except Exception as e:
    #         print e
    #         self.result = 0
    #     finally:
    #         self.insertLog()


    # def setResult(self, flag):
    #     '''设置操作状态

    #     在info字段中最前面加入一个标志，代表当前操作是否成功
        
    #     Arguments:
    #         flag {boolean} -- 当前操作是否成功，true--成功，false--失败
    #     '''
    #     if(flag):
    #         self.result = 1
    #     else:
    #         self.result = 0

    @classmethod
    def listLogsByUserName(cls, user_name):
        '''返回用户编号为uer_id的所有操作日志

        首先，通过uer_id获得Log表中的数据；
        然后，将user_name转user_name，并对象转dict

        Arguments:
            user_name {int} -- 当前用户id
        
        Returns:
            [list<dict>] -- None 或者 将Log对象转换成字典，然后存入list
        
        Raises:
            e -- 代指一切异常
        '''
        logs_list = []
        try:
            results = Log.query.filter_by(user_name = user_name).order_by(Log.date_time.desc()).all()
            for x in results:
                temp = {}
                temp.update(x.__dict__)
                del temp['_sa_instance_state']
                logs_list.append(temp)
        except Exception as e:
            db.session.rollback()
            logs_list = None
            raise e
        finally:
            return logs_list

    @classmethod
    def createLog(cls, event_type, info):
        return Log(event_type, info, current_user.name, request.remote_addr)

    def insertLog(self, result):
        '''插入一条日志信息到数据库
        TODO(HX):如果当前的日志信息与当前用户最近一条日志信息相同且相隔1s内，则不插入
        
        Returns:
            [int] -- 响应码，200-成功；500-失败
        
        Raises:
            e -- 数据库插入异常，回滚事务
        '''
        self.result = result
        response = {'message': 200, 'data': None}
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            response['message'] = 500
            raise e
        finally:
            return response['message']

    # @classmethod
    # def createLog(cls, event_type, info, status = True):
    #     '''创建一个log对象，相当于重载构造函数
        
    #     创建log对象
        
    #     Arguments:
    #         id {int} -- 日志编号，自增
    #         user_name {string} -- 操作者名字
    #         ip_address {string} -- 操作的ip地址
    #         event_type {string} -- 事件类型，query,insert,delete,update
    #         info {string} -- 事件详情
        
    #     Keyword Arguments:
    #         user_name {string} -- 当前用户名 (default: {current_user.name})
    #         ip_address {string} -- 当前用户所在ip (default: {request.remote_addr})
    #         status {bool} -- 操作是否成功 (default: {True})
    #     '''
    #     log = Log(current_user.name, request.remote_addr, event_type, info)
    #     log.setResult(status)
    #     return lo
