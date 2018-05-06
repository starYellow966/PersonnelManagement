## 进度
- 2018-3-7 完成段信息批处理操作，包括下载格式文件，上传excel文件，但细节上异常处理、查重以及界面没有完成
- 2018-3-14 完成v1.1版本，合并了组织机构的表，把v1.0的功能全部移植成功
- 2018-3-15 完成v1.1版本中新增，修改的有效性检查，导出功能
- 2018-3-17 完成数据字典管理中的删除、批处理以及导出功能
- 2018-3-18 完成数据字典管理中的新增以及修改（包括了查重处理），彻底完成数据字典管理模块；另外，初步完成登录功能，但界面以及具体使用依旧不懂
- 2018-3-20 初步完成了用户登录以及功能访问受限的问题，但未经测试不大稳定的样子。着手日记部分的编程
- 2018-3-21 完成日志的显示,以及对字典数据管理操作进行记录，没有用设计模式，dictionary和log类耦合度高
- 2018-3-28 完成了组织表的修改，同时成功用树状图treeview显示，python的json转js的json好烦
- 2018-4-9 调整一下项目结构，完成图片上传并保存路径在数据库
- 2018-4-12 完成人员信息管理的查看、查询以及修改；但字段不完整且性别单选框有问题
- 2018-4-17 完成组织机构管理的新、删、改、查以及人员浏览页面；批处理没有做
- 2018-4-20 完成员工详情信息页面，以及Employee表
- 2018-4-22 完成员工详情信息页面展示页面，修改了employe_manager，使其点击树状菜单有不同的响应。同时完成了填写员工信息的页面布局
- 2018-4-23 完成了新增员工信息中从前端到后端的数据传输，后端数据处理没有完成
- 2018-4-26 完成了员工新增、删除以及修改前后端的开发，并写了web前端开发接口文档。
- 2018-5-2  完成了变动管理的界面设计（细节有待调整），并成功进行内部变动，但日志这块没有完成
- 2018-5-6 完成了新进人员、减少人员、批量新进人员、内部变动、定职管理、统计分析的后前端开发，还差异常处理以及日志未完成。

## 使用说明
- 针对谷歌浏览器，如果使用“批量导入功能”时需要关闭迅雷插件，否则无法下载格式文件*

## 代码说明
- TODO 代表尚未完成的功能需要日后完成的
- FIXME 代表此处代码需要修改
- Warning 代表注意事项，可能需要增加异常处理

## 版本说明
- 1.0-----组织机构表是分别的，即分为段表，车间表以及班组表*
- 1.1-----组织机构表是合并在一起的，即段，车间以及班组公用一个表，组织类型再用一个表表示*

## 待完成任务
- 运用flask_wtf 生成自定义登录表单,同时尝试去将数据字典新增表单改写成FlaskForm并自定义验证 [参考文献](https://zhuanlan.zhihu.com/p/23605845) [flask-wtf官方文档](https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms) 
- mysql密码的存储，不能使用明文存储
- 修改html，刷新页面，依旧使用原来的html(问题出在Bootstrap(app))
- 好好了解一下浏览器对页面的缓存
- 好好阅读flask的官方文档，尤其是context（上下文）这块
- cookie时间设置
- 头像图片压缩
- 

## 问题记录
- 切换网络，出现异常StatementError: (sqlalchemy.exc.InvalidRequestError) Can't reconnect until invalid transaction is rolled back [SQL: u'SELECT `User`.id AS `User_id`, `User`.name AS `User_name`, `User`.password AS `User_password` \nFROM `User` \nWHERE `User`.id = %s'] [parameters: [{'%(78380168 param)s': 1}]]
