USE Salon_managment_system;
GO

CREATE PROCEDURE GetAllCustomers
AS
BEGIN
    SELECT * FROM Customer;
END;
GO

EXEC GetAllCustomers;
GO

CREATE PROCEDURE GetDailyRevenue
    @d DATE
AS
BEGIN
    SELECT ISNULL(SUM(Amount), 0) AS TotalRevenue
    FROM Payment
    WHERE PaymentDate = @d;
END;
GO

EXEC GetDailyRevenue @d = '2025-06-01';
GO

CREATE PROCEDURE GetTotalCustomerCount
    @TotalCount INT OUTPUT
AS
BEGIN
    SELECT @TotalCount = COUNT(*) FROM Customer;
END;
GO

DECLARE @count INT;
EXEC GetTotalCustomerCount @TotalCount = @count OUTPUT;
SELECT @count AS TotalCustomers;
GO

CREATE PROCEDURE BookAppointment
    @CustomerID INT,
    @StaffID INT,
    @ServiceID INT,
    @AppointmentDate DATE,
    @AppointmentTime TIME,
    @FinalPrice INT,
    @PaymentMethod VARCHAR(20)
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        DECLARE @NewAppointmentID INT;
        SELECT @NewAppointmentID = ISNULL(MAX(AppointmentID), 0) + 1 FROM Appointment;

        INSERT INTO Appointment 
            (AppointmentID, CustomerID, StaffID, ServiceID, PackageID, Appointmentdate, Appointmenttime, Status, FinalPrice)
        VALUES 
            (@NewAppointmentID, @CustomerID, @StaffID, @ServiceID, NULL, @AppointmentDate, @AppointmentTime, 'Pending', @FinalPrice);

        DECLARE @NewPaymentID INT;
        SELECT @NewPaymentID = ISNULL(MAX(PaymentID), 0) + 1 FROM Payment;

        INSERT INTO Payment (PaymentID, AppointmentID, Amount, PaymentMethod, PaymentDate)
        VALUES (@NewPaymentID, @NewAppointmentID, @FinalPrice, @PaymentMethod, GETDATE());

        COMMIT TRANSACTION;
        SELECT 'Success' AS Result, @NewAppointmentID AS AppointmentID;

    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        SELECT 'Failed' AS Result, ERROR_MESSAGE() AS ErrorDetails;
    END CATCH
END;
GO

EXEC BookAppointment
    @CustomerID = 1,
    @StaffID = 1,
    @ServiceID = 1,
    @AppointmentDate = '2026-07-15',
    @AppointmentTime = '11:00:00',
    @FinalPrice = 1200,
    @PaymentMethod = 'Cash';
GO

SELECT TOP 1 * FROM Appointment ORDER BY AppointmentID DESC;
SELECT TOP 1 * FROM Payment ORDER BY PaymentID DESC;

-- Transaction test
BEGIN TRANSACTION;
INSERT INTO Customer (CustomerID, FirstName, LastName, Email, Gender, RegistrationDate)
VALUES (100, 'Test', 'User', 'testuser@salon.com', 'F', GETDATE());
COMMIT;
SELECT * FROM Customer WHERE CustomerID = 100;

-- Rollback test
BEGIN TRANSACTION;
INSERT INTO Customer (CustomerID, FirstName, LastName, Email, Gender, RegistrationDate)
VALUES (101, 'Rollback', 'Test', 'rollbacktest@salon.com', 'F', GETDATE());
ROLLBACK;
SELECT * FROM Customer WHERE CustomerID = 101;  -- should return ZERO rows