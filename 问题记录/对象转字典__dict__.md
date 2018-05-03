### 问题描述
在使用 flask-sqlalchemy 获得一个包含多个 Employee 对象的list，在循环这个list时，将每个对象利用 `__dict__` 属性转换成字典时，经常出现丢失部分键值对。但在使用 `__dict__` 之前先引用一次对象，如 `print obj` 再使用 `print obj.__dict`，就不会丢失键值对

### 问题分析
目前觉得是属性 `__dict__` 使用不当造成，没有明白该属性的原理