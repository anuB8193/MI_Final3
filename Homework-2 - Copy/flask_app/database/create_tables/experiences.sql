CREATE TABLE experiences (
    experience_id SERIAL PRIMARY KEY,
    position_id INT REFERENCES positions(position_id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    hyperlink VARCHAR(255),
    start_date DATE,
    end_date DATE
);
