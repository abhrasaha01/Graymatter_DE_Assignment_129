create view vw_sample as
select 
BusinessEntityID, 
PersonType 
from Person.Person

select * from vw_sample

select * from Person.Person