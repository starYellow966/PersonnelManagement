# -*- coding: utf-8 -*-
# 设置默认编码
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8")
from extensions import db
# from db_helper import db
from organization import TreeNode,Organization
from dictionary import Dictionary     

class Employee(db.Model):
    '''员工信息表
    
    
    Extends:
        db.Model
    
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
        birthdate {str} -- 出生日期，时间戳
        work_date {str} -- 入职时间，时间戳
        origin {str} -- 出生地
        phone1 {str} -- 电话1
        phone2 {str} -- 电话2
        address {str} -- 住址
        email {str} -- 邮箱
        techlevel_id {str} -- 技能等级编号，来源于Dictionary表
        others {str} -- 备注
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

    birthdate = db.Column(db.Integer(), nullable = True)

    work_date = db.Column(db.Integer(), nullable = True)

    origin = db.Column(db.String(40), nullable = True)

    phone1 = db.Column(db.String(20), nullable = True)

    phone2 = db.Column(db.String(20), nullable = True)

    address = db.Column(db.String(30), nullable = True)

    email = db.Column(db.String(20), nullable = True)

    techlevel_id = db.Column(db.String(30), nullable = True)

    others = db.Column(db.String(40), nullable = True)

    def __init__(self, id, name, sex, org_id, **kw):
        self.id = id
        self.name = name
        self.sex = sex
        self.org_id = org_id
        self.setOption(kw)

    def setOption(self, kw):
        if 'old_name' in kw:
            self.old_name = kw['old_name']
        if 'photo_url' in kw:
            self.photo_url = kw['photo_url']
        if 'emp_type' in kw:
            self.emp_type = kw['emp_type']
        if 'status_id' in kw:
            self.status_id = kw['status_id']
        if 'position_id' in kw:
            self.position_id = kw['position_id']
        if 'nation_id' in kw:
            self.nation_id = kw['nation_id']
        if 'degree_id' in kw:
            self.degree_id = kw['degree_id']
        import time
        if 'birthdate' in kw:
            # kw['birthdate']不是时间戳 FIXME(HX):有问题
            self.birthdate = time.strftime(kw['birthdate'], '%Y-%m-%d').time()
            print self.birthdate
        if 'work_date' in kw:
            self.work_date = time.strftime(kw['work_date'], '%Y-%m-%d').time()
        if 'origin' in kw:
            self.origin = kw['origin']
        if 'phone1' in kw:
            self.phone1 = kw['phone1']
        if 'phone2' in kw:
            self.phone2 = kw['phone2']
        if 'address' in kw:
            self.address = kw['address']
        if 'email' in kw:
            self.email = kw['email']
        if 'techlevel_id' in kw:
            self.techlevel_id = kw['techlevel_id']
        if 'others' in kw:
            self.others = kw['others']

    def __repr__(self):
        return u'<Employee {}>' .format(self.id)

    @classmethod
    def list_all(cls):
        return Employee.query.order_by(Employee.id).all()

    @classmethod
    def getEmployeeById(cls, eid):
        return Employee.query.filter_by(id = eid).first();

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


    # @classmethod
    # def updatePhoto(cls, eid, photo_url):
    #     '''根据员工id更新图片
        
    #     Arguments:
    #         eid {str} -- 员工id
    #         photo_url {str} -- 图片路径
        
    #     Returns:
    #         [int] -- 响应码。200-成功，500-失败
        
    #     Raises:
    #         e -- 更新异常
    #     '''
    #     response = 200
    #     try:
    #         Employee.query.filter_by(id = eid).update({'photo_url': photo_url})
    #         db.session.commit()
    #     except Exception as e:
    #         print e
    #         db.session.rollback()
    #         response = 500
    #         raise e            
    #     finally:
    #         return response

    @classmethod
    def getEmployeeById(cls, eid):
        # print eid
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
            print e
            response_code = 500
            db.session.rollback()
            raise e
        else:
            return response_code