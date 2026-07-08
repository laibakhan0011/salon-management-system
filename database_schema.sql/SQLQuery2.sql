USE Salon_managment_system;

CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,  -- auto-increment primary key
    Username VARCHAR(50) NOT NULL UNIQUE,   -- no two users can share a username
    Password VARCHAR(255) NOT NULL,         -- will store bcrypt HASH, not plain text
    Role VARCHAR(20) NOT NULL CHECK (Role IN ('Admin', 'Receptionist'))
);