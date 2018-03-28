/*CREATE TABLE IF NOT EXISTS OrgType(
id int primary key AUTO_INCREMENT,
name varchar(10) not null
)CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Org(
id int primary key AUTO_INCREMENT,
num varchar(20) unique,
name varchar(20) not null,
typeid int not null,
foreign key(typeid) references OrgType(id) on delete cascade on update cascade
)CHARSET=utf8;
*/

#客运段
create table if not exists Segment(
id char(10) primary key,       #编码
name varchar(20) not null, #客运段名称
stype varchar(10) not null default '客运段', #部门类型
dep_name varchar(20) not null, #部门名称
seg_date int(10) not null default 0, #成立时间
railway varchar(20) not null   #所属铁路局
)CHARSET=utf8;


#车间
create table if not exists Workshop(
id char(10) primary key,  #编号
name varchar(20) not null, #车间名称
wtype varchar(10) not null default '车间', #部门类型
dep_name varchar(20) not null, #部门名称
seg_id char(10) not null, #所属客运段
num int,  #序号
FOREIGN KEY (seg_id) REFERENCES Segment (id) 
on delete cascade
on update cascade
)CHARSET=utf8;

#班组
create table if not exists Team(
id char(10) primary key, #编号
name varchar(20) not null, #班组名称
type varchar(10) not null default '班组', #部门类型 
dep_name varchar(20) not null, #部门名称
work_id char(10) not null, #所属车间
num int, #序号
foreign key(work_id) references Workshop(id) 
on delete cascade
on update cascade
)CHARSET=utf8;

#数据字典类型
create table if not exists DicType(
id int primary key AUTO_INCREMENT, #编号
name char(10) not null #类型名称
)CHARSET=utf8;

#数据字典
create table if not exists Dictionary(
id char(10) primary key, #编号
name varchar(20) not null, #名称
type_id int not null,
foreign key(type_id) references DicType(id)
on delete cascade
on update cascade
)CHARSET=utf8;

/*#日志
create table if not exists Log(
id int primary key AUTO_INCREMENT, #编号
log_time int(10) not null, #时间
description varchar(50) not null, #事件描述
user_id char(10) not null, #用户id
foreign key(user_id) references User(id)
on delete cascade
on update cascade
)charset=utf8;
*/
insert into Segment(id,name,dep_name,seg_date,railway) values('0901','成都客运段','成都客运段',183052800,'成都铁路局');

insert into Workshop(id,name,dep_name,seg_id) values('1090','北京车队','北京车队','0901');
insert into Workshop(id,name,dep_name,seg_id) values('1091','上海车队','上海车队','0901');

insert into Team(id,name,dep_name,work_id) values('2090','上海1班','上海1班','1091');
insert into Team(id,name,dep_name,work_id) values('2091','北京1班','北京1班','1090');

	