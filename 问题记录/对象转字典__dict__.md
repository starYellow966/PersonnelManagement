### 问题描述
在使用 flask-sqlalchemy 获得一个包含多个 Employee 对象的list，在循环这个list时，将每个对象利用 `__dict__` 属性转换成字典时，经常出现丢失部分键值对。但在使用 `__dict__` 之前先引用一次对象，如 `print obj` 再使用 `print obj.__dict__`，就不会丢失键值对

即在使用`obj.__dict__`前，要使用一次`obj`。

### 问题分析
目前觉得是属性 `__dict__` 使用不当造成，没有明白该属性的原理
感觉跟 flask-sqlalchemy 有关

正常的实例
```python
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

            
@fresh_login_required
@employeeBlueprint.route('/scan/list_all')
def scan_list_all():
    employee_list = employee.Employee.list_all().data
    for x in employee_list:
        x['org_name'] = organization.Organization.getNameById(x['org_id'])
        x['political_status'] = dictionary.Dictionary.getNameById(x['political_status_id']).data
        x['emp_type_name'] = dictionary.Dictionary.getNameById(x['emp_type']).data
        x['position'] = dictionary.Dictionary.getNameById(x['position_id']).data
    return json.dumps(employee_list)
```

异常的实例
```python

@classmethod
    def list_all(cls):
        return Employee.query.filter_by(isUse = 1).order_by(Employee.id).all()

@fresh_login_required
@employeeBlueprint.route('/scan/list_all')
def scan_list_all():
    employee_list = employee.Employee.list_all()
    result = []
    for x in employee_list:
        print x # 别注释，不print x，下面的x.__dict__无法正常调用
        if x is not None:
            temp = {}
            temp.update(x.__dict__)
            del temp['_sa_instance_state']
            temp['org_name'] = organization.Organization.getNameById(x.org_id)
            temp['political_status'] = dictionary.Dictionary.getNameById(x.political_status_id).data
            temp['emp_type_name'] = dictionary.Dictionary.getNameById(x.emp_type).data
            temp['position'] = dictionary.Dictionary.getNameById(x.position_id).data
            result.append(temp)
    return json.dumps(result)
```