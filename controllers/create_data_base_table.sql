CREATE DATABASE warsztaty_2;

CREATE TABLE users
(
id serial,
username VARCHAR (255),
hashed_password VARCHAR(255),
email VARCHAR (255) unique
);




