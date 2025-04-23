CREATE TABLE dummy_data (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO dummy_data (name) VALUES ('Alice'), ('Bob'), ('Charlie');
