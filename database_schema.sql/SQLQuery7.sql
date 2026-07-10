ALTER PROCEDURE BookAppointment
    @CustomerID INT,
    @StaffID INT,
    @ServiceID INT,
    @AppointmentDate DATE,
    @AppointmentTime TIME,
    @FinalPrice INT,
    @PaymentMethod VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;  -- suppresses "X rows affected" messages that confuse pyodbc

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