# -*- coding: utf-8 -*-
# 设置默认编码
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8");

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import json
from extensions import db
# from db_helper import db

class TreeNode:
    '''树节点类
    
    Variables:
        id {string} -- 编号
        parent_id {string} -- 父亲节点编号
        text {string} -- 名称
        node {List<TreeNode>} -- 子节点
        icon {str} -- 图标
    '''
    id = ""
    parent_id = ""
    text = ""
    nodes = []
    icon = ""

    def __init__(self, id, parent_id, text, nodes = []):
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

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(20), primary_key = True)

    name = db.Column(db.String(50), unique = True)

    status = db.Column(db.Integer(), nullable = False)

    level = db.Column(db.Integer(), nullable = False)

    parent_id = db.Column(db.String(20), nullable = True)

    num = db.Column(db.Integer(), nullable = True)

    def __init__(self, id, name, status, parent_id, num):
        self.id = id
        self.name = name
        self.status = status
        self.parent_id = parent_id
        # self.level = 0
        self.setLevel()
        self.num = num

    def __repr__(self):
        return u'<Organization {} {} status:{} level:{} parent:{} >' .format(
            self.id, self.name, self.status, self.level, Organization.getNameById(self.parent_id))

    @classmethod
    def getNameById(cls, id):
        '''通过待查询的组织编号获得待查询的组织名称
        
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
            db.session.rollback()
            name = None
            raise e
        finally:
            return name

    def setLevel(self):
        self.level = Organization.query.filter_by(id = self.parent_id).first().level + 1

    @classmethod
    def listAll(cls, level_direction=False):
        '''获得组织表中所有数据，且封装成list
        根据level_direction的值决定结果按level值升序或降序排列
        
        Keyword Arguments:
            level_direction {bool} -- false代表结果按level升序排列 (default: {False})

        Returns:
            [list<Organization>] -- 组织表中所有数据
        
        Raises:
            e -- 所有异常
        
        
        '''
        result = None
        try:
            if level_direction :
                #先按level降序再按num升序
                result = Organization.query.order_by(Organization.level.desc(), Organization.num).all()
            else:
                #先按level升序再按num升序
                result = Organization.query.order_by(Organization.level, Organization.num).all()
        except Exception as e:
            db.session.rollback()
            result = None
            raise e
        finally:
            return result

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
            max_level = Organization.query.order_by(Organization.level.desc()).first().level
            child_list = TreeNode.convert(Organization.query.filter_by(level = max_level).order_by(Organization.num).all())
            cur_level = max_level - 1
            cur_list = child_list
            # 逐层向上连接成树
            while cur_level >= 0:
                '''
                1.获得child_list上一层的所有组织机构信息，存放在cur_list
                2.循环cur_list，为这层的每一个组织机构从child_list中选出属于自己的孩子，并连接在自己的nodes中,链接后将孩子从TreeNode转换成dict
                3.循环结束后，将cur_list赋值给child_list
                '''
                cur_list = TreeNode.convert(Organization.query.filter_by(level = cur_level).order_by(Organization.num).all())
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
            print e
            db.session.rollback()
            root = None
            raise e
        finally:
            # print root
            return root

    def listChilds(self):
        '''返回子节点
        
        根据当前节点的name，利用广度遍历全局变量获得其所有的子节点
        '''
        # child_list = None
        # try:
        #     all_nodes = Organization.listAll(False) #按广度遍历排序好的结果
        #     cur_organization = Organization.query.filter_by(name = self.name).first()
        #     if len(all_nodes) > 0 :
        #         index = all_nodes.index(cur_organization) #不存在时抛ValueError
        #         nodes_list = all_nodes[index + 1 :] #只有排在当前节点后面的节点才可能是其子节点
        #         if len(nodes_list) > 0 :
                    
                
        # except Exception as e:
        #     raise e
        # finally:
        #     return child_list
        #     
    @classmethod
    def list_all_name(cls):
        '''只返回所有组织的编号和名字
        
        Raises:
            e -- [description]
        '''
        result = None
        try:
            result = Organization.query.with_entities(Organization.id, Organization.name).filter_by(status = 1).order_by(Organization.level, Organization.num).all()
        except Exception as e:
            print e
            db.session.rollback()
            result = None
            raise e
        finally:
            return result

    def insert(self):
        response = '200'
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            response = '500'
            raise e
        finally:
            return response

    def update(self):
        response = '200'
        try:
            Organization.query.filter_by(id = self.id).update({'name': self.name,
                'status': self.status, 'parent_id': self.parent_id, 'num': self.num, 'level':self.level})
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            response = '500'
            raise e
        finally:
            return response

    @classmethod
    def remove(cls, id_list):
        response = '200'
        try:
            for x in id_list:
                o = Organization.query.filter_by(id = x).first()
                db.session.delete(o)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            response = '500'
            raise e
        finally:
            return response

    @classmethod
    def queryById(cls, oid):
        result = None
        try:
            result = Organization.query.filter_by(id = oid).first()
        except Exception as e:
            print e
            result = None
            db.session.rollback()
            raise e
        finally:
            return result