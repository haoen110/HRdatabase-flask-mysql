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

-- create a sample database that will be interacted by front-end interface
-- CREATE TABLE articles(id INT(11) AUTO_INCREMENT PRIMARY KEY,
--                       title VARCHAR(30),
--                       body VARCHAR(30),
--                       transactor VARCHAR(30),
--                       issue_date TIMESTAMP  DEFAULT CURRENT_TIMESTAMP)


CREATE TABLE employees(eid int PRIMARY KEY,
                       ename varchar(30),
                       gender varchar(10),
                       age int,
                       salary int,
                       department varchar(30),
                       address varchar(30));