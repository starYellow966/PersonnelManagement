create table if not exists OrganizationType(
id varchar(30) primary key,
name varchar(50) unique
)CHARSET=utf8;

create table if not exists Organization(
id varchar(30) primary key,
name varchar(50) unique,
type_id varchar(30) not null,
parent_id varchar(30) not null,
foreign key (type_id) references OrganizationType(id)
on delete cascade
on update cascade,
foreign key (parent_id) references Organization(id)
on delete cascade
on update cascade
)CHARSET=utf8;

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