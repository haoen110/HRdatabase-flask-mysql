# HR Database

> A mini HR database built with flask, MySQL and bootstrap templates.

## Requirements

- Platform: OSX-64
- Language: Python3.7.4
- Web Framework: Flask
- Environment: conda
- IDE: PyCharm Professional Edition
- Database: MySQL
- Front End: Bootstrap tamplates (HTML, JavaScript)

## Functions

### Registration

- Registration constraint (username length / pwd confirmation).
    - By using `wtforms` to give constraint.
- Storing information in MySQL with hashed password and timestamp.
    - By using `SQLAlchemy` and `pymysql` to interact with database and `sha256_crypt` to encrypt password.
    
### Login

- Compare with information stored in database.
- Acquire information of user after logged in.
    - Implement by `session.username` in html.
- All the information available after logged in. 
    - Define a function with `session[logged_in]`

### Change User

- Return the login page and clear the session to logout.

### Add and Delete New Recruitment

- Add an employee with his or her name, age, gender, salary, address, department and contract.
- Show added data after executed the process.
- Table form will provide a simple search function.
- Every ends of columns are delete buttons which can be used to delete this record.     

### Employees Description

- Show the entire information of employees.
- Introduce Fuzzy search on name / gender / department to search a specified employee.
- Implement some basic visualization function below the search table.

### Department Description

- Illustrate the basic information of departments.
- Visualize the department budgets by bar chart.
- Visualize the people distribution by pie chart.

### Contracts Description

- Illustrate the basic information of contracts (start, end).
- Visualize the number of contracts made at history time line.

### Attendance Description

- Illustrate the attendance information of all employees among these years.

## Requirements
  
### Packages

```python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, request, redirect, url_for, logging, session
from wtforms import Form, StringField, TextAreaField, PasswordField, IntegerField, validators
from passlib.hash import sha256_crypt
from functools import wraps
```

### Database
```mysql
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

--
select cid, contracts.eid, ename, employees.department, contracts.start_date, contracts.finish_date
from employees, contracts
where employees.eid = contracts.eid;

```

