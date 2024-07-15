-- creating database

create database gmadmin

use gmadmin

create schema gme

create table gme.emp_location_test(
emp_id int primary key identity(1,1),
emp_name varchar(30),
emp_city varchar(30)
)

alter table gme.emp_location_test
add constraint valid_id
check (emp_id < 60)

insert into gme.emp_location_test (emp_name, emp_city) values ('harsh','blr')

alter table gme.emp_location_test
alter column emp_name varchar(40)

select * from gme.emp_location_test