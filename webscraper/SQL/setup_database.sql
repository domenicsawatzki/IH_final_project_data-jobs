-- Active: 1691744613924@@127.0.0.1@3306
USE final_project;
CREATE TABLE IF NOT EXISTS linked_in_scrap
(
id INTEGER PRIMARY KEY,
title varchar(50),
company varchar(50),
city varchar(50),
posting_date date,
job_description JSON,
seniority_level varchar(50),
job_function varchar(50),
industries varchar(50),
scraping_date date,
url varchar(500),
keyword varchar(50)
)
;


CREATE TABLE IF NOT EXISTS soup_archiv
(
id INTEGER PRIMARY KEY,
little_soup json
);

