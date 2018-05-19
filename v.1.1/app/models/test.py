# -*- coding: utf-8 -*-
import sys
sys.path.append('E:\\Programming\\PersonnelManagement\\v.1.1\\app')
# from users import User


def test():
    try:
        return 'hello'
    except Exception as e:
        raise e
    finally:
        return 'finally'

