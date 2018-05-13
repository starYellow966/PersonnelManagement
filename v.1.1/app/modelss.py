# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class User(UserMixin,db.Model):
    '''系统登录用户
    
    Extends:
        UserMixin
        db.Model
    '''

    __tablename__ = 'User'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(),primary_key = True)

    name = db.Column(db.String(64), unique = True)

    pw_hash = db.Column(db.String(100), nullable = False)

    def __init__(self, name, password):
        self.name = name;
        self.set_password(password)


    def __repr__(self):
        return '<User {0}>' .format(self.name)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password) 


class DictionaryType(db.Model):
    '''数据字典类型
    
    Extends:
        db.Model
    '''

    __tablename__ = 'DictionaryType'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(), primary_key = True)

    name = db.Column(db.String(50), unique = True)

    isUse = db.Column(db.Integer(), default = 1)


    def __init__(self, id, name, **kw):
        self.id = id
        self.name = name

    def __repr__(self):
        return u'<DictionaryType %d %s>' %(self.id, self.name)

    def to_json(self):
        json_object = {
            'id': self.id,
            'name': self.name,
            'isUse': self.isUse
            }
        return json_object


class Dictionary(db.Model):

    __tablename__ = 'Dictionary'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(30), primary_key = True)

    name = db.Column(db.String(50), nullable = False)

    type_id = db.Column(db.Integer(), nullable = False)

    isUse = db.Column(db.Integer(), default = 1)

    """docstring for Dictionary"""
    def __init__(self, id, name, type_id):
        self.id = (''.join(id) if isinstance(id, list) else id)
        self.name = (''.join(name) if isinstance(name,list) else name)
        self.type_id = (''.join(type_id) if isinstance(type_id,list) else type_id)

    def __repr__(self):
        return u'<字典数据 id:{0} name:{1} >' .format(self.id, self.name)

    def to_json(self):
        json_object = {
            'id': self.id,
            'name': self.name,
            'type_id': self.type_id,
            'isUse': self.isUse
            }
        return json_object
    


class Organization(db.Model):
    '''组织机构表
    
    负责与数据库服务器建立链接
    
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

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(20), primary_key = True)

    name = db.Column(db.String(50), unique = True)

    status = db.Column(db.Integer(), nullable = False)

    level = db.Column(db.Integer(), nullable = False)

    parent_id = db.Column(db.String(20), nullable = True)

    num = db.Column(db.Integer(), nullable = True)

    isUse = db.Column(db.Integer(), default = 1)

    def __init__(self, id, name, status, parent_id, num):
        self.id = (''.join(id) if isinstance(id, list) else id)
        self.name = (''.join(name) if isinstance(name, list) else name)
        self.status = (''.join(status) if isinstance(status, list) else status)
        self.parent_id = (''.join(parent_id) if isinstance(parent_id, list) else parent_id)
        self.level = Organization.query.filter_by(id = self.parent_id).first().level + 1
        self.num = (''.join(num) if isinstance(num, list) else num)

    def __repr__(self):
        return u'<Organization {} {} status:{} level:{} parent:{} >' .format(
            self.id, self.name, self.status, self.level, Organization.getNameById(self.parent_id))

    def to_json(self):
        json_object = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "level": self.level,
            "parent_id": self.parent_id,
            "num": self.num
            }
        return json_object



    @classmethod
    def treeAll(cls):
        '''获得组织表中所有数据，并以tree形结构展示

        思路：从下往上一层层建树
        首先获取最后一层的节点child_list，然后获取倒数第二层的节点cur_list，通过parent_id将child_list连接到cur_list中
        然后让child_list=cur_list，再将上一层的节点放入cur_list，依此类推。
        注意：每次成功为一个节点链接上孩子后，还需要将孩子从TreeNode转换成dict
        
        Returns:
            [TreeNode] -- 根节点

        Raises:
            e -- 所有异常
        
        '''
        root = None
        try:
            # import pdb
            # pdb.set_trace()
            max_level = Organization.query.filter_by(isUse = 1).order_by(Organization.level.desc()).first().level
            child_list = TreeNode.convert(Organization.query.filter_by(isUse = 1,level = max_level).order_by(Organization.num).all())
            cur_level = max_level - 1
            cur_list = child_list
            # 逐层向上连接成树
            while cur_level >= 0:
                '''
                1.获得child_list上一层的所有组织机构信息，存放在cur_list
                2.循环cur_list，为这层的每一个组织机构从child_list中选出属于自己的孩子，并连接在自己的nodes中,链接后将孩子从TreeNode转换成dict
                3.循环结束后，将cur_list赋值给child_list
                '''
                cur_list = TreeNode.convert(Organization.query.filter_by(isUse = 1,level = cur_level).order_by(Organization.num).all())
                #循环遍历当前层级的所有节点
                for cur in cur_list:
                    #表示当前还有待寻亲的节点
                    if len(child_list) > 0 :
                        cur.nodes = cur.nodes + cur.findChild(child_list)
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
            # print e
            db.session.rollback()
            root = None
            raise e
        finally:
            # print root
            return root


# 待修改
class TreeNode:
    '''树节点类
    
    Variables:
        id {string} -- 编号
        parent_id {string} -- 父亲节点编号
        text {string} -- 名称
        node {List<TreeNode>} -- 子节点
        icon {str} -- 图标
    '''

    def __init__(self, id = "", parent_id = "", text = "", nodes = []):
        self.id = id
        self.parent_id = parent_id
        self.text = text
        self.nodes = nodes
        self.icon = "glyphicon glyphicon-bed"
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
            if len(self.nodes) == 0 :
                return
            for x in self.nodes:
                # temp = json.dumps(x.__dict__)
                temp = x.__dict__
                del temp['parent_id']
                if len(temp['nodes']) == 0:
                    del temp['nodes']
                result.append(temp)
            self.nodes = result
        except Exception as e:
            print e
            raise e