CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    experience_id INT REFERENCES experiences(experience_id),
    name VARCHAR(255) NOT NULL,
    skill_level INT CHECK (skill_level BETWEEN 1 AND 10)
);
