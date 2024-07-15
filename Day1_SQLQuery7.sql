-- creating procedure

create procedure sp_gme as
select * from gme.emp_location_test
go

exec sp_gme