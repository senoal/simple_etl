create table apipop (
	id serial,
	id_nation varchar (50),
	nation varchar (225),
	id_year int,
	year int,
	population int,
	slug_nation varchar(225),
	PRIMARY KEY (id)
)

select * from apipop