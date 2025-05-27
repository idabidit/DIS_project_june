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
    age INT NOT NULL,
    gender INT,
    FOREIGN KEY (gender) REFERENCES genders(id),
    image_url VARCHAR(255) NOT NULL,
    species INT,
    FOREIGN KEY (species) REFERENCES species(id),
    caretaker_id INT,
    FOREIGN KEY (caretaker_id) REFERENCES caretakers(id)
);
CREATE TABLE species(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE gender(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);