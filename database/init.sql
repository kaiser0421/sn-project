CREATE DATABASE sndb;
\c sndb

CREATE TABLE users (
    "id" SERIAL PRIMARY KEY,
    "username" varchar(32) UNIQUE NOT NULL ,
    "password" varchar(32) NOT NULL,
    "password_retry" integer DEFAULT 0 NOT NULL,
    "updated_on" timestamp NOT NULL
);