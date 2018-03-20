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

class OrganizationType(db.Model):
    __tablename__ = 'OrganizationType';

    id = db.Column(db.String(30), primary_key = True);
    name = db.Column(db.String(50), unique = True );

    def __init__(self, id, name):
        #会自动声明一个对象的session
        self.id = id;
        self.name = name;

    def __repr__(self):
        return u'<OrganizationType %s %s>' %(self.id, self.name);

    '''返回所有组织类型
    
    发生异常时，打印异常信息，返回['500']代表服务器内部错误

    :return : list<dict>
    :date :2018/3/12
    '''
    @classmethod
    def listAllTypes(cls):
        #查询
        try:
            results = OrganizationType.query.all();
            #将对象转换成字典
            typeLists = [];
            for item in results:
                temp = item.__dict__;
                del temp['_sa_instance_state'];
                typeLists.append(temp);
        except Exception as e:
            print e;
            db.session.rollback();
            return ['500'];
        finally:
            # db.session.close();
            return typeLists;

    '''返回id对应的名字
    
    发生异常时，打印异常信息，返回'error:500'代表服务器内部错误

    :param : 带查询的id
    :return : 名称string
    :date :2018/3/12
    '''
    @classmethod
    def getNameById(cls,target):
        try:
            result = OrganizationType.query.filter_by(id = target).first().name;
        except Exception as e:
            print e;
            db.session.rollback();
            result = 'error:500';
        finally:
            # db.session.close();
            return result;

    '''返回名称对应的id
    
    发生异常时，打印异常信息，返回'error:500'代表服务器内部错误

    :param : 带查询的name
    :return : string id
    :date :2018/3/12
    '''
    @classmethod
    def getIdByName(cls, target_name):
        try:
            result = OrganizationType.query.filter_by(name = target_name).first().id;
        except Exception as e:
            print e;
            db.session.rollback();
            result = 'error:500';
        finally:
            # db.session.close();
            return result;

    '''新增组织类型
    
    :return : 响应码，200-成功，500-失败
    :date :2018/3/13
    '''
    def insertOrganizationType(self):
        print 'enter into function Organization.insertOrganizationType';
        response = '200';
        try:
            db.session.add(self);
            db.session.commit();
        except Exception as e:
            print e;
            db.session.rollback();
            response = '500';
        finally:
            # db.session.close();
            return response;

#FIXME：db.session.close()的使用还待商榷，当close后，当前的Organization对象就不能再使用session了
class Organization(db.Model):
    __tablename__ = 'Organization';

    id = db.Column(db.String(30), primary_key = True);

    name = db.Column(db.String(50), unique = True);

    type_id = db.Column(db.String(30), nullable = False);

    parent_id = db.Column(db.String(30), nullable = False);

    def __init__(self, id, name, type_id, parent_id):
        self.id = id;
        self.name = name;
        self.type_id = type_id;
        self.parent_id = parent_id;

    def __repr__(self):
        return u'<Organization %s %s %s %s>' %(self.id,self.name,self.type_id,self.parent_id);

    '''插入一个组织到数据库中，返回响应码
    
    :return : 响应码string 200-成功，500-失败
    :date :2018/3/12
    '''
    def insertOrganization(self):
        response = '200';
        try:
            db.session.add(self);
            db.session.commit();
        except Exception as e:
            print e;
            db.session.rollback();
            response = '500';
        finally:
            # db.session.close();
            return response;

    '''从数据库删除组织，可以是多个也可以是一个，返回响应码
    
    :param 'targets' : 一个待删除的组织id的list
    :return : 响应码string 200-成功，500-失败
    :date :2018/3/12
    '''
    @classmethod
    def removeOrganizations(cls,targets):
        response = '200';
        try:
            #循环lsit，一个一个删除
            for item in targets:
                o = Organization.query.filter_by(id = item).first();
                db.session.delete(o);
            db.session.commit();
        except Exception as e:
            print e;
            db.session.rollback();
            response = '500';
        finally:
            # db.session.close();
            return response;

    '''通过组织id来更新组织信息，返回响应码

    :return : 响应码string 200-成功，500-失败
    :date :2018/3/12
    '''
    def updateOrganizationById(self):
        response = '200';
        try:
            Organization.query.filter_by(id = self.id).update({'name': self.name, 
                'type_id': self.type_id, 'parent_id': self.parent_id});
            db.session.commit();
        except Exception as e:
            print e;
            db.session.rollback();
            response = '500';
        finally:
            # db.session.close();
            return response;

    '''(私有方法)根据id查找对应的组织名称

    :param : 待查询组织编号
    :return : string 组织名称;
    :exception : 
    :date :2018/3/13
    '''
    @classmethod
    def getNameById(cls,target_id):
        try:
            name = Organization.query.filter_by(id = target_id).first().name;
        except Exception as e:
            db.session.rollback();
            raise e
        finally:
            # db.session.close();
            return name;

    '''(私有方法)根据组织名称查找对应的id

    :param : 待查询组织名称
    :return : string 组织id;
    :exception : 
    :date :2018/3/14
    '''
    @classmethod
    def getIdByName(cls, target_name):
        try:
            target_id = Organization.query.filter_by(name = target_name).first().id;
        except Exception as e:
            db.session.rollback();
            raise e
        finally:
            # db.session.close();
            return target_id;

    '''(私有方法)根据组织类型编号获得同一组织类型的所有组织信息    

    :param : 待查询类型编号
    :return : list<dict> 同一类型的所有组织信息；发生异常时，向上提交异常信息
    :exception : 
    :date : 2018/3/12
    '''
    @classmethod
    def listOrganizationByTypeId(cls, type_id):
        try:
            results = Organization.query.filter_by(type_id = type_id).all();
            #对象转dict
            lists = [];
            for item in results:
                temp = item.__dict__;
                del temp['_sa_instance_state'];
                lists.append(temp);
        except Exception as e:
            db.session.rollback();
            # lists = ['500'];
            raise e;
        finally:
            # db.session.close();
            return lists;

    '''返回所有客运段显示信息

    第一步，调用listOrganizationByType(u'0001')获得表中属于‘客运段’类型所有信息
    第二步，将type_id转为type_name,将parent_id转为parent_name
    第三步，返回list<dict>

    :return : list<dict> 所有客运段信息, 发生异常时，打印异常信息，返回['500']代表服务器内部错误
    :date :2018/3/13
    '''
    @classmethod
    def listAllSegment(cls):
        try:
            results = Organization.listOrganizationByTypeId(u'0001');
            for x in results:
                x['type_name'] = OrganizationType.getNameById(x['type_id']);
                x['parent_name'] = Organization.getNameById(x['parent_id']);
        except Exception as e:
            print e;
            db.session.rollback();
            return ['500'];
        finally:
            return results;

    '''获取所有上级组织的信息

    :param : string，当前组织级别，分别为seg,work,team
    :return : list<dict>,字段有{parent_id,parent_name} ; 异常返回['500']
    '''
    @classmethod
    def listAllParent(cls, level):
        try:
            if (level == 'seg'):
                type_id = OrganizationType.getIdByName(u'路局');
            elif (level == 'work'):
                type_id = OrganizationType.getIdByName(u'客运段');
            elif (level == 'team'):
                type_id = OrganizationType.getIdByName(u'车间');
            else:
                type_id = None;
            if( type(type_id) != type(None)):
                results = Organization.query.filter_by(type_id = type_id).all();
                lists = [];
                for x in results:
                    lists.append({'parent_id': x.id, 'parent_name': x.name});
        except Exception as e:
            print e;
            db.session.rollback();
            lists = ['500'];
        finally:
            return lists;


    '''产生一个客运段对象
    
    :param : 组织id
    :param : 组织名称
    :param : 组织所属路局名称
    :return : 返回一个Organization对象或者发生异常时返回None
    '''
    @classmethod
    def createSegment(cls, sid, name, parent_name):
        try:
            type_id = OrganizationType.getIdByName(u'客运段');
            parent_id = Organization.getIdByName(parent_name);
            seg = Organization(sid, name, type_id, parent_id);
            return seg;
        except Exception as e:
            print e;
            return None;

    '''字段查重

    :param[field]: 字段名
    :return : True-没重复，False-重复,出现异常返回False
    '''
    def duplicateCheck(self, field):
        try:
            if(field == 'id'):
                result = Organization.query.filter_by(id = self.id).first();
            elif (field == 'name'):
                result = Organization.query.filter_by(name = self.name).first();
            if (result == None) :
                return True;
            else:
                return False;
        except Exception as e:
            print e;
            return False;

    #db.session有问题
    @classmethod
    def getSession(cls):
        return db.session;
