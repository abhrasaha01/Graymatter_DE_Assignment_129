-- testing cte

with adv_cte as(
select * from Person.Address)
select AddressID, AddressLine1, AddressLine2 from adv_cte