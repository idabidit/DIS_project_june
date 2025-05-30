DROP TABLE IF EXISTS likes, owns, gender_pref, species_pref, age_pref, caretakers, pets, areas, species, gender, age_range CASCADE;

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

-- Age Range (for preference)
CREATE TABLE age_range (
    id SERIAL PRIMARY KEY,
    age_from INT NOT NULL,
    age_to INT NOT NULL
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
    caretaker_id INT REFERENCES caretakers(id),
    species_id INT REFERENCES species(id),
    PRIMARY KEY (caretaker_id, species_id)
);

CREATE TABLE gender_pref (
    caretaker_id INT REFERENCES caretakers(id),
    gender_id INT REFERENCES gender(id),
    PRIMARY KEY (caretaker_id, gender_id)
);

CREATE TABLE age_pref (
    caretaker_id INT REFERENCES caretakers(id),
    age_range_id INT REFERENCES age_range(id),
    PRIMARY KEY (caretaker_id, age_range_id)
);

-- Likes (pet-to-pet)
CREATE TABLE likes (
    pet_id INT REFERENCES pets(id),
    liked_pet_id INT REFERENCES pets(id),
    PRIMARY KEY (pet_id, liked_pet_id)
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
('Pig');

-- Default areas in Denmark
INSERT INTO areas (name) VALUES 
('Hovedstaden'),
('Midtjylland'),
('Nordjylland'),
('Sjælland'),
('Syddanmark');