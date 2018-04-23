# -*- coding: utf-8 -*-
import sys
sys.path.append('E:\\Programming\\PersonnelManagement\\v.1.1\\app')
# print sys.path
# from dictionary import DictionaryType,Dictionary
# from operate_log import Log
d = {'1':'1'}
d['2'] = 2

print d

d = {'id':'1','sex':1,'org_id':'2','name':'hh','test':'ttt'}
id = d['id']
name = d['name']

class Person():
    def __init__(self, id, name, **kw):
        self.id = id
        self.name = name
        self.hh = hh
        print kw


p = Person(**d)