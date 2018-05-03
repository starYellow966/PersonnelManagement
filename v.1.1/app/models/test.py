# -*- coding: utf-8 -*-
import sys
sys.path.append('E:\\Programming\\PersonnelManagement\\v.1.1\\app')
# print sys.path
# from dictionary import DictionaryType,Dictionary
# from operate_log import Log
# d = {'1':'1'}
# d['2'] = 2

# d = {'id':'1','sex':1,'org_id':'2','name':'hh','test':'ttt'}
# id = d['id']
# name = d['name']

# print [type(x) for x in d.itervalues()]

# def is_empty(s):
#     # s = ''.join(x)
#     return s and s.strip()

# print filter(is_empty, map(str,d.itervalues()))

# def log(text):
#     def decorator(func):
#         def wrapper(*args, **kw):
#             func(*args, **kw)
#             print '%s %s():' % (text, func.__name__)
#             # return func(*args, **kw)
#         return wrapper
#     return decorator

# @log('execute')
# def build(x, y):
#     print x + y
# print build(1,2)

class Foo(object):
    def __init__(self, func):
        print '__init__'
        self._func = func

    def __call__(self, *args):
        self.hh = args
        print self.hh
        print ('class decorator runing')
        self._func(args)
        print ('class decorator ending')

@Foo
def bar(*args):
    print(args)
    print ('bar')

bar()


def timethis(func):
    print 'hello'
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper