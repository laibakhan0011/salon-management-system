USE Salon_managment_system;

UPDATE Users SET Email = 'admin1@salon.com' WHERE Username = 'admin1';
UPDATE Users SET Email = 'reception1@salon.com' WHERE Username = 'reception1';

ALTER TABLE Users
ALTER COLUMN Email VARCHAR(100) NOT NULL;

ALTER TABLE Users
ADD CONSTRAINT UQ_Users_Email UNIQUE (Email);