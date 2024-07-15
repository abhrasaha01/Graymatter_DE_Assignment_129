-- creating index

create index idx_sample
on Person.Person(
BusinessEntityID,
PersonType
)

select * from Person.Person