-- create and testing views

create view vw_public as
select BusinessEntityID,
EmailAddress,
EmailAddressID
from person.EmailAddress order by BusinessEntityID

select * from vw_public

select * from person.EmailAddress