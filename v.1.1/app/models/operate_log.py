# -*- coding: utf-8 -*-
# 设置默认编码
import sys
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from users import User
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8'
db = SQLAlchemy(app)

class Log(db.Model):
    '''操作日记表
    
    负责连接数据库，查询Log表或向Log表插入数据
    
    Extends:
        db.Model
    
    Variables:
        __tablename__ {str} -- 表名
        id {int} -- 日记编号，自增
        user_id {int} -- 操作者id
        ip_address {string} -- 操作的ip地址
        event_type {string} -- 事件类型，query,insert,delete,update
        info {string} -- 时间详情
        date_time {int} -- 操作时间戳
    '''

    __tablename__ = 'Log'

    id = db.Column(db.Integer(),primary_key = True)

    user_id = db.Column(db.Integer(), nullable = True)

    ip_address = db.Column(db.String(20), nullable = False)

    event_type = db.Column(db.String(20), nullable = False)

    info = db.Column(db.String(100), nullable = True)

    date_time = db.Column(db.Integer, nullable = False)

    def __init__(self, user_id, ip_address, event_type, info, date_time=int(time.time())):
        self.user_id = user_id
        self.ip_address = ip_address
        self.event_type = event_type
        self.info = info
        self.date_time = date_time

    def __repr__(self):
        return u'<Log {} {} {} {} {} {}>' .format(self.id, 
            self.user_id, self.ip_address, self.event_type, self.info, self.date_time)

    @classmethod
    def list_all_logs(cls):
        '''返回Log表中所有数据

        首先，获得Log表中所有数据；
        然后，将user_id转user_name，并对象转dict
        
        Returns:
            [list<dict>] -- None 或者 将Log对象转换成字典，然后存入list
        
        Raises:
            e -- 代指一切异常
        '''
        logs_list = []
        try:
            results = Log.query.order_by(Log.date_time).all()
            for x in results:
                temp = x.__dict__
                del temp['_sa_instance_state']
                if (temp['user_id'] != None) :
                    temp['user_name'] = User.query.filter_by(id = temp['user_id']).first().name
                logs_list.append(temp)
        except Exception as e:
            raise e
            db.session.rollback()
            logs_list = None
        finally:
            return logs_list

    def insert_log(self):
        '''插入一条日记信息到数据库
        
        Returns:
            [int] -- 响应码，200-成功；500-失败
        
        Raises:
            e -- 数据库插入异常，回滚事务
        '''
        response = 200
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise e
            db.session.rollback()
            response = 500
        finally:
            return response