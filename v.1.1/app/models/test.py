# -*- coding: utf-8 -*-
import sys
sys.path.append('E:\\Programming\\PersonnelManagement\\v.1.1\\app')
from users import User

user = User('test', '123')
print user.pw_hash
