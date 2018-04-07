# -*- coding: utf-8 -*-
# from dictionary import DictionaryType,Dictionary
# from operate_log import Log
from organization import Organization
from employee import Employee

for x in Employee.query.with_entities(Employee.id, Employee.name).all():
    print x.id
    print x.name

