CREATE TABLE areas(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE gender(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE species(
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
    FOREIGN KEY (gender) REFERENCES gender(id),
    image_url VARCHAR(255) NOT NULL,
    species INT,
    FOREIGN KEY (species) REFERENCES species(id),
    caretaker_id INT,
    FOREIGN KEY (caretaker_id) REFERENCES caretakers(id)
);
INSERT INTO areas (name) VALUES
('København K'), ('København N'), ('København Ø'), ('København S'), ('København V'), ('København SV'), ('København NV'), ('Frederiksberg');

INSERT INTO species (name) VALUES
('Dog'), ('Cat'), ('Rabbit'), ('Hamster'), ('Parrot'), ('Giraffe');

INSERT INTO gender (name) VALUES
('Female'), ('Male'), ('Other');

INSERT INTO caretakers (name, password, area) VALUES
('Thomas', '0013', 1),
('Alice', 'password123', 1),
('Bob', 'password456', 2),
('Charlie', 'password789', 3),
('Diana', 'password101112', 4),
('Ethan', 'password131415', 5),
('Fiona', 'password161718', 6);