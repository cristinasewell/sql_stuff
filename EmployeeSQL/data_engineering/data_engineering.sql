-- drop tables if they exist
drop table departments CASCADE;
drop table dept_emp CASCADE;
drop table dept_manager CASCADE;
drop table employees CASCADE;
drop table salaries CASCADE;
drop table titles CASCADE;

-- create the tables that have primary keys only and not foreign keys
-- Departments table
create table departments (
	dept_no varchar(40) not null,
	dept_name varchar(40) not null,
	primary key (dept_no)
);

-- what do we have in the departments
select * from departments

-- Titles table
create table titles (
	title_id varchar not null,
	title varchar not null,
	primary key (title_id)
);

select * from titles

-- Employees table will have a foreign key for the emp_title_id
create table employees (
	emp_no int not null,
	emp_title_id varchar(40) not null,
	birth_date date not null,
	first_name character varying(40) not null,
	last_name character varying(40) not null,
	sex char(1) not null,
	hire_date date not null,
	primary key (emp_no),
	foreign key (emp_title_id) references titles.title_id
);

select * from employees

create table dept_emp (
	emp_no int not null,
	dept_no varchar(40) not null,
	foreign key (emp_no) references employees(emp_no),
	foreign key (dept_no) references departments(dept_no),
	-- the composite key
	primary key(emp_no, dept_no)
);

select * from dept_emp

create table dept_manager (
	dept_no varchar(40) not null,
	emp_no int not null,
	foreign key (dept_no) references departments(dept_no),
	foreign key (emp_no) references employees(emp_no)
	-- the composite key
	primary key (dept_no, emp_no)
);

select * from dept_manager

create table salaries (
	emp_no int not null,
	salary int not null,
	foreign key (emp_no) references employees.emp_no
);

-- 1 

-- AVG - average of a set of values
-- COUNT - counts the rows in a specific table or view
-- MIN - min of set values
-- MAX - max of set values
-- SUM - sum of set values

-- Aggregate functions used with:
-- group by
-- having
-- select

-- IMPORTANT: aggregate functions returns in random order!!

-- ORDER BY - ascending order by default or DESC - descending, LIMIT - limit the return
-- ROUND - to round after the decimal