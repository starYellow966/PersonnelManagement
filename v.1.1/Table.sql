-- create table if not exists OrganizationType(
-- id varchar(30) primary key,
-- name varchar(50) unique
-- )CHARSET=utf8;

-- create table if not exists Organization(
-- id varchar(30) primary key,
-- name varchar(50) unique,
-- type_id varchar(30) not null,
-- parent_id varchar(30) not null,
-- foreign key (type_id) references OrganizationType(id)
-- on delete cascade
-- on update cascade,
-- foreign key (parent_id) references Organization(id)
-- on delete cascade
-- on update cascade
-- )CHARSET=utf8;

create table if not exists DictionaryType(
id int primary key AUTO_INCREMENT,
name varchar(50) unique
)CHARSET=utf8;

insert into DictionaryType(name) values('用工性质');
insert into DictionaryType(name) values('民族');
insert into DictionaryType(name) values('学历');
insert into DictionaryType(name) values('学位');
insert into DictionaryType(name) values('职名');
insert into DictionaryType(name) values('政治面貌');
insert into DictionaryType(name) values('人员状态');
insert into DictionaryType(name) values('转干方式');
insert into DictionaryType(name) values('岗位档次');
insert into DictionaryType(name) values('技能档次');
insert into DictionaryType(name) values('所属单位');

create table if not exists Dictionary(
id varchar(30) primary key,
name varchar(50) not null,
type_id int not null,
foreign key(type_id) references DictionaryType(id)
on delete cascade
on update cascade
)CHARSET=utf8;

create table if not exists User(
id int primary key AUTO_INCREMENT,
name varchar(64) unique,
password varchar(64) not null
)CHARSET=utf8;

create table if not exists Log(
id int primary key AUTO_INCREMENT,
user_id int not null,
ip_address varchar(20) not null,
event_type varchar(20) not null,
info varchar(100)
)CHARSET=utf8;

create table if not exists Organization(
id varchar(20) primary key,
name varchar(50) unique,
status tinyint(1) not null, --0代表虚拟节点，1代表实节点；如name=车间就是虚拟节点
level tinyint not null,
parent_id varchar(20),
num int ,
foreign key(parent_id) references Organization(id)
on delete cascade
on update cascade
)CHARSET=utf8;

insert into Organization(id,name,status,level) values('0000000','成都客运段',0,0);
insert into Organization(id,name,status,level,parent_id,num) values('0000001','段领导',0,1,'0000000',0);
insert into Organization(id,name,status,level,parent_id,num) values('0000002','车间',0,1,'0000000',1);
insert into Organization(id,name,status,level,parent_id,num) values('0000003','成都车队',1,2,'0000002',0);
insert into Organization(id,name,status,level,parent_id,num) values('0000004','成都1队',1,3,'0000003',0);
insert into Organization(id,name,status,level,parent_id,num) values('0000005','段长',1,2,'0000001',0);
insert into Organization(id,name,status,level,parent_id,num) values('0000006','副段长',1,2,'0000001',1);

-- 打算创建一个简单的员工信息表和一个详细的员工信息表
-- 两者区别：前者用于树状结构，因为树状结构需要的字段少；后者用于展示详情
create table if not exists Employee(
id varchar(20) primary key,
name varchar(30) not null,
sex tinyint(1),
org_id varchar(20) not null, --所属部门
foreign key(org_id) references Organization(id)
on delete cascade
on update cascade,
emp_type varchar(30) , --用工性质
unit varchar(10) default '成都客运段', --所属单位
photo_url varchar(200)
)CHARSET=utf8;


-- create table if not exists Person(
-- id varchar(20) primary key,
-- name varchar(30) not null,
-- emp_typeid varchar(30) not null,
-- unit varchar(10) not null default('成都客运段'),
-- org_id varchar(10) not null,
-- position_id varchar(30) not null,
-- status varchar(10) not null,
-- old_name varchar(30),
-- sex tinyint(1),
-- recordnum varchar(20),
-- foreign key(emp_typeid) references Dictionary(id)
-- on delete cascade
-- on update cascade,
-- foreign key(org_id) references Organization(id)
-- on delete cascade
-- on update cascade,
-- foreign key(position_id) references Dictionary(id)
-- on delete cascade
-- on update cascade
-- )CHARSET=utf8;