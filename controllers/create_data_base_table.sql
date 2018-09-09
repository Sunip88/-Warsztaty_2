CREATE DATABASE warsztaty_2;

CREATE TABLE users
(
id serial,
username VARCHAR (255),
hashed_password VARCHAR(255),
email VARCHAR (255) unique,
PRIMARY KEY (id)
);

CREATE TABLE message
(
id serial,
from_id int,
to_id int,
message text,
creation_date timestamp,
PRIMARY KEY (id)
);





