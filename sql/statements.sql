-- create database and set encode mode as 'utf-8'
create database sdsc5003 character set utf8;

-- switch to sdsc5003
use sdsc5003;

-- create a table to store the information of users
create table users(
    id int(11) auto_increment primary key,
    username varchar(30),
    email varchar(100),
    password varchar(100),
    register_date timestamp default current_timestamp);

-- create employees' table
create table employees(
    eid int primary key,
    ename varchar(30),
    gender varchar(10),
    age int,
    salary int,
    department varchar(30),
    address varchar(30));

-- load data from csv -- cp employees.csv /usr/local/mysql/data/sdsc5003/
load data infile 'employees.csv'
into table employees
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;

-- create departments' table
create table departments(
	did int primary key,
	dname varchar(30),
	meid int,
	mname varchar(30),
	budget int);

-- load data from csv -- cp departments.csv /usr/local/mysql/data/sdsc5003/
load data infile 'departments.csv'
into table departments
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;

-- create contracts' table
create table contracts(
	cid int primary key,
	eid int,
	did int,
	start_date date,
	v_start_date varchar(10),
	finish_date date,
	v_finish_date varchar(10),
	foreign key (eid) references employees (eid),
	foreign key (did) references departments (did));

-- load data from csv -- cp contracts.csv /usr/local/mysql/data/sdsc5003/
load data infile 'contracts.csv'
into table contracts
fields terminated by ','
lines terminated by '\n'
ignore 1 lines
(cid, eid, did, v_start_date, v_finish_date);
update contracts SET start_date = STR_TO_DATE(v_start_date, '%m/%d/%Y');
update contracts SET finish_date = STR_TO_DATE(v_finish_date, '%m/%d/%Y');
alter table contracts drop v_start_date;
alter table contracts drop v_finish_date;

-- create attendance table
create table attendance_owned(
	aid int,
	eid int,
	on_work int,
	off_work int,
    primary key (aid, eid),
    foreign key (eid) references employees (eid) on delete cascade);

-- load data from csv -- cp attendance.csv /usr/local/mysql/data/sdsc5003/
load data infile 'attendance.csv'
into table attendance_owned
fields terminated by ','
lines terminated by '\n'
ignore 1 lines;

-- count the number of employees in each departments
select * from departments,
(select emp.department, count(emp.eid) as Total
from employees emp
group by emp.department
order by emp.department) as tp
where departments.dname = tp.department;


