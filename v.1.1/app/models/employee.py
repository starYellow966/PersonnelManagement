# -*- coding: utf-8 -*-
# 设置默认编码
# import sys
# reload(sys);
# sys.setdefaultencoding("utf-8")
from extensions import db
# from db_helper import db
from organization import TreeNode,Organization
from dictionary import Dictionary   
from response_object import ResponseObject 
from operate_log import Log

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
        # print 'finish setOption'

    def __repr__(self):
        return u'<Employee {} {}>' .format(self.id, self.name)

    @classmethod
    def list_all(cls):
        response = ResponseObject(data = [])
        try:
            result = Employee.query.filter_by(isUse = 1).order_by(Employee.id).all()
            for x in result:
                temp = {}
                temp.update(x.__dict__)
                del temp['_sa_instance_state']
                response.data.append(temp)
        except Exception as e:
            print e
            response.set_fail(None)
            raise e
        finally:
            return response
        

    @classmethod
    def getEmployeeById(cls, eid):
        return Employee.query.filter_by(id = eid, isUse = 1).first()

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

    @classmethod
    def list_all_practice(cls):
        response = ResponseObject(data = [])
        try:
            result = Employee.query.with_entities(Employee.id, Employee.name, Employee.org_id, Employee.position_id, Employee.emp_type).filter_by(is_Practice = 1, isUse = 1).all() #获得属于当前节点的员工信息
            for x in result:
                response.data.append({'id': x[0], 'name': x[1], 'org_id': x[2], 'position_id': x[3], 'emp_type': x[4]})
        except Exception as e:
            print e
            response.set_fail([])
            raise e
        finally:
            return response

    def insert(self):
        response = ResponseObject()
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            response.set_fail()
            raise e
        finally:
            Log.createLog('Insert', u'插入员工数据{id:' + self.id + ',name:' + self.name + '}'
                ).insertLog(response.message)
            return response

    @classmethod
    def remove(cls, id_list):
        response = ResponseObject()
        try:
            for x in id_list:
                e = Employee.query.filter_by(id = x).update({'isUse': 0})
                # if (e is not None):
                #     db.session.delete(e)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            response.set_fail()
            raise e
        finally:
            Log.createLog('Delete', u'删除员工数据id{' + ''.join(id_list) + u"}"
                ).insertLog(response.message)
            return response

    def update(self):
        response = ResponseObject()
        try:
            Employee.query.filter_by(id = self.id).update({
                'name': self.name,
                'old_name': self.old_name,
                'photo_url': self.photo_url,
                'emp_type': self.emp_type,
                'sex': self.sex,
                'org_id': self.org_id,
                'status_id': self.status_id,
                'position_id': self.position_id,
                'id_num': self.id_num,
                'political_status_id': self.political_status_id,
                'nation_id': self.nation_id,
                'degree_id': self.degree_id,
                'birthdate': self.birthdate,
                'work_date': self.work_date,
                'origin': self.origin,
                'phone1': self.phone1,
                'phone2': self.phone2,
                'address': self.address,
                'email': self.email,
                'techlevel_id': self.techlevel_id,
                'others': self.others
                });
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            response.set_fail()
            raise e
        finally:
            Log.createLog('Update', u'修改{工号:' + self.id + ',名字:'+ self.name + '}员工数据'
                ).insertLog(response.message)
            return response

    @classmethod
    def inside_change(cls, id, org_id, position_id, change_date, **kw):
        response = ResponseObject()
        try:
            id_list = ''.join(id).split(',')
            for x in id_list:
                Employee.query.filter_by(id = x).update({
                    'org_id': ''.join(org_id),
                    'position_id': ''.join(position_id)
                    })
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            response.set_fail()
            raise e
        finally:
            return response

    @classmethod
    def formal_update(cls, id, change_date, report_date, **kw):
        response = ResponseObject()
        update_dict = {'is_Practice': 0}
        if 'org_id' in kw:
            update_dict['org_id'] = ''.join(kw['org_id'])
        if 'position_id' in kw:
            update_dict['position_id'] = ''.join(kw['position_id'])
        try:
            id_list = ''.join(id).split(',')
            for x in id_list:
                Employee.query.filter_by(id = x).update(update_dict)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            response.set_fail()
            raise e
        finally:
            return response

    @classmethod
    def statistics_column(cls, column_name):
        '''查询柱状图统计数据
        
        Arguments:
            column_name {str} -- Employee表字段名
        
        Returns:
            [ResponseObject] -- message代表操作码
                                data代表数据，data包含name,value,color三个字段
        
        Raises:
            e -- [description]
        '''
        response = ResponseObject(data = [])
        color = ['#3A68D3', '#9F2626', '#2A962A', '#3895BF', '#4267BE', '#4F7DE7', '#7A3C9C', '#B97944', 
            '#782A56', '#484848', '#FFFF33', '#FF3333', '#FFCC33', '#009966', '#99CC00']
        try:
            sql = 'select {0}, count(*) from Employee group by {0} order by count(*) desc'.format(column_name)
            result = db.session.execute(sql).fetchall()
            index = 0
            for x in result:
                temp = {'name':'', 'value':'', 'color':color[index]}
                index = (index + 1) % len(color)
                if column_name == 'sex':
                    temp['name'] = u'男' if x[0] == 1 else u'女'
                elif column_name == 'org_id':
                    temp['name'] = Organization.getNameById(x[0])
                else:
                    temp['name'] = Dictionary.getNameById(x[0]).data
                temp['value'] = x[1]
                response.data.append(temp)
            # print response.data
        except Exception as e:
            print e
            response.set_fail(None)
            raise e
        finally:
            return response

    @classmethod
    def statistics_pie(cls, column_name):
        '''查询柱状图统计数据
        
        Arguments:
            column_name {str} -- 字段名
        
        Returns:
            [] -- [description]
        
        Raises:
            e -- [description]
        '''
        response = ResponseObject(data = [])
        try:
            response = Employee.statistics_column(column_name)
            total_count = db.session.execute('select count(1) from Employee').fetchall()[0][0]
            for x in response.data:
                x['value'] = round(x['value']* 100.0 / total_count, 1)
        except Exception as e:
            print e
            response.set_fail(None)
            raise e
        finally:
            return response

    @classmethod
    def create_employee_cn(cls, **row):
        '''专门针对批量新增功能，创建一个employee对象
        
        因为row中的key是字段名用中文表达，所以需要进行字段名转换
        
        Arguments:
            **row {dict} -- excel文件的一行数据
        '''
        # 直接映射表，这些字段可以直接转换
        direct_references = {u'工号': 'id', u'姓名': 'name', u'曾用名': 'old_name',u'籍贯': 'origin', 
            u'身份证号': 'id_num', u'联系电话': 'phone1',u'家庭住址': 'address', u'出生日期': 'birthdate', 
            u'电子邮箱':'email',u'入职日期': 'work_date', u'备注': 'others'}
        # Dictionary类映射表，与字典数据有关的字段
        dictionary_references = {u'用工性质': 'emp_type', u'职名': 'position_id', 
            u'人员状态': 'status_id',u'民族': 'nation_id', u'技能等级': 'techlevel_id', 
            u'学历': 'degree_id',u'政治面貌': 'political_status_id'}
        data = {}
        for x in row:
            if x in direct_references:
                data[direct_references[x]] = row[x]
            elif x in dictionary_references:
                d = Dictionary.get_id_by_name(row[x]).data
                if d == '':
                    d = None
                data[dictionary_references[x]] = d
            elif x == u'所属部门':
                o = Organization.get_id_by_name(row[x]).data
                if o == '':
                    o = None
                data['org_id'] = o
            elif x == u'性别':
                data['sex'] = (1 if row[x] == u'男' else 0)
            # elif x == u'是否实习':
            #     data['is_Practice'] = (1 if row[x] == u'是' else 0)
        print data
        e = Employee(**data)
        print e
        return e



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