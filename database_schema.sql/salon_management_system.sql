create database Salon_managment_system
use Salon_managment_system

--DDL
Create table Customer(
  CustomerID int primary key,-- uniquely identifies each customer
  FirstName varchar(50) NOT NULL,-- first name cannot be empty
  LastName varchar(50) NOT NULL,-- last name cannot be empty
  Email varchar(100) UNIQUE,-- duplicate emails are not allowed
  Gender varchar(1)check (Gender IN ('M','F')),-- only M or F values are allowed
  RegistrationDate date
);
USE Salon_managment_system;

UPDATE Customer SET Email = LOWER(FirstName) + CAST(CustomerID AS VARCHAR) + '@salon.com'
WHERE Email IS NULL;
Create table Customer_Phone(
  CustomerID int,
  Phone varchar(15),
  primary key (CustomerID, Phone),-- one customer can have multiple phone numbers but same number cannot repeat
  foreign key (CustomerID)
  references Customer(CustomerID)-- links phone number with customer table
  ON DELETE CASCADE
  ON UPDATE CASCADE
  -- if customer record changes or deletes,
  -- related phone records also update/delete automatically
);
Create table Staff(
  StaffID int primary key,-- uniquely identifies each staff member
  FirstName varchar(50) NOT NULL,-- first name is required
  LastName varchar(50) NOT NULL,-- last name is required
  Gender varchar(1)check (Gender IN ('M','F')),-- only M or F values are accepted
  StaffType varchar(30)check (StaffType IN ('Senior','Junior','Intern')),-- only valid staff categories are allowed
  Specialization varchar(50)
);
Create table Staff_Phone(
  StaffID int,
  Phone varchar(15),
  primary key (StaffID, Phone),-- prevents duplicate phone numbers for same staff member
  foreign key (StaffID)
  references Staff(StaffID)-- connects phone number with staff table
  ON DELETE CASCADE
  ON UPDATE CASCADE
  -- if staff record changes or deletes,
  -- related phone records also update/delete automatically
);
Create table Service(
  ServiceID int primary key,-- uniquely identifies each service
  Servicename varchar(50) NOT NULL,-- service name cannot be empty
  Baseprice int NOT NULL check (Baseprice > 0),-- service price must be greater than zero
  Duration int NOT NULL check (Duration > 0)-- service duration must be positive
);
Create table Package(
  PackageID int primary key,-- uniquely identifies each package
  Packagename varchar(50) NOT NULL,-- package name is required
  Description varchar(255),
  Packageprice int NOT NULL check (Packageprice > 0)-- package price must be greater than zero
);
Create table Appointment(
  AppointmentID int primary key,-- uniquely identifies each appointment
  CustomerID int NOT NULL,-- appointment must belong to a customer
  StaffID int,
  ServiceID int,
  PackageID int,
  Appointmentdate date NOT NULL,-- appointment date is compulsory
  Appointmenttime time NOT NULL,-- appointment time is compulsory
  Status varchar(20)check (Status IN ('Pending','Confirmed','Completed','Cancelled')),-- only valid appointment status values are allowed
  Staffpreference varchar(50),
  foreign key (CustomerID)
  references Customer(CustomerID)-- links appointment with customer
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
  -- customer cannot be deleted if appointments exist
  foreign key (StaffID)
  references Staff(StaffID)-- links appointment with staff member
  ON DELETE SET NULL
  ON UPDATE SET NULL,
  -- if staff leaves salon,
  -- appointment remains but StaffID becomes NULL
  foreign key (ServiceID)
  references Service(ServiceID)-- links appointment with service
   ON DELETE NO ACTION
  ON UPDATE NO ACTION,
  -- service cannot be deleted if appointment exists
  foreign key (PackageID)
  references Package(PackageID)-- links appointment with package
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
  -- package cannot be deleted if appointment exists
  check (
    ServiceID IS NOT NULL
    OR
    PackageID IS NOT NULL
  )-- appointment must contain either a service or a package
);
Create Table Payment
(
PaymentID int primary key,-- uniquely identifies each payment
AppointmentID int NOT NULL UNIQUE,-- one appointment can have only one payment
foreign key (AppointmentID) 
references Appointment(AppointmentID)-- links payment with appointment
ON DELETE NO ACTION
ON UPDATE NO ACTION,
-- appointment cannot be deleted if payment exists
Amount decimal(10,2) NOT NULL check (Amount > 0),-- payment amount must be greater than zero
PaymentMethod varchar(20) NOT NULL check (PaymentMethod IN ('Cash','Card','Online','JazzCash')),-- only valid payment methods are allowed
PaymentDate date NOT NULL-- payment date is required
);

Create Table Review
(
ReviewID int primary key,-- uniquely identifies each review
CustomerID int NOT NULL,-- review must belong to a customer
foreign key (CustomerID) 
references Customer(CustomerID)-- connects review with customer
ON DELETE NO ACTION
ON UPDATE NO ACTION,
-- customer cannot be deleted if review exists
AppointmentID int NOT NULL UNIQUE,-- one appointment can have only one review
foreign key (AppointmentID) 
references Appointment(AppointmentID)-- connects review with appointment
ON DELETE NO ACTION
ON UPDATE NO ACTION,
-- appointment cannot be deleted if review exists
Rating int check (Rating between 1 AND 5),-- rating value must be between 1 and 5
Comment varchar(255),
ReviewDate date
);
Create Table Package_Service
(
PackageID int,
ServiceID int,
primary key (PackageID, ServiceID),-- prevents duplicate service entries in same package
foreign key (PackageID)
references Package(PackageID)-- links package_service with package table
ON DELETE CASCADE
ON UPDATE CASCADE,
-- if package changes/deletes,
-- related package services also update/delete
foreign key (ServiceID)
references Service(ServiceID)-- links package_service with service table
ON DELETE CASCADE
ON UPDATE CASCADE
-- if service changes/deletes,
-- related package services also update/delete
);

--DML
insert into Customer(CustomerID, FirstName, LastName, Email, Gender, RegistrationDate)
values
(1, 'Hafsa', 'Ahmad', 'hafsa.ahmad@gmail.com', 'F', '2023-03-12'),
(2, 'Saliha', 'Abbasi', 'saliha.abbasi@gmail.com', 'F', '2024-07-18'),
(3, 'Laiba', 'Khan', 'laiba.khan@gmail.com', 'F', '2025-01-09'),
(4, 'Ali', 'Raza', 'ali.raza@gmail.com', 'M', '2022-11-20'),
(5, 'Sara', 'Malik', 'sara.malik@gmail.com', 'F', '2024-05-14'),
(6, 'Ahmed', 'Sheikh', 'ahmed.sheikh@gmail.com', 'M', '2023-09-02'),
(7, 'Zainab', 'Butt', 'zainab.butt@gmail.com', 'F', '2025-02-11'),
(8, 'Hamza', 'Ali', 'hamza.ali@gmail.com', 'M', '2024-12-01');

insert into Customer_Phone(CustomerID, Phone)
values
(1, '03001234567'),
(2, '03111234567'),
(3, '03221234567'),
(4, '03331234567'),
(5, '03441234567'),
(6, '03551234567'),
(7, '03661234567'),
(8, '03771234567');

insert into Staff(StaffID, FirstName, LastName, Gender, StaffType, Specialization)
values
(1, 'Ayesha', 'Khan', 'F', 'Senior', 'Hair Styling'),
(2, 'Bilal', 'Ahmed', 'M', 'Junior', 'Skin Care'),
(3, 'Hina', 'Malik', 'F', 'Intern', 'Facial'),
(4, 'Saad', 'Raza', 'M', 'Senior', 'Hair Coloring'),
(5, 'Iqra', 'Sheikh', 'F', 'Senior', 'Makeup'),
(6, 'Maham', 'Butt', 'F', 'Junior', 'Manicure'),
(7, 'Farhan', 'Ali', 'M', 'Intern', 'Pedicure'),
(8, 'Taha', 'Khan', 'M', 'Senior', 'Skin Treatment');

insert into Staff_Phone(StaffID, Phone)
values
(1, '03009876543'),
(2, '03119876543'),
(3, '03229876543'),
(4, '03339876543'),
(5, '03449876543'),
(6, '03559876543'),
(7, '03669876543'),
(8, '03779876543');

insert into Service(ServiceID, Servicename, Baseprice, Duration)
values
(1, 'Haircut & Styling', 800, 45),
(2, 'Hair Coloring', 2500, 90),
(3, 'Facial Treatment', 1500, 60),
(4, 'Skin Whitening', 2000, 75),
(5, 'Bridal Makeup', 8000, 180),
(6, 'Party Makeup', 3500, 90),
(7, 'Manicure', 1200, 45),
(8, 'Pedicure', 1400, 50);

insert into Package(PackageID, Packagename, Description, Packageprice)
values
(1, 'Bridal Package', 'Bridal makeup, hair styling and skin treatment', 12000),
(2, 'Glow Package', 'Facial, skin whitening and pedicure', 5000),
(3, 'Refresh Package', 'Haircut, facial and manicure', 3000),
(4, 'Premium Package', 'Hair coloring, party makeup and skin whitening', 7000),
(5, 'Relax Package', 'Pedicure, manicure and facial', 4500),
(6, 'Basic Package', 'Haircut and facial', 2000),
(7, 'Skin Package', 'Skin whitening and facial treatment', 3500),
(8, 'Hair Package', 'Hair coloring and haircut styling', 3200);

insert into Appointment(AppointmentID, CustomerID, StaffID, ServiceID, PackageID, Appointmentdate, Appointmenttime, Status, Staffpreference)
values
(1, 1, 1, 1, NULL, '2025-06-01', '10:00:00', 'Confirmed', 'Female'),
(2, 2, 5, 6, NULL, '2025-06-02', '11:00:00', 'Pending', 'Female'),
(3, 3, 6, 7, NULL, '2025-06-03', '14:00:00', 'Confirmed', 'Female'),
(4, 4, 2, 3, NULL, '2025-06-04', '09:30:00', 'Completed', 'Male'),
(5, 5, 1, NULL, 3, '2024-12-05', '12:00:00', 'Confirmed', 'Female'),
(6, 6, 7, NULL, 5, '2023-11-06', '15:00:00', 'Pending', NULL),
(7, 7, 5, NULL, 1, '2025-01-07', '10:30:00', 'Confirmed', NULL),
(8, 8, 8, 4, NULL, '2024-08-08', '13:00:00', 'Cancelled', 'Female');

insert into Payment(PaymentID, AppointmentID, Amount, PaymentMethod, PaymentDate)
values
(1, 1, 800, 'Cash', '2025-06-01'),
(2, 2, 3500, 'Card', '2025-06-02'),
(3, 3, 1200, 'Online', '2025-06-03'),
(4, 4, 1500, 'JazzCash', '2025-06-04'),
(5, 5, 3000, 'Cash', '2024-12-05'),
(6, 6, 4500, 'Card', '2023-11-06'),
(7, 7, 12000, 'Online', '2025-01-07'),
(8, 8, 2000, 'Cash', '2024-08-08');

insert into Review(ReviewID, CustomerID, AppointmentID, Rating, Comment, ReviewDate)
values
(1, 1, 1, 5, 'Excellent haircut service and very cooperative staff', '2025-06-01'),
(2, 2, 2, 4, 'Really liked the party makeup look', '2025-06-02'),
(3, 3, 3, 5, 'Manicure service was neat and professional', '2025-06-03'),
(4, 4, 4, 4, 'Facial treatment gave good results', '2025-06-04'),
(5, 5, 5, 5, 'Refresh package was worth the price', '2024-12-05'),
(6, 6, 6, 3, 'Overall experience was satisfactory', '2023-11-06'),
(7, 7, 7, 5, 'Bridal package services were excellent', '2025-01-07'),
(8, 8, 8, 2, 'Appointment timing was delayed', '2024-08-08');

insert into Package_Service(PackageID, ServiceID)
values
(1, 5),
(1, 1),
(1, 4),
(2, 3),
(2, 4),
(2, 8),
(3, 1),
(3, 7);

--Select statements
-- Display complete customer information
select * 
from Customer;

-- Display all staff members working in salon
select * 
from Staff;

-- Display all salon services
select * 
from Service;

-- Display all available salon packages
select * 
from Package;

-- Display only confirmed appointments
select * 
from Appointment
where Status = 'Confirmed';

-- Display female customers only
select * 
from Customer
where Gender = 'F';

-- Display senior staff members
select * 
from Staff
where StaffType = 'Senior';

-- Display services having price greater than 2000
select * 
from Service
where Baseprice > 2000;

-- Display payments made through cash
select * 
from Payment
where PaymentMethod = 'Cash';

-- Display reviews with 5 star rating
select * 
from Review
where Rating = 5;

-- Display selected customer columns only
select FirstName, LastName, Email
from Customer;

-- Display services from highest price to lowest price
select * 
from Service
order by Baseprice DESC;

--ALTER STATEMENT
-- Add Address column in Customer table
alter table Customer
add Address varchar(100);

--UPDATE STATEMENT
-- Update appointment status
update Appointment
set Status = 'Completed'
where AppointmentID = 2;

--DELETE STATEMENT
-- Delete a review record
delete from Review
where ReviewID = 8;

--aggregate functions
-- Count total customers in salon
select COUNT(*) AS TotalCustomers
from Customer;

-- Count total confirmed appointments
select COUNT(*) AS ConfirmedAppointments
from Appointment
where Status = 'Confirmed';

-- Calculate total revenue generated from payments
select SUM(Amount) AS TotalRevenue
from Payment;

-- Calculate average service price
select AVG(Baseprice) AS AverageServicePrice
from Service;

-- Find highest package price
select MAX(Packageprice) AS HighestPackagePrice
from Package;

-- Find lowest service price
select MIN(Baseprice) AS LowestServicePrice
from Service;

-- Count staff members according to their type
select StaffType, COUNT(*) AS TotalStaff
from Staff
group by StaffType;

-- Calculate average customer rating
select AVG(Rating) AS AverageRating
from Review;

-- Calculate total payment received through each payment method
select PaymentMethod, SUM(Amount) AS TotalAmount
from Payment
group by PaymentMethod;

-- Count total customer reviews
select COUNT(*) AS TotalReviews
from Review;


--DATE AND TIME FUNCTIONS
-- display current date and time
select getdate() AS CurrentDateTime;

-- display today's date only
select cast(getdate() AS date) AS TodayDate;

-- display day number from each appointment date
select AppointmentID, day(Appointmentdate) AS AppointmentDay
from Appointment;

-- display month number from each appointment date
select AppointmentID, month(Appointmentdate) AS AppointmentMonth
from Appointment;

-- display year from each appointment date
select AppointmentID, year(Appointmentdate) AS AppointmentYear
from Appointment;

-- display how many days ago each customer registered
select CustomerID, FirstName, datediff(day, RegistrationDate, getdate()) AS DaysSinceRegistration
from Customer;

-- display follow up date by adding 7 days to each appointment date
select AppointmentID, Appointmentdate, dateadd(day, 7, Appointmentdate) AS FollowUpDate
from Appointment;

-- display appointment date in DD/MM/YYYY format
select AppointmentID, format(Appointmentdate, 'dd/MM/yyyy') AS FormattedDate
from Appointment;

-- display appointments that have already passed
select AppointmentID, Appointmentdate, Status
from Appointment
where Appointmentdate < getdate();

-- display payments made in the current year
select PaymentID, PaymentDate, Amount
from Payment
where year(PaymentDate) = year(getdate());

--string functions
-- combine customer first and last name
select FirstName,LastName,
CONCAT(FirstName,' ',LastName) AS fullname
from Customer;

-- combine staff information with separator
select CONCAT_WS(' - ',FirstName,LastName,Specialization) AS staffdetail
from Staff;

-- convert customer names into uppercase
select FirstName,
UPPER(FirstName) AS uppername
from Customer;

-- convert customer emails into lowercase
select Email,
LOWER(Email) AS loweremail
from Customer;

-- remove left spaces
select LTRIM('   Beauty Salon') AS leftTrim;

-- remove right spaces
select RTRIM('Beauty Salon   ') AS rightTrim;

-- remove spaces from both sides
select TRIM('   Salon Management System   ') AS fullTrim;

-- extract first 5 characters from service name
select ServiceName,
SUBSTRING(ServiceName,1,5) AS shortservice
from Service;

-- extract first 3 letters of package name
select LEFT(PackageName,3) AS packagecode
from Package;

-- extract last 4 digits of customer phone number
select RIGHT(Phone,4) AS lastdigits
from Customer_Phone;

-- count total characters in review comments
select Comment,
LEN(Comment) AS commentlength
from Review;

--joins
-- inner join : Customer with their appointment
SELECT 
    C.Firstname + ' ' + C.Lastname AS Customername,
    A.AppointmentID,
    A.Appointmentdate,
    A.Status
FROM Customer C
INNER JOIN Appointment A 
ON C.CustomerID = A.CustomerID;

-- left join : All services including unbooked ones
SELECT 
    SR.Servicename,
    SR.Baseprice,
    A.AppointmentID
FROM Service SR
LEFT JOIN Appointment A 
ON SR.ServiceID = A.ServiceID;

-- right join : All appointments with staff info
SELECT 
    S.Firstname + ' ' + S.Lastname AS Staffname,
    S.Stafftype,
    A.AppointmentID,
    A.Appointmentdate
FROM Staff S
RIGHT JOIN Appointment A 
ON S.StaffID = A.StaffID;

-- full outer join : All customers and all appointments
SELECT 
    C.Firstname + ' ' + C.Lastname AS Customername,
    A.AppointmentID,
    A.Status
FROM Customer C
FULL OUTER JOIN Appointment A 
ON C.CustomerID = A.CustomerID;

-- self join : staff members of same type
SELECT 
    S1.Firstname + ' ' + S1.Lastname AS Staffmember1,
    S2.Firstname + ' ' + S2.Lastname AS Staffmember2,
    S1.Stafftype
FROM Staff S1
JOIN Staff S2 
ON S1.Stafftype = S2.Stafftype
AND S1.StaffID <> S2.StaffID;

-- cross join — All customer and service combinations
SELECT 
    C.Firstname + ' ' + C.Lastname AS Customername,
    SR.Servicename
FROM Customer C
CROSS JOIN Service SR;

-- multi table join : complete booking details
SELECT 
    C.Firstname + ' ' + C.Lastname AS Customername,
    S.Firstname + ' ' + S.Lastname AS Staffname,
    SR.Servicename,
    P.Amount,
    P.Paymentmethod
FROM Appointment A
JOIN Customer C  ON A.CustomerID    = C.CustomerID
JOIN Staff S     ON A.StaffID       = S.StaffID
JOIN Service SR  ON A.ServiceID     = SR.ServiceID
JOIN Payment P   ON A.AppointmentID = P.AppointmentID;

-- join with GROUP BY : Total Appointments Per Staff
SELECT 
    S.Firstname + ' ' + S.Lastname AS Staffname,
    S.Stafftype,
    COUNT(A.AppointmentID) AS Totalappointments
FROM Staff S
LEFT JOIN Appointment A 
ON S.StaffID = A.StaffID
GROUP BY S.StaffID, S.FirstName, S.LastName, S.StaffType;

-- join with having : staff with more than one appointment
SELECT 
    S.Firstname + ' ' + S.Lastname AS Staffname,
    COUNT(A.AppointmentID) AS Totalappointments
FROM Staff S
JOIN Appointment A 
ON S.StaffID = A.StaffID
GROUP BY S.StaffID, S.Firstname, S.Lastname
HAVING COUNT(A.AppointmentID) > 1;

-- join with aggregate : revenue per service
SELECT 
    SR.Servicename,
    COUNT(P.PaymentID) AS Totalbookings,
    SUM(P.Amount)      AS Totalrevenue,
    AVG(P.Amount)      AS Averagepayment
FROM Service SR
JOIN Appointment A ON SR.ServiceID    = A.ServiceID
JOIN Payment P     ON A.AppointmentID = P.AppointmentID
GROUP BY SR.ServiceID, SR.Servicename;

-- join with order by — top spending customers
SELECT 
    C.Firstname + ' ' + C.Lastname AS Customername,
    SUM(P.Amount)      AS Totalspent,
    COUNT(P.PaymentID) AS Totalpayments
FROM Customer C
JOIN Appointment A ON C.CustomerID    = A.CustomerID
JOIN Payment P     ON A.AppointmentID = P.AppointmentID
GROUP BY C.CustomerID, C.Firstname, C.Lastname
ORDER BY Totalspent DESC;

--scalar value function
-- Function to Calculate Discounted Price
Create Function fn_DiscountPrice
(
    @Price int
)
Returns int
AS
BEGIN
    Return @Price - (@Price * 10 / 100)
END;
select 
PackageID,
Packagename,
Packageprice,
dbo.fn_DiscountPrice(Packageprice) AS DiscountedPrice
from Package;

-- Function to Check Customer Rating
Create Function fn_RatingStatus
(
    @Rating int
)
Returns varchar(20)
AS
BEGIN
    Declare @Status varchar(20)
    IF @Rating >= 5
        SET @Status = 'Excellent'
    ELSE IF @Rating >= 4
        SET @Status = 'Good'
    ELSE IF @Rating >= 3
        SET @Status = 'Average'
    ELSE
        SET @Status = 'Poor'
    Return @Status
END;
select
ReviewID,
Rating,
dbo.fn_RatingStatus(Rating) AS ReviewStatus
from Review;

-- Function to Calculate Service Tax
Create Function fn_ServiceTax
(
    @Amount decimal(10,2)
)
Returns decimal(10,2)
AS
BEGIN
    Return @Amount + (@Amount * 15 / 100)
END;
select
PaymentID,
Amount,
dbo.fn_ServiceTax(Amount) AS TotalWithTax
from Payment;

-- Function to Check Appointment Status
Create Function fn_AppointmentResult
(
    @Status varchar(20)
)
Returns varchar(30)
AS
BEGIN
    Declare @Result varchar(30)
    IF @Status = 'Completed'
        SET @Result = 'Service Finished'
    ELSE IF @Status = 'Confirmed'
        SET @Result = 'Appointment Confirmed'
    ELSE IF @Status = 'Pending'
        SET @Result = 'Waiting'
    ELSE
        SET @Result = 'Appointment Cancelled'
    Return @Result
END;
select
AppointmentID,
Status,
dbo.fn_AppointmentResult(Status) AS AppointmentMessage
from Appointment;

--table valued functions
-- display all customers
create function fun_CustomerInformation()
returns table
as
return
(
    select * from Customer
);
select * 
from dbo.fun_CustomerInformation();

-- Display Appointments of a Customer
Create Function fn_AppointmentsByCustomer
(
    @CustomerID int
)
Returns Table
AS
RETURN
(
    select
    AppointmentID,
    Appointmentdate,
    Appointmenttime,
    Status
    from Appointment
    where CustomerID = @CustomerID
);
select *
from dbo.fn_AppointmentsByCustomer(1);

-- Display Services of a Package
Create Function fn_ServicesByPackage
(
    @PackageID int
)
Returns Table
AS
RETURN
(
    select
    Service.ServiceID,
    Servicename,
    Baseprice
    from Service
    inner join Package_Service
    ON Service.ServiceID = Package_Service.ServiceID
    where Package_Service.PackageID = @PackageID
);
select *
from dbo.fn_ServicesByPackage(1);

-- Display Reviews Given By Customers
Create Function fn_CustomerReviews
(
    @CustomerID int
)
Returns Table
AS
RETURN
(
    select
    ReviewID,
    Rating,
    Comment,
    ReviewDate
    from Review
    where CustomerID = @CustomerID
);
select *
from dbo.fn_CustomerReviews(2);

-- Display Payments Above Given Amount
Create Function fn_HighPayments
(
    @Amount decimal(10,2)
)
Returns Table
AS
RETURN
(
    select
    PaymentID,
    AppointmentID,
    Amount,
    PaymentMethod
    from Payment
    where Amount > @Amount
);
select *
from dbo.fn_HighPayments(3000);

-- subqueries
-- Customer Having Highest Payment
select 
C.FirstName,
C.LastName,
P.Amount
from Customer C
join Appointment A
ON C.CustomerID = A.CustomerID
join Payment P
ON A.AppointmentID = P.AppointmentID
where P.Amount =
(
    select max(Amount)
    from Payment
);

--Customers Paying Above Average Payment
select
C.FirstName,
C.LastName,
P.Amount
from Customer C
join Appointment A
ON C.CustomerID = A.CustomerID
join Payment P
ON A.AppointmentID = P.AppointmentID
where P.Amount >
(
    select avg(Amount)
    from Payment
);

--Services Having Price Greater Than
-- Average Service Price
select
Servicename,
Baseprice
from Service
where Baseprice >
(
    select avg(Baseprice)
    from Service
);

--Package with Highest Price
select
Packagename,
Packageprice
from Package
where Packageprice =
(
    select max(Packageprice)
    from Package
);

--Staff Members Handling Appointments
select
FirstName,
LastName,
Specialization
from Staff
where StaffID IN
(
    select StaffID
    from Appointment
);

--Customers Giving 5-Star Reviews
select
FirstName,
LastName
from Customer
where CustomerID IN
(
    select CustomerID
    from Review
    where Rating = 5
);

--Customers Without Any Review
select
FirstName,
LastName
from Customer
where CustomerID NOT IN
(
    select CustomerID
    from Review
);

--Appointments Having Completed Status
select
AppointmentID,
Appointmentdate,
Status
from Appointment
where AppointmentID IN
(
    select AppointmentID
    from Appointment
    where Status = 'Completed'
);

--Services Included in Packages
select
Servicename
from Service
where ServiceID IN
(
    select ServiceID
    from Package_Service
);

--Customers Who Booked Packages
select
FirstName,
LastName
from Customer
where CustomerID IN
(
    select CustomerID
    from Appointment
    where PackageID IS NOT NULL
);

--Payments Greater Than Average Payment
select
PaymentID,
Amount
from Payment
where Amount >
(
    select avg(Amount)
    from Payment
);

--Staff Having Senior Type
select
FirstName,
LastName,
StaffType
from Staff
where StaffType =
(
    select top 1 StaffType
    from Staff
    where StaffType = 'Senior'
);

--Package Containing Bridal Makeup Service
select
Packagename
from Package
where PackageID IN
(
    select PackageID
    from Package_Service
    where ServiceID =
    (
        select ServiceID
        from Service
        where Servicename = 'Bridal Makeup'
    )
);

--Customers Registered Before Average Date
select
FirstName,
LastName,
RegistrationDate
from Customer
where RegistrationDate <
(
    select avg(cast(RegistrationDate AS bigint))
    from Customer
);

--Highest Rated Reviews
select
ReviewID,
Comment,
Rating
from Review
where Rating =
(
    select max(Rating)
    from Review
);


