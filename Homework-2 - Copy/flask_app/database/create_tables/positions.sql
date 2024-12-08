CREATE TABLE positions (
    position_id INT GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1) PRIMARY KEY,
    inst_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    responsibilities VARCHAR(500) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE DEFAULT NULL,
    FOREIGN KEY (inst_id) REFERENCES institutions(inst_id)
);
