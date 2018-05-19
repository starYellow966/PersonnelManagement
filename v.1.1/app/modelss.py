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
    '''

    __tablename__ = 'User'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(),primary_key = True)

    name = db.Column(db.String(64), unique = True)

    pw_hash = db.Column(db.String(100), nullable = False)

    level = db.Column(db.Integer(), default = 1) # 1--普通，0---系统

    def __init__(self, name, password, **kw):
        self.name = name;
        self.set_password(password)
        if 'level' in kw:
            self.level = kw['level']


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




class Employee(db.Model):
    '''员工信息表
       
    Variables:
        __tablename__ {str} -- 表名
        __table_args__ {dict} -- 选项
        id {str} -- 工号
        name {str} -- 姓名
        old_name {str} -- 曾用名
        photo_url {str} -- 照片地址
        sex {boolean} -- 性别，1-男，0-女
        org_id {str} -- 所属部门编号，来源于Organization表
        emp_type {str} -- 用工性质编号，来源于Dictionary表
        status_id {str} -- 人员状态编号，来源于Dictionary表
        position_id {str} -- 职名编号，来源于Dictionary表
        id_num {str} -- 身份证号
        political_status_id {str} -- 政治面貌编号，来源于Dictionary表
        nation_id {str} -- 民族编号，来源于Dictionary表
        degree_id {str} -- 学历编号，来源于Dictionary表
        birthdate {str} -- 出生日期,日期不满10前面要加0，如2018-03-12
        work_date {str} -- 入职时间,日期不满10前面要加0，如2018-03-12
        origin {str} -- 出生地
        phone1 {str} -- 电话1
        phone2 {str} -- 电话2
        address {str} -- 住址
        email {str} -- 邮箱
        techlevel_id {str} -- 技能等级编号，来源于Dictionary表
        others {str} -- 备注
        isUse {boolean} -- 是否在使用，1-是；0-否
    '''

    __tablename__ = 'Employee'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(20), primary_key = True)

    name = db.Column(db.String(30), nullable = False)

    old_name = db.Column(db.String(45), nullable = True)

    photo_url = db.Column(db.String(100), nullable = True)

    sex = db.Column(db.Integer(), nullable = True)

    org_id = db.Column(db.String(20), nullable = True)

    emp_type = db.Column(db.String(30), nullable = True)

    status_id = db.Column(db.String(30), nullable = True)

    position_id = db.Column(db.String(30), nullable = True)

    id_num = db.Column(db.String(20), nullable = True)

    political_status_id = db.Column(db.String(30), nullable = True)

    nation_id = db.Column(db.String(30), nullable = True)

    degree_id = db.Column(db.String(30), nullable = True)

    birthdate = db.Column(db.String(12), nullable = True)

    work_date = db.Column(db.String(12), nullable = True)

    origin = db.Column(db.String(40), nullable = True)

    phone1 = db.Column(db.String(20), nullable = True)

    phone2 = db.Column(db.String(20), nullable = True)

    address = db.Column(db.String(30), nullable = True)

    email = db.Column(db.String(20), nullable = True)

    techlevel_id = db.Column(db.String(30), nullable = True)

    others = db.Column(db.String(40), nullable = True)

    isUse = db.Column(db.Integer(), default = 1)

    is_Practice = db.Column(db.Integer(), default = 1)


    def __init__(self, id, name, **kw):
        super(Employee, self).__init__()
        self.id = (''.join(id) if isinstance(id, list) else id)
        self.name = (''.join(name) if isinstance(name,list) else name)
        self.setOption(kw)

    def setOption(self, kw):
        # print 'enter setOption'
        if 'sex' in kw:
            self.sex = (''.join(kw['sex']) if isinstance(kw['sex'],list) else kw['sex'])
        if 'org_id' in kw:
            self.org_id = (''.join(kw['org_id']) if isinstance(kw['org_id'],list) else kw['org_id'])
        if 'old_name' in kw:
            self.old_name = (''.join(kw['old_name']) if isinstance(kw['old_name'],list) else kw['old_name'])
        if 'photo_url' in kw:
            self.photo_url = (''.join(kw['photo_url']) if isinstance(kw['photo_url'],list) else kw['photo_url'])
        if 'emp_type' in kw:
            self.emp_type = (''.join(kw['emp_type']) if isinstance(kw['emp_type'],list) else kw['emp_type'])
        if 'status_id' in kw:
            self.status_id = (''.join(kw['status_id']) if isinstance(kw['status_id'],list) else kw['status_id'])
        if 'political_status_id' in kw:
            self.political_status_id = (''.join(kw['political_status_id']) if isinstance(kw['political_status_id'],list) else kw['political_status_id'])
        # print 'finish political_status_id'
        if 'position_id' in kw:
            self.position_id = (''.join(kw['position_id']) if isinstance(kw['position_id'],list) else kw['position_id'])
        if 'nation_id' in kw:
            self.nation_id = (''.join(kw['nation_id']) if isinstance(kw['nation_id'],list) else kw['nation_id'])
        if 'degree_id' in kw:
            self.degree_id = (''.join(kw['degree_id']) if isinstance(kw['degree_id'],list) else kw['degree_id'])
        if 'birthdate' in kw:
            self.birthdate = (''.join(kw['birthdate']) if isinstance(kw['birthdate'],list) else kw['birthdate'])
        if 'work_date' in kw:
            self.work_date = (''.join(kw['work_date']) if isinstance(kw['work_date'],list) else kw['work_date'])
        if 'origin' in kw:
            self.origin = (''.join(kw['origin']) if isinstance(kw['origin'],list) else kw['origin'])
        if 'phone1' in kw:
            self.phone1 = (''.join(kw['phone1']) if isinstance(kw['phone1'],list) else kw['phone1'])
        if 'phone2' in kw:
            self.phone2 = (''.join(kw['phone2']) if isinstance(kw['phone2'],list) else kw['phone2'])
        if 'address' in kw:
            self.address = (''.join(kw['address']) if isinstance(kw['address'],list) else kw['address'])
        if 'email' in kw:
            self.email = (''.join(kw['email']) if isinstance(kw['email'],list) else kw['email'])
        if 'techlevel_id' in kw:
            self.techlevel_id = (''.join(kw['techlevel_id']) if isinstance(kw['techlevel_id'],list) else kw['techlevel_id'])
        if 'others' in kw:
            self.others = (''.join(kw['others']) if isinstance(kw['others'],list) else kw['others'])
        if 'is_Practice' in kw:
            self.is_Practice = (''.join(kw['is_Practice']) if isinstance(kw['is_Practice'],list) else kw['is_Practice'])
        if 'id_num' in kw:
            self.id_num = (''.join(kw['id_num']) if isinstance(kw['id_num'],list) else kw['id_num'])
        # print 'finish setOption'

    def to_json(self):
        json_object = {
            "id": self.id,
            "name": self.name,
            "old_name": self.old_name,
            "sex": self.sex,
            "org_id": self.org_id,
            "photo_url": self.photo_url,
            "emp_type": self.emp_type,
            "status_id": self.status_id,
            "position_id": self.position_id,
            "political_status_id": self.political_status_id,
            "nation_id": self.nation_id,
            "degree_id": self.degree_id,
            "birthdate": self.birthdate,
            "work_date": self.work_date,
            "origin": self.origin,
            "phone1": self.phone1,
            "phone2": self.phone2,
            "address": self.address,
            "email": self.email,
            "techlevel_id": self.techlevel_id,
            "others": self.others,
            "isUse": self.isUse,
            "is_Practice": self.is_Practice,
            "id_num": self.id_num
            }
        return json_object

    def __repr__(self):
        return u'<Employee {} {}>' .format(self.id, self.name)

    @classmethod
    def treeAll(cls):
        root = None
        try:
            # import pdb
            # pdb.set_trace()
            max_level = Organization.query.filter_by(isUse = 1).order_by(Organization.level.desc()).first().level
            child_list = TreeNode.convert(Organization.query.filter_by(isUse = 1, level = max_level).order_by(Organization.num).all())
            for x in child_list:
                x.nodes = x.nodes + Employee.appendEmployee(x.id)
                x.convertToDict()
            cur_level = max_level - 1
            cur_list = child_list
            # 从倒数第二层逐层向上连接成树
            while cur_level >= 0:
                cur_list = TreeNode.convert(Organization.query.filter_by(isUse = 1, level = cur_level).order_by(Organization.num).all())
                #循环遍历当前层级的所有节点
                for cur in cur_list:
                    cur.nodes = cur.nodes + Employee.appendEmployee(cur.id)
                    #表示当前还有待寻亲的节点
                    if len(child_list) > 0 :
                        child = cur.findChild(child_list)
                        cur.nodes = cur.nodes + child
                        #从待寻亲的节点中删除已经找到父亲的节点
                        for c in child:
                            child_list.remove(c)
                    cur.convertToDict()
                child_list = cur_list
                cur_level -= 1
            root = cur_list[0]
            root = root.__dict__
            del root['parent_id']
        except Exception as e:
            print e
            root = None
            raise e   
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
            Employee_list = Employee.query.with_entities(Employee.id, Employee.name, Employee.org_id).filter_by(org_id = node_id, isUse = 1).all() #获得属于当前节点的员工信息
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


class Change_Log(db.Model):
    '''变动信息日志
    
    Variables:
        __tablename__ {str} -- [description]
        __table_args__ {dict} -- [description]
        id {[type]} -- [description]
        change_type {[type]} -- 退休R1,死亡R2，调出R3,辞职R4解除R5
        employee_id {[type]} -- [description]
        change_date {[type]} -- [description]
        executor {[type]} -- [description]
    '''

    __tablename__ = 'Change_Log'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    change_type = db.Column(db.String(3), nullable = True)
    employee_id = db.Column(db.String(20), nullable = True)
    change_date = db.Column(db.String(11), nullable = True)
    executor = db.Column(db.String(20), nullable = False)
    others = db.Column(db.String(50), nullable = True)

    type_dictionary = {'R1': u'退休','R2': u'死亡', 'R3': u'调出', 'R4': u'辞职', 'R5': u'解除',
        'I': u'新进', 'F': u'定职', 'IC': u'内部变动'}

    def __init__(self, change_type, employee_id, change_date, executor, others):
        self.change_date = change_date
        self.change_type = change_type
        self.employee_id = employee_id
        self.executor = executor
        self.others = others

    def to_json(self):
        json_object = {
            "id": self.id,
            "change_type": self.change_type,
            "employee_id": self.employee_id,
            "change_date": self.change_date,
            "executor": self.executor,
            "others": self.others
            }
        return json_object

class General_Log(db.Model):
    '''登录注销日志表
    
    Variables:
        __tablename__ {str} -- 表名
        id {int} -- 日志编号，自增
        user_name {string} -- 操作者名字
        ip_address {string} -- 操作的ip地址
        info {string} -- 事件详情
        date_time {int} -- 操作时间戳
    '''

    __tablename__ = 'Log'

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(),primary_key = True)

    user_name = db.Column(db.String(50), nullable = True)

    ip_address = db.Column(db.String(20), nullable = False)

    info = db.Column(db.String(100), nullable = True)

    date_time = db.Column(db.Integer, nullable = True)

    result = db.Column(db.Integer(), default = 1)

    def __init__(self, info, user_name, ip_address):
        self.info = info
        self.user_name = user_name
        self.ip_address = ip_address
        import time
        self.date_time = int(time.time())

    def to_json(self):
        json_object = {
            'id': self.id,
            'user_name': self.user_name,
            'ip_address': self.ip_address,
            'info': self.info,
            'date_time': self.date_time
            }
        return json_object