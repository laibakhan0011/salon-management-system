USE Salon_managment_system;

-- 1. INNER JOIN: AppointmentID + Customer name + Staff name + Service name
SELECT 
    A.AppointmentID,
    C.FirstName + ' ' + C.LastName AS CustomerName,
    S.FirstName + ' ' + S.LastName AS StaffName,
    SV.Servicename AS ServiceName
FROM Appointment A
INNER JOIN Customer C ON A.CustomerID = C.CustomerID
INNER JOIN Staff S ON A.StaffID = S.StaffID
INNER JOIN Service SV ON A.ServiceID = SV.ServiceID;

-- 2. LEFT JOIN: all customers, even with no appointments
SELECT 
    C.CustomerID,
    C.FirstName + ' ' + C.LastName AS CustomerName,
    A.AppointmentID
FROM Customer C
LEFT JOIN Appointment A ON C.CustomerID = A.CustomerID;

-- 3. Subquery: customers who spent more than average (per payment)
SELECT
    C.FirstName,
    C.LastName,
    P.Amount
FROM Customer C
JOIN Appointment A ON C.CustomerID = A.CustomerID
JOIN Payment P ON A.AppointmentID = P.AppointmentID
WHERE P.Amount > (
    SELECT AVG(Amount) FROM Payment
);

-- 4. GROUP BY: appointments per staff member
SELECT 
    S.FirstName + ' ' + S.LastName AS StaffName,
    COUNT(A.AppointmentID) AS TotalAppointments
FROM Staff S
LEFT JOIN Appointment A ON S.StaffID = A.StaffID
GROUP BY S.StaffID, S.FirstName, S.LastName;

-- 5. HAVING: staff with more than 5 appointments
-- (With only 8 sample appointments total, none will show yet — expected until more data is added)
SELECT 
    S.FirstName + ' ' + S.LastName AS StaffName,
    COUNT(A.AppointmentID) AS TotalAppointments
FROM Staff S
JOIN Appointment A ON S.StaffID = A.StaffID
GROUP BY S.StaffID, S.FirstName, S.LastName
HAVING COUNT(A.AppointmentID) > 5;
GO

-- 6. View: AppointmentDetails
CREATE VIEW AppointmentDetails AS
SELECT 
    A.AppointmentID,
    A.Appointmentdate,
    A.Appointmenttime,
    A.Status,
    A.FinalPrice,
    C.FirstName + ' ' + C.LastName AS CustomerName,
    S.FirstName + ' ' + S.LastName AS StaffName,
    SV.Servicename AS ServiceName
FROM Appointment A
LEFT JOIN Customer C ON A.CustomerID = C.CustomerID
LEFT JOIN Staff S ON A.StaffID = S.StaffID
LEFT JOIN Service SV ON A.ServiceID = SV.ServiceID;
GO

-- 7. View: DailyRevenue
CREATE VIEW DailyRevenue AS
SELECT
    PaymentDate,
    SUM(Amount) AS TotalRevenue,
    COUNT(*) AS TotalPayments
FROM Payment
GROUP BY PaymentDate;
GO

-- 8. View: StaffPerformance
CREATE VIEW StaffPerformance AS
SELECT 
    S.StaffID,
    S.FirstName + ' ' + S.LastName AS StaffName,
    S.StaffType,
    COUNT(A.AppointmentID) AS TotalAppointments,
    ISNULL(SUM(P.Amount), 0) AS TotalRevenue
FROM Staff S
LEFT JOIN Appointment A ON S.StaffID = A.StaffID
LEFT JOIN Payment P ON A.AppointmentID = P.AppointmentID
GROUP BY S.StaffID, S.FirstName, S.LastName, S.StaffType;
GO

-- 9. Test all three views
SELECT * FROM AppointmentDetails;
SELECT * FROM DailyRevenue;
SELECT * FROM StaffPerformance;
    
