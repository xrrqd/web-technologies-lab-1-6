CREATE TABLE dealers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(200) NOT NULL,
    area VARCHAR(50),
    rating DECIMAL(2,1)
);
