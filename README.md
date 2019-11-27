# HR Database

> A mini HR database built with flask, MySQL and bootstrap templates.

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
- Visualize the number of 

### Attendance Description


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
CREATE DATABASE sdsc5003 CHARACTER SET utf8; 

-- switch to sdsc5003
USE sdsc5003;

-- create a table to store the infomation of users
CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY,
                   username VARCHAR(30),
                   email VARCHAR(100),
                   password VARCHAR(100),
                   register_date TIMESTAMP  DEFAULT CURRENT_TIMESTAMP);
```

