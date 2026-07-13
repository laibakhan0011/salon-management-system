USE Salon_managment_system;
GO

-- 1. Loyalty Points column + AFTER INSERT trigger
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('Customer') AND name = 'LoyaltyPoints')
BEGIN
    ALTER TABLE Customer ADD LoyaltyPoints INT NOT NULL DEFAULT 0;
END
GO

DROP TRIGGER IF EXISTS trg_AddLoyaltyPoints;
GO

CREATE TRIGGER trg_AddLoyaltyPoints
ON Appointment
AFTER INSERT
AS
BEGIN
    UPDATE Customer
    SET LoyaltyPoints = LoyaltyPoints + 10
    FROM Customer C
    INNER JOIN inserted I ON C.CustomerID = I.CustomerID;
END;
GO

-- 2. PaymentLog table + AFTER DELETE trigger
IF OBJECT_ID('PaymentLog', 'U') IS NULL
BEGIN
    CREATE TABLE PaymentLog (
        LogID INT IDENTITY(1,1) PRIMARY KEY,
        PaymentID INT,
        AppointmentID INT,
        Amount DECIMAL(10,2),
        PaymentMethod VARCHAR(20),
        DeletedAt DATETIME DEFAULT GETDATE()
    );
END
GO

DROP TRIGGER IF EXISTS trg_LogDeletedPayments;
GO

CREATE TRIGGER trg_LogDeletedPayments
ON Payment
AFTER DELETE
AS
BEGIN
    INSERT INTO PaymentLog (PaymentID, AppointmentID, Amount, PaymentMethod)
    SELECT PaymentID, AppointmentID, Amount, PaymentMethod
    FROM deleted;
END;
GO

-- 3. Index on Customer_Phone(Phone)

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_CustomerPhone')
BEGIN
    CREATE INDEX idx_CustomerPhone ON Customer_Phone(Phone);
END
GO

-- 4. RANK() - staff ranked by revenue
SELECT 
    S.FirstName + ' ' + S.LastName AS StaffName,
    ISNULL(SUM(P.Amount), 0) AS TotalRevenue,
    RANK() OVER (ORDER BY ISNULL(SUM(P.Amount), 0) DESC) AS RevenueRank
FROM Staff S
LEFT JOIN Appointment A ON S.StaffID = A.StaffID
LEFT JOIN Payment P ON A.AppointmentID = P.AppointmentID
GROUP BY S.StaffID, S.FirstName, S.LastName
ORDER BY RevenueRank;
GO

-- 5.  Delete cancelled appointments older than 30 days
DELETE FROM Appointment
WHERE Status = 'Cancelled'
AND Appointmentdate < DATEADD(DAY, -30, GETDATE());
GO

-- TESTING SECTION 

-- ---- Test 1: Loyalty points trigger ----
SELECT LoyaltyPoints FROM Customer WHERE CustomerID = 1;  -- BEFORE value

EXEC BookAppointment
    @CustomerID = 1, @StaffID = 1, @ServiceID = 2,
    @AppointmentDate = '2026-08-01', @AppointmentTime = '10:00:00',
    @FinalPrice = 2500, @PaymentMethod = 'Cash';

SELECT LoyaltyPoints FROM Customer WHERE CustomerID = 1;  
GO

-- ---- Test 2: PaymentLog / AFTER DELETE trigger 

DECLARE @TestAppointmentID INT;

SELECT TOP 1 @TestAppointmentID = A.AppointmentID
FROM Appointment A
LEFT JOIN Payment P ON A.AppointmentID = P.AppointmentID
WHERE P.AppointmentID IS NULL
ORDER BY A.AppointmentID DESC;

INSERT INTO Payment (PaymentID, AppointmentID, Amount, PaymentMethod, PaymentDate)
VALUES ((SELECT ISNULL(MAX(PaymentID),0)+1 FROM Payment), @TestAppointmentID, 500, 'Cash', GETDATE());

DELETE FROM Payment WHERE AppointmentID = @TestAppointmentID;

SELECT * FROM PaymentLog;  -- should show the deleted row logged here
GO

-- ---- Test 3: Index + execution stats 
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT * FROM Customer_Phone WHERE Phone = '03001234567';

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
GO