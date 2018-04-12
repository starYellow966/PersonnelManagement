# -*- coding: utf-8 -*-
# 设置默认编码
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8")
from extensions import db
from organization import TreeNode,Organization

class Employee(db.Model):
    '''简单的员工信息表
    
    仅包含树状结构图所需要的字段
    
    Extends:
        db.Model
    
    Variables:
        __tablename__ {str} -- 表名
        id {str} -- 员工编号
        name {str} -- 员工姓名
        sex {int} -- 性别，0--男生，1--女生
        org_id {str} -- 所属部门编号
    '''

    __tablename__ = 'Employee'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(20), primary_key = True)

    name = db.Column(db.String(30), nullable = False)

    sex = db.Column(db.Integer())

    org_id = db.Column(db.String(20), nullable = False)

    unit = db.Column(db.String(10), default= u'成都客运段')

    photo_url = db.Column(db.String(100))

    def __init__(self, id, name, sex, org_id):
        self.id = id
        self.name = name
        self.sex = sex
        self.org_id = org_id

    def __repr__(self):
        return u'<Employee {} {} {}>' .format(self.id, self.name, self.org_id)

    @classmethod
    def listAll(cls):
        return Employee.query.all()

    @classmethod
    def treeAll(cls):
        root = None
        try:
            # import pdb
            # pdb.set_trace()
            max_level = Organization.query.order_by(Organization.level.desc()).first().level
            child_list = TreeNode.convert(Organization.query.filter_by(level = max_level).order_by(Organization.num).all())
            for x in child_list:
                x.nodes = x.nodes + Employee.appendEmployee(x.id)
                x.convertToDict()
            cur_level = max_level - 1
            cur_list = child_list
            # 从倒数第二层逐层向上连接成树
            while cur_level >= 0:
                cur_list = TreeNode.convert(Organization.query.filter_by(level = cur_level).order_by(Organization.num).all())
                #循环遍历当前层级的所有节点
                for cur in cur_list:
                    cur.nodes = cur.nodes + Employee.appendEmployee(cur.id)
                    #表示当前还有待寻亲的节点
                    if len(child_list) > 0 :
                        cur.nodes = cur.nodes + cur.findChild(child_list)
                        #从待寻亲的节点中删除已经找到父亲的节点
                        for child in cur.nodes:
                            child_list.remove(child)
                    cur.convertToDict()
                child_list = cur_list
                cur_level -= 1
            root = cur_list[0]
            root = root.__dict__
            del root['parent_id']
        except Exception as e:
            print e
            raise e
            root = None
        finally:
            return root

    @classmethod
    def appendEmployee(cls, node_id):
        '''为节点编号为node_id的节点挂上员工
        
        1.通过查询得到属于该待挂载组织节点的员工列表
        2.将list<Employee>转换为list<TreeNode>并返回
        
        Arguments:
            node_id {str} -- 待挂载员工的节点编号
        
        Returns:
            [list<TreeNode>] -- 属于该节点的员工
        
        Raises:
            e -- [description]
        '''
        result = [];
        try:
            Employee_list = Employee.query.with_entities(Employee.id, Employee.name, Employee.org_id).filter_by(org_id = node_id).all() #获得属于当前节点的员工信息
            if Employee_list is not None:
                for x in Employee_list:
                    node = TreeNode(x.id, "", x.name)
                    node.icon = "glyphicon glyphicon-user"
                    result.append(node)
        except Exception as e:
            print e
            raise e
        finally:
            return result


    @classmethod
    def updatePhoto(cls, eid, photo_url):
        '''根据员工id更新图片
        
        Arguments:
            eid {str} -- 员工id
            photo_url {str} -- 图片路径
        
        Returns:
            [int] -- 响应码。200-成功，500-失败
        
        Raises:
            e -- 更新异常
        '''
        response = 200
        try:
            Employee.query.filter_by(id = eid).update({'photo_url': photo_url})
            db.session.commit()
        except Exception as e:
            print e
            raise e
            db.session.rollback()
            response = 500
        finally:
            return response

    @classmethod
    def getEmployeeById(cls, eid):
        result = None
        try:
            result = Employee.query.filter_by(id = eid).first()
        except Exception as e:
            print e
            raise e
            db.session.rollback()
            result = None
        finally:
            return result

    def update_employee(self):
        response_code = 200
        try:
            Employee.query.filter_by(id = self.id).update({
                'name': self.name,
                'sex': self.sex,
                'org_id': self.org_id});
            db.session.commit()
        except Exception as e:
            raise e
            print e
            response_code = 500
            db.session.rollback()
        else:
            return response_code