# -*- coding: utf-8 -*-
# 设置默认编码
import sys
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8';
db = SQLAlchemy(app)

class TreeNode:
    '''树节点类
    
    Variables:
        id {string} -- 编号
        parent_id {string} -- 父亲节点编号
        text {string} -- 名称
        node {List<TreeNode>} -- 子节点
    '''
    id = ""
    parent_id = ""
    text = ""
    nodes = None

    def __init__(self, id, parent_id, text, nodes = None):
        self.id = id
        self.parent_id = parent_id
        self.text = text
        self.nodes = nodes
    def __repr__(self):
        return u'id:{},text:{}, nodes:{}' .format(self.id, self.text, self.nodes)

    @classmethod
    def convert(cls, lists):
        '''将list<Organization>转换成list<TreeNode>
        
        Arguments:
            lists {list<Organization>} -- list<Organization>
        '''
        result = []
        for item in lists:
            result.append(TreeNode(item.id, item.parent_id, item.name))
        return result

    def findChild(self, child_list):
        '''从child_list中找到自己的子节点，并把子节点从对象转换成字典
        
        Arguments:
            child_list {list<TreeNode>} -- 待连接的子节点集合
        
        Returns:
            [list<dict>] -- 属于自己的子节点集合
        '''
        result = []
        for x in child_list:
            if x.parent_id == self.id :
                result.append(x)
        return result

    def convertToDict(self):
        '''把self.nodes转换成dict
        
        '''
        try:
            result = []
            if self.nodes == None :
                return
            for x in self.nodes:
                # temp = json.dumps(x.__dict__)
                temp = x.__dict__
                del temp['id']
                del temp['parent_id']
                if temp['nodes'] == None:
                    del temp['nodes']
                result.append(temp)
            self.nodes = result
        except Exception as e:
            print e
            raise e

class Organization(db.Model):
    '''组织机构表
    
    负责与数据库服务器建立链接
    
    Extends:
        db.Model
    
    Variables:
        __tablename__ {string} -- 表名
        id {varchar(20)} -- 组织编号
        name {varchar(50)} -- 组织姓名
        status {int} -- 节点状态，0代表虚节点，1代表实节点，比如车间就是虚节点，北京车队就是实节点
        level {int} -- 组织所在的层次
        parent_id {varchar(20)} -- 组织所属上级
        num {int} -- 同层级的排序序号
    '''

    __tablename__ = 'Organization'

    id = db.Column(db.String(20), primary_key = True)

    name = db.Column(db.String(50), unique = True)

    status = db.Column(db.Integer(), nullable = False)

    level = db.Column(db.Integer(), nullable = False)

    parent_id = db.Column(db.String(20), nullable = True)

    num = db.Column(db.Integer(), nullable = True)

    def __init__(self, id, name, status, level, parent_id):
        self.id = id
        self.name = name
        self.status = status
        self.level = level
        self.parent_id = parent_id

    def __repr__(self):
        return u'<Organization {} {} status:{} level:{} parent:{} >' .format(
            self.id, self.name, self.status, self.level, Organization.getNameById(self.parent_id))

    @classmethod
    def getNameById(cls, id):
        '''通过id获得名称
        
        Arguments:
            id {string} -- 待查询的组织编号
        
        Returns:
            [string] -- 组织名称 或者 None(当发生异常或查询为空)
        
        Raises:
            e -- 查询失败
        '''
        name = None
        try:
            name = Organization.query.filter_by(id = id).first().name
        except Exception as e:
            raise e
            name = None
        finally:
            return name

    @classmethod
    def listAll(cls):
        '''获得组织表中所有数据，且封装成list
        根据level降序排列
        
        Returns:
            [list<Organization>] -- 组织表中所有数据
        
        Raises:
            e -- 所有异常
        '''
        result = None
        try:
            result = Organization.query.order_by(Organization.level.desc()).all()
        except Exception as e:
            raise e
            result = None
        finally:
            return result

    @classmethod
    def treeAll(cls):
        '''获得组织表中所有数据，并以tree形结构展示

        思路：从小往上一层层建树
        首先获取最后一层的节点child_list，然后获取倒数第二层的节点cur_list，通过parent_id将child_list连接到cur_list中
        然后让child_list=cur_list，再将上一层的节点放入cur_list，依此类推。
        
        Returns:
            [TreeNode] -- 根节点

        Raises:
            e -- 所有异常
        
        '''
        root = None
        try:
            # import pdb
            # pdb.set_trace()
            max_level = Organization.query.order_by(Organization.level.desc()).first().level
            child_list = TreeNode.convert(Organization.query.filter_by(level = max_level).order_by(Organization.num).all())
            cur_level = max_level - 1
            cur_list = child_list
            # 逐层向上连接成树
            while cur_level >= 0:
                cur_list = TreeNode.convert(Organization.query.filter_by(level = cur_level).order_by(Organization.num).all())
                # print cur_list
                # print child_list
                # print "================="
                #循环遍历当前层级的所有节点
                for cur in cur_list:
                    #表示当前没有待寻亲的节点
                    if len(child_list) == 0 :
                        break;
                    cur.nodes = cur.findChild(child_list)
                    #从待寻亲的节点中删除已经找到父亲的节点
                    for child in cur.nodes:
                        child_list.remove(child)
                    cur.convertToDict()
                    # print cur
                child_list = cur_list
                cur_level -= 1
            root = cur_list[0]
            root = root.__dict__
            del root['id']
            del root['parent_id']
        except Exception as e:
            raise e
            root = None
        finally:
            return root

