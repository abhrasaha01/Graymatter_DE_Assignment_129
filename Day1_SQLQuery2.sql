-- testing select, join and group by commands

select * from Person.ContactType

select * from Person.BusinessEntityContact

select 
c.ContactTypeID, 
count(b.BusinessEntityID) as quantity
from Person.ContactType c left join Person.BusinessEntityContact b
on c.ContactTypeID = b.ContactTypeID
group by c.ContactTypeID