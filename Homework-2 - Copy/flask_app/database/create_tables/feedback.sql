CREATE TABLE feedback (
    comment_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    comment VARCHAR(1000) NOT NULL
);