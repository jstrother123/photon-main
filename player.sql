--Create table
CREATE TABLE player (
  id INT,
  first_name VARCHAR(30),
  last_name VARCHAR(30),
  codename VARCHAR(30)
);

--Place first record into table
INSERT INTO player (id, first_name, last_name, codename)
VALUES (1, 'Jim', 'Strother', 'Opus');

