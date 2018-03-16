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