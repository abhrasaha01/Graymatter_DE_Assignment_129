-- Creating and testing temp table

create table #gmetbl1
(emp_id int, emp_name varchar(40), emp_city varchar(30))

insert into #gmetbl1
select * from gme.emp_location_test

select * from #gmetbl1