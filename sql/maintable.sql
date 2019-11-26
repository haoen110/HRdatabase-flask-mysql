CREATE TABLE employees (
	eid INT,
	ename VARCHAR ( 30),
	gender VARCHAR ( 10 ),
	age INT,
	salary REAL,
	department VARCHAR(30),
	address VARCHAR ( 30),
	PRIMARY KEY ( eid ) 
);
CREATE TABLE department (
	did INT,
	dname VARCHAR(30),
	meid INT,
	mname VARCHAR(30),
	budget INT,
	PRIMARY KEY ( did )
);

CREATE TABLE contract (
	cid INT,
	eid INT,
	did INT,
	start_date date,
	finish_date date,
	PRIMARY KEY ( cid ),
	FOREIGN KEY ( eid ) REFERENCES employees ( eid ),
	FOREIGN KEY ( did ) REFERENCES department ( did ) 
);

CREATE TABLE attendence_owned (
	aid INT,
	eid INT,
	off_work INT,
	on_work INT,
PRIMARY KEY ( aid, eid ),
FOREIGN KEY ( eid ) REFERENCES employees ( eid ) ON DELETE CASCADE
);