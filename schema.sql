DROP DATABASE IF EXISTS pet_tinder_test;
CREATE DATABASE pet_tinder_test;
CREATE TABLE areas(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE caretakers(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    area INT,
    FOREIGN KEY (area) REFERENCES areas(id)
);
CREATE TABLE pets(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    species VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caretaker_id INT,
    FOREIGN KEY (caretaker_id) REFERENCES caretakers(id)
);