DROP TABLE IF EXISTS likes, owns, gender_pref, species_pref, age_pref, caretakers, pets, areas, species, gender, CASCADE;

-- Area
CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Caretaker
CREATE TABLE caretakers (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    area INT REFERENCES areas(id)
);

-- Gender
CREATE TABLE gender (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Species
CREATE TABLE species (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Pets
CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender INT REFERENCES gender(id),
    image_url VARCHAR(255) NOT NULL,
    description TEXT,
    species INT REFERENCES species(id),
    caretaker_id INT REFERENCES caretakers(id)
);

-- Preferences
CREATE TABLE species_pref (
    pet_id INT REFERENCES pets(id),
    species_id INT REFERENCES species(id),
    PRIMARY KEY (pet_id, species_id)
);

CREATE TABLE gender_pref (
    pet_id INT REFERENCES pets(id),
    gender_id INT REFERENCES gender(id),
    PRIMARY KEY (pet_id, gender_id)
);

CREATE TABLE age_pref (
    pet_id INT PRIMARY KEY REFERENCES pets(id),
    age_from INT NOT NULL,
    age_to INT NOT NULL
);

-- Owns (caretaker-to-pet) [optional, implicit through caretaker_id]
CREATE TABLE owns (
    caretaker_id INT REFERENCES caretakers(id),
    pet_id INT REFERENCES pets(id),
    PRIMARY KEY (caretaker_id, pet_id)
);

-- Default gender values
INSERT INTO gender (name) VALUES 
('Male'), 
('Female'), 
('Other');

-- Default species values
INSERT INTO species (name) VALUES 
('Dog'), 
('Cat'), 
('Bird'), 
('Rabbit'), 
('Hamster'), 
('Fish'), 
('Turtle'), 
('Lizard'), 
('Horse'), 
('Cow'), 
('Pig');

-- Default areas in Denmark
INSERT INTO areas (name) VALUES
('Capital Region'),
('Central Jutland'),
('North Jutland'),
('Zealand'),
('South Denmark');