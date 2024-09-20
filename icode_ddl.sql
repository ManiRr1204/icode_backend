-- create database icode;
-- use icode;

-- CREATE TABLE `Company` (
--   `CID` char(36),
--   `CName` varchar(36),
--   `CLogo` blob,
--   `CAddress` varchar(255),
--   `UserName` varchar(255),
--   `Password` varchar(255),
--   PRIMARY KEY (`CID`, `UserName`)
-- );
-- ALTER TABLE Company
-- ADD ReportType VARCHAR(255) AFTER CAddress;

-- CREATE TABLE `Customer` (
--   `CustomerID` char(36) PRIMARY KEY,
--   `CID` char(36),
--   `FName` varchar(255),
--   `LName` varchar(255),
--   `Address` varchar(255),
--   `PhoneNumber` varchar(255),
--   `Email` varchar(255),
--   `IsActive` boolean
-- );

-- ALTER TABLE `Customer` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

-- CREATE TABLE `Employee` (
--   `EmpID` char(36) PRIMARY KEY,
--   `CID` char(36),
--   `FName` varchar(255),
--   `LName` varchar(255),
--   `IsActive` boolean,
--   `PhoneNumber` varchar(255),
--   `Pin` int
-- );

-- ALTER TABLE `Employee` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);


-- CREATE TABLE `DeviceSetting` (
--   `DeviceID` char(36),
--   `CID` char(36),
--   `DeviceName` varchar(255),
--   `RegID` varchar(255),
--   `IsActive` boolean,
--   PRIMARY KEY (`DeviceID`, `CID`)
-- );

-- ALTER TABLE `DeviceSetting` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);


-- CREATE TABLE `ContactUS` (
--     `RequestID` CHAR(36) PRIMARY KEY,
--     `CID` CHAR(36),
--     `Name` CHAR(36),
--     `RequestorEmail` VARCHAR(255) NOT NULL,
--     `ConcernsQuestions` TEXT,
--     `PhoneNumber` VARCHAR(20),
--     `Status` VARCHAR(50)
-- );

-- ALTER TABLE `ContactUS` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

-- CREATE TABLE `ReportRecipients` (
--   `CheckinID` char(36) PRIMARY KEY,
--   `CID` char(36),
--   `EmailId` varchar(255),
--   `Exec` boolean
-- );

-- ALTER TABLE `ReportRecipients` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

-- CREATE TABLE `CheckInType` (
--   `TypeID` char(36) PRIMARY KEY,
--   `CID` char(36),
--   `TypeNames` varchar(255)
-- );

-- ALTER TABLE `CheckInType` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

-- CREATE TABLE `ReportType` (
--   `ReportTypeID` char(36) PRIMARY KEY,
--   `ReportTypeName` varchar(255)
-- );

-- CREATE TABLE `CompanyReportType` (
--   `CompanyReporterEmail` char(255),
--   `CID` char(36),
--   `IsDailyReportActive` boolean DEFAULT FALSE,
--   `IsWeeklyReportActive` boolean DEFAULT FALSE,
--   `IsBiWeeklyReportActive` boolean DEFAULT FALSE,
--   `IsMonthlyReportActive` boolean DEFAULT FALSE,
--   `IsBiMonthlyReportActive` boolean DEFAULT FALSE,
--   PRIMARY KEY (`CompanyReporterEmail`, `CID`)
-- );

-- ALTER TABLE `CompanyReportType` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

-- CREATE TABLE `ReportSchedule` (
--   `ReportID` char(36),
--   `CID` char(36),
--   `ReportTypeID` char(36),
--   `IsDelivered` boolean,
--   `IsActive` boolean,
--   `ReportTimeGenerated` datetime,
--   `ReportTimeSent` datetime,
--   `TextReportTime` varchar(255),
--   `CreatedAt` datetime,
--   `UpdatedAt` datetime,
--   PRIMARY KEY (`ReportID`, `CID`)
-- );

-- ALTER TABLE `ReportSchedule` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);
-- ALTER TABLE `ReportSchedule` ADD FOREIGN KEY (`ReportTypeID`) REFERENCES `ReportType` (`ReportTypeID`);

-- CREATE TABLE `TransactionStatus` (
--   `TransactionID` char(36),
--   `CID` char(36),
--   `UserName` varchar(255),
--   `CreditCardEncrypted` varchar(255),
--   `ExpiryDate` date,
--   `CVV` int ,
--   `TransactionAmount` decimal(10,2),
--   `TransactionStartTime` datetime,
--   `TransactionEndTime` datetime,
--   `TransactionStatus` varchar(255),
--   `BillingAddress` varchar(255),
--   PRIMARY KEY (`TransactionID`,`CID`,`UserName`)
-- );

-- ALTER TABLE `TransactionStatus` ADD FOREIGN KEY (`CID`, `UserName`) REFERENCES `Company` (`CID`,`UserName`);

-- CREATE TABLE `DailyReportTable` (
--   `EmpID` char(36),
--   `CID` char(36),
--   `TypeID` char(36),
--   `CheckInSnap` blob,
--   `CheckInTime` datetime,
--   `CheckOutSnap` blob,
--   `CheckOutTime` datetime,
--   `TimeWorked` decimal(10,2),
--   `Date` date,
--   PRIMARY KEY (`CheckInTime`,`EmpID`,`CID`)
-- );

-- ALTER TABLE `DailyReportTable` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);
-- ALTER TABLE `DailyReportTable` ADD FOREIGN KEY (`EmpID`) REFERENCES `Employee` (`EmpID`);


-- -- Stored Procedures-- 
-- -- Store Procedures for Company Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateCompany(
--   IN p_cid CHAR(36),
--   IN p_cname VARCHAR(36),
--   IN p_clogo BLOB,
--   IN p_caddress VARCHAR(255),
--   IN p_username VARCHAR(255),
--   IN p_password VARCHAR(255),
--   IN p_reportType VARCHAR(255)
-- )
-- BEGIN
--     INSERT INTO Company (CID, CName, CLogo, CAddress, UserName, Password, ReportType)
--   VALUES (p_cid, p_cname, p_clogo, p_caddress, p_username, p_password, p_reportType);
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetAllCompanies ()
-- BEGIN
--   SELECT * FROM Company;
-- END//

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetCompany (
-- IN p_cid CHAR(36)
-- )
-- BEGIN
--   SELECT * FROM Company WHERE CID = p_cid;
-- END//

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetUser (
-- IN p_username CHAR(36)
-- )
-- BEGIN
--   SELECT * FROM Company WHERE UserName = p_username;
-- END//

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spUpdateCompany (
--   IN p_cid CHAR(36),
--   IN p_cname VARCHAR(36),
--   IN p_clogo BLOB,
--   IN p_caddress VARCHAR(255),
--   IN p_username VARCHAR(255),
--   IN p_password VARCHAR(255),
--   IN p_reportType VARCHAR(255)
-- )
-- BEGIN
--   UPDATE Company
--   SET CName = p_cname,
--       CLogo = p_clogo,
--       CAddress = p_caddress,
--       UserName = p_username,
--       Password = p_password,
--       ReportType = p_reportType
--   WHERE CID = p_cid;
-- END//

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spUpdateCompanyReport(
--     IN p_company_id CHAR(36),
--     IN p_report_type VARCHAR(255)
-- )
-- BEGIN
--     UPDATE Company
--     SET ReportType = p_report_type
--     WHERE CID = p_company_id;
-- END//

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spDeleteCompany (
--   IN p_cid CHAR(36)
-- )
-- BEGIN
--   DELETE FROM Company WHERE CID = p_cid;
-- END//

-- DELIMITER ;

-- -- Store Procedures for Customer Table-- 
-- DELIMITER //

-- CREATE PROCEDURE spCreateCustomer(
--     IN p_CustomerID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_FName VARCHAR(255),
--     IN p_LName VARCHAR(255),
--     IN p_Address VARCHAR(255),
--     IN p_PhoneNumber VARCHAR(255),
--     IN p_Email VARCHAR(255),
--     IN p_IsActive BOOLEAN
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO Customer (CustomerID, CID, FName, LName, Address, PhoneNumber, Email, IsActive)
--     VALUES (p_CustomerID, p_CID, p_FName, p_LName, p_Address, p_PhoneNumber, p_Email, p_IsActive);

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetCustomerUsingCID (
-- IN p_cid CHAR(36)
-- )
-- BEGIN
--   SELECT * FROM Customer WHERE CID = p_cid;
-- END//

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetCustomer(
--     IN p_CustomerID CHAR(36)
-- )
-- BEGIN
--     SELECT *
--     FROM Customer
--     WHERE CustomerID = p_CustomerID;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spUpdateCustomer(
--     IN p_CustomerID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_FName VARCHAR(255),
--     IN p_LName VARCHAR(255),
--     IN p_Address VARCHAR(255),
--     IN p_PhoneNumber VARCHAR(255),
--     IN p_Email VARCHAR(255),
--     IN p_IsActive BOOLEAN
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE Customer
--     SET CID = p_CID,
--         FName = p_FName,
--         LName = p_LName,
--         Address = p_Address,
--         PhoneNumber = p_PhoneNumber,
--         Email = p_Email,
--         IsActive = p_IsActive
--     WHERE CustomerID = p_CustomerID;

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spDeleteCustomer(
--     IN p_CustomerID CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM Customer WHERE CustomerID = p_CustomerID;

--     COMMIT;
-- END //

-- DELIMITER ;


-- -- Store Procedures for Employee Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateEmployee(
--     IN p_EmpID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_FName VARCHAR(255),
--     IN p_LName VARCHAR(255),
--     IN p_IsActive BOOLEAN,
--     IN p_PhoneNo VARCHAR(255),
--     IN p_Pin INT
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO Employee (EmpID, CID, FName, LName, IsActive, PhoneNumber, Pin)
--     VALUES (p_EmpID, p_CID, p_FName, p_LName, p_IsActive, p_PhoneNo, p_Pin);

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetAllEmployee (
-- 	IN p_CID CHAR(36)
-- )
-- BEGIN
--   SELECT * FROM Employee WHERE CID = p_CID;
-- END//

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetEmployee(
--     IN p_EmpID CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM Employee WHERE EmpID = p_EmpID;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spUpdateEmployee(
--     IN p_EmpID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_FName VARCHAR(255),
--     IN p_LName VARCHAR(255),
--     IN p_IsActive BOOLEAN,
--     IN p_PhoneNo VARCHAR(255),
--     IN p_Pin INT
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE Employee
--     SET CID = p_CID,
--         FName = p_FName,
--         LName = p_LName,
--         IsActive = p_IsActive,
--         PhoneNumber = p_PhoneNo,
--         Pin = p_Pin
--     WHERE EmpID = p_EmpID;

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spDeleteEmployee(
--     IN p_EmpID CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM Employee WHERE EmpID = p_EmpID;

--     COMMIT;
-- END //

-- DELIMITER ;


-- -- Store Procedures for DeviceSetting Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateDeviceSetting(
--     IN p_DeviceID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_DeviceName VARCHAR(255),
--     IN p_RegID VARCHAR(255),
--     IN p_IsActive BOOLEAN
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO DeviceSetting (DeviceID, CID, DeviceName, RegID, IsActive)
--     VALUES (p_DeviceID, p_CID, p_DeviceName, p_RegID, p_IsActive);

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spGetDeviceSetting(
--     IN p_DeviceID CHAR(36),
--     IN p_CID CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM DeviceSetting WHERE DeviceID = p_DeviceID AND CID = p_CID;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spUpdateDeviceSetting(
--     IN p_DeviceID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_DeviceName VARCHAR(255),
--     IN p_RegID VARCHAR(255),
--     IN p_IsActive BOOLEAN
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE DeviceSetting
--     SET DeviceName = p_DeviceName,
--         RegID = p_RegID,
--         IsActive = p_IsActive
--     WHERE DeviceID = p_DeviceID AND CID = p_CID;

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spDeleteDeviceSetting(
--     IN p_DeviceID CHAR(36),
--     IN p_CID CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM DeviceSetting WHERE DeviceID = p_DeviceID AND CID = p_CID;

--     COMMIT;
-- END //


-- DELIMITER ;

-- -- Store Procedures for ContactUS Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateContact(
--     IN p_requestId CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_Name CHAR(36),
--     IN p_requestorEmail VARCHAR(255),
--     IN p_concerns_questions TEXT,
--     IN p_phoneNumber VARCHAR(20),
--     IN p_status VARCHAR(50)
-- )
-- BEGIN
--     INSERT INTO ContactUS (
--         RequestID, 
--         CID, 
--         Name,
--         RequestorEmail, 
--         ConcernsQuestions, 
--         PhoneNumber, 
--         Status
--     ) VALUES (
--         p_requestId, 
--         p_CID, 
--         p_Name,
--         p_requestorEmail, 
--         p_concerns_questions, 
--         p_phoneNumber, 
--         p_status
--     );
-- END //

-- DELIMITER :

-- DELIMITER //

-- CREATE PROCEDURE spGetContact(
--     IN p_requestId CHAR(36)
-- )
-- BEGIN
--     SELECT 
--         *
--     FROM 
--         ContactUS
--     WHERE 
--         RequestID = p_requestId;
-- END //

-- DELIMITER :

-- DELIMITER //

-- CREATE PROCEDURE spDeleteContact(
--     IN p_requestId CHAR(36)
-- )
-- BEGIN
--     DELETE FROM ContactUS
--     WHERE RequestID = p_requestId;
-- END //

-- DELIMITER :

-- DELIMITER //

-- CREATE PROCEDURE spUpdateContact(
--     IN p_requestId CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_Name CHAR(36),
--     IN p_requestorEmail VARCHAR(255),
--     IN p_concerns_questions TEXT,
--     IN p_phoneNumber VARCHAR(20),
--     IN p_status VARCHAR(50)
-- )
-- BEGIN
--     UPDATE ContactUS
--     SET 
--         CID = p_CID,
--         Name = p_Name,
--         RequestorEmail = p_requestorEmail, 
--         ConcernsQuestions = p_concerns_questions, 
--         PhoneNumber = p_phoneNumber, 
--         Status = p_status
--     WHERE 
--         RequestID = p_requestId;
-- END //

-- DELIMITER :

-- -- Store Procedures for ReportRecipient Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateReportRecipient(
--     IN p_CheckinID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_EmailID VARCHAR(255),
--     IN p_Exec boolean
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO ReportRecipients (CheckinID, CID, EmailId, Exec)
--     VALUES (p_CheckinID, p_CID, p_EmailID, p_Exec);

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetReportRecipient(
--     IN p_CheckinID CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM ReportRecipients WHERE CheckinID = p_CheckinID;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spUpdateReportRecipient(
--     IN p_CheckinID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_EmailID VARCHAR(255),
--     IN p_Exec VARCHAR(255)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE ReportRecipients
--     SET CID = p_CID,
--         EmailId = p_EmailID,
--         Exec = p_Exec
--     WHERE CheckinID = p_CheckinID;

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spDeleteReportRecipient(
--     IN p_CheckinID CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM ReportRecipients WHERE CheckinID = p_CheckinID;

--     COMMIT;
-- END //

-- DELIMITER ;

-- -- Store Procedures for CheckinType Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateCheckInType(
--     IN p_TypeID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_TypeNames VARCHAR(255)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO CheckInType (TypeID, CID, TypeNames)
--     VALUES (p_TypeID, p_CID, p_TypeNames);

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetCheckInType(
--     IN p_TypeID CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM CheckInType WHERE TypeID = p_TypeID;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spUpdateCheckInType(
--     IN p_TypeID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_TypeNames VARCHAR(255)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE CheckInType
--     SET CID = p_CID,
--         TypeNames = p_TypeNames
--     WHERE TypeID = p_TypeID;

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spDeleteCheckInType(
--     IN p_TypeID CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM CheckInType WHERE TypeID = p_TypeID;

--     COMMIT;
-- END //

-- DELIMITER ;

-- -- Store Procedures for Report-type Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateReportType(
--     IN p_ReportTypeID CHAR(36),
--     IN p_ReportTypeName VARCHAR(255)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO ReportType (ReportTypeID, ReportTypeName)
--     VALUES (p_ReportTypeID, p_ReportTypeName);

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetReportType(
--     IN p_ReportTypeID CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM ReportType WHERE ReportTypeID = p_ReportTypeID;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spUpdateReportType(
--     IN p_ReportTypeID CHAR(36),
--     IN p_ReportTypeName VARCHAR(255)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE ReportType
--     SET ReportTypeName = p_ReportTypeName
--     WHERE ReportTypeID = p_ReportTypeID;

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spDeleteReportType(
--     IN p_ReportTypeID CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM ReportType WHERE ReportTypeID = p_ReportTypeID;

--     COMMIT;
-- END //

-- DELIMITER ;


-- -- Store Procedures for Company Report-type Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateCompanyReportType(
--     IN p_CompanyReporterEmail CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_IsDailyReportActive BOOLEAN,
--     IN p_IsWeeklyReportActive BOOLEAN,
--     IN p_IsBiWeeklyReportActive BOOLEAN,
--     IN p_IsMonthlyReportActive BOOLEAN,
--     IN p_IsBiMonthlyReportActive BOOLEAN
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO CompanyReportType(CompanyReporterEmail, CID, IsDailyReportActive,
--         IsWeeklyReportActive,
--         IsBiWeeklyReportActive,
--         IsMonthlyReportActive,
--         IsBiMonthlyReportActive)
--     VALUES (p_CompanyReporterEmail, p_CID, p_IsDailyReportActive,
--         p_IsWeeklyReportActive,
--         p_IsBiWeeklyReportActive,
--         p_IsMonthlyReportActive,
--         p_IsBiMonthlyReportActive);

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spGetCompanyReportType(
--     IN p_CompanyReporterEmail CHAR(36),
--     IN p_CID CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM CompanyReportType WHERE CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spGetAllCompanyReportType(
--     IN p_CID CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM CompanyReportType WHERE CID = p_CID;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spUpdateCompanyReportType(
--     IN p_CompanyReporterEmail CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_IsDailyReportActive BOOLEAN,
--     IN p_IsWeeklyReportActive BOOLEAN,
--     IN p_IsBiWeeklyReportActive BOOLEAN,
--     IN p_IsMonthlyReportActive BOOLEAN,
--     IN p_IsBiMonthlyReportActive BOOLEAN
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE CompanyReportType
--     SET IsDailyReportActive = p_IsDailyReportActive,
--         IsWeeklyReportActive = p_IsWeeklyReportActive,
--         IsBiWeeklyReportActive = p_IsBiWeeklyReportActive,
--         IsMonthlyReportActive = p_IsMonthlyReportActive,
--         IsBiMonthlyReportActive = p_IsBiMonthlyReportActive
--     WHERE CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID;

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spDeleteCompanyReportType(
--     IN p_CompanyReporterEmail CHAR(36),
--     IN p_CID CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM CompanyReportType WHERE CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID;

--     COMMIT;
-- END //

-- DELIMITER ;

-- -- Store Procedures for Report Schedule Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateReportSchedule(
--     IN p_ReportID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_ReportTypeID CHAR(36),
--     IN p_IsDelivered BOOLEAN,
--     IN p_IsActive BOOLEAN,
--     IN p_ReportTimeGenerated DATETIME,
--     IN p_ReportTimeSent DATETIME,
--     IN p_TextReportTime VARCHAR(255),
--     IN p_CreatedAt DATETIME,
--     IN p_UpdatedAt DATETIME
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO ReportSchedule (ReportID, CID, ReportTypeID, IsDelivered, IsActive, ReportTimeGenerated, ReportTimeSent, TextReportTime, CreatedAt, UpdatedAt)
--     VALUES (p_ReportID, p_CID, p_ReportTypeID, p_IsDelivered, p_IsActive, p_ReportTimeGenerated, p_ReportTimeSent, p_TextReportTime, p_CreatedAt, p_UpdatedAt);

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spGetReportSchedule(
--     IN p_ReportID CHAR(36),
--     IN p_CID CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM ReportSchedule WHERE ReportID = p_ReportID AND CID = p_CID;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spUpdateReportSchedule(
--     IN p_ReportID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_ReportTypeID CHAR(36),
--     IN p_IsDelivered BOOLEAN,
--     IN p_IsActive BOOLEAN,
--     IN p_ReportTimeGenerated DATETIME,
--     IN p_ReportTimeSent DATETIME,
--     IN p_TextReportTime VARCHAR(255),
--     IN p_CreatedAt DATETIME,
--     IN p_UpdatedAt DATETIME
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE ReportSchedule
--     SET ReportTypeID = p_ReportTypeID,
--         IsDelivered = p_IsDelivered,
--         IsActive = p_IsActive,
--         ReportTimeGenerated = p_ReportTimeGenerated,
--         ReportTimeSent = p_ReportTimeSent,
--         TextReportTime = p_TextReportTime,
--         CreatedAt = p_CreatedAt,
--         UpdatedAt = p_UpdatedAt
--     WHERE ReportID = p_ReportID AND CID = p_CID;

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spDeleteReportSchedule(
--     IN p_ReportID CHAR(36),
--     IN p_CID CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM ReportSchedule WHERE ReportID = p_ReportID AND CID = p_CID;

--     COMMIT;
-- END //

-- DELIMITER ;


-- -- Store Procedures for Transaction status Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateTransactionStatus(
--     IN p_transactionid CHAR(36),
--     IN p_cid CHAR(36),
--     IN p_username VARCHAR(255),
--     IN p_creditcardencrypted VARCHAR(255),
--     IN p_expirydate DATE,
--     IN p_cvv INT,
--     IN p_transactionamount DECIMAL(10, 2),
--     IN p_transactionstarttime DATETIME,
--     IN p_transactionendtime DATETIME,
--     IN p_transactionstatus VARCHAR(255),
--     IN p_billingaddress VARCHAR(255)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO TransactionStatus (TransactionID, CID, UserName, CreditCardEncrypted, ExpiryDate, CVV, TransactionAmount, TransactionStartTime, TransactionEndTime, TransactionStatus, BillingAddress)
--     VALUES (p_transactionid, p_cid, p_username, p_creditcardencrypted, p_expirydate, p_cvv, p_transactionamount, p_transactionstarttime, p_transactionendtime, p_transactionstatus, p_billingaddress);

--     COMMIT;
-- END //

-- DELIMITER :

-- DELIMITER //

-- CREATE PROCEDURE spGetTransactionStatus(
--     IN p_transactionid CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM TransactionStatus WHERE TransactionID = p_transactionid;
-- END //

-- DELIMITER :

-- DELIMITER //

-- CREATE PROCEDURE spDeleteTransactionStatus(
--     IN p_transactionid CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM TransactionStatus WHERE TransactionID = p_transactionid;

--     COMMIT;
-- END //

-- DELIMITER :


-- DELIMITER //

-- CREATE PROCEDURE spUpdateTransactionStatus(
--     IN p_transactionid CHAR(36),
--     IN p_cid CHAR(36),
--     IN p_username VARCHAR(255),
--     IN p_creditcardencrypted VARCHAR(255),
--     IN p_expirydate DATE,
--     IN p_cvv INT,
--     IN p_transactionamount DECIMAL(10,2),
--     IN p_transactionstarttime DATETIME,
--     IN p_transactionendtime DATETIME,
--     IN p_transactionstatus VARCHAR(255),
--     IN p_billingaddress VARCHAR(255)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE TransactionStatus
--     SET CID = p_cid,
--         UserName = p_username,
--         CreditCardEncrypted = p_creditcardencrypted,
--         ExpiryDate = p_expirydate,
--         CVV = p_cvv,
--         TransactionAmount = p_transactionamount,
--         TransactionStartTime = p_transactionstarttime,
--         TransactionEndTime = p_transactionendtime,
--         TransactionStatus = p_TransactionStatus,
--         BillingAddress = p_billingaddress
--     WHERE TransactionID = p_transactionid;

--     COMMIT;
-- END //

-- DELIMITER :

-- -- Store Procedures for Daily Report Table-- 

-- DELIMITER //

-- CREATE PROCEDURE spCreateDailyReport(
--     IN p_EmpID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_TypeID CHAR(36),
--     IN p_CheckInSnap BLOB,
--     IN p_CheckInTime DATETIME,
--     IN p_CheckOutSnap BLOB,
--     IN p_CheckOutTime DATETIME,
--     IN p_TimeWorked DECIMAL(10, 2),
--     IN p_Date DATE
-- )
-- BEGIN
--     INSERT INTO DailyReportTable (
--         EmpID, 
--         CID, 
--         TypeID, 
--         CheckInSnap, 
--         CheckInTime, 
--         CheckOutSnap, 
--         CheckOutTime, 
--         TimeWorked,
--         Date
--     ) VALUES (
--         p_EmpID, 
--         p_CID, 
--         p_TypeID, 
--         p_CheckInSnap, 
--         p_CheckInTime, 
--         p_CheckOutSnap, 
--         p_CheckOutTime, 
--         p_TimeWorked,
--         p_Date
--     );
-- END //

-- DELIMITER :


-- DELIMITER //

-- CREATE PROCEDURE spDeleteDailyReport(
--     IN p_EmpID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_CheckInTime DATETIME
-- )
-- BEGIN
--     DELETE FROM DailyReportTable
--     WHERE EmpID = p_EmpID AND CID = p_CID AND CheckInTime = p_CheckInTime;
-- END //

-- DELIMITER :


-- DELIMITER //

-- CREATE PROCEDURE spGetDailyReport(
--     IN p_EmpID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_CheckInTime DATETIME
-- )
-- BEGIN
--     SELECT 
--         EmpID, 
--         CID, 
--         TypeID, 
--         CheckInSnap, 
--         CheckInTime, 
--         CheckOutSnap, 
--         CheckOutTime, 
--         TimeWorked,
--         Date
--     FROM 
--         DailyReportTable
--     WHERE 
--         EmpID = p_EmpID AND
--         CID = p_CID AND
--         CheckInTime = p_CheckInTime;
-- END //

-- DELIMITER :


-- DELIMITER //

-- CREATE PROCEDURE spUpdateDailyReport(
--     IN p_EmpID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_Date DATE,
--     IN p_TypeID CHAR(36),
--     IN p_CheckInSnap BLOB,
--     IN p_CheckInTime DATETIME,
--     IN p_CheckOutSnap BLOB,
--     IN p_CheckOutTime DATETIME,
--     IN p_TimeWorked DECIMAL(10, 2)
-- )
-- BEGIN
--     UPDATE DailyReportTable
--     SET 
--         TypeID = p_TypeID,
--         Date = p_Date,
--         CheckInSnap = p_CheckInSnap,
--         CheckOutSnap = p_CheckOutSnap,
--         CheckOutTime = p_CheckOutTime,
--         TimeWorked = p_TimeWorked
--     WHERE 
--         EmpID = p_EmpID AND
--         CID = p_CID AND
--         CheckInTime = p_CheckInTime;
-- END //

-- DELIMITER :



-- DELIMITER //

-- CREATE PROCEDURE spGetEmployeeDailyReport(IN reportDate DATE)
-- BEGIN
--     SELECT 
--         CONCAT(Employee.FName, " ", Employee.LName) AS "Name", 
--         Employee.PIN AS "Pin", 
--         DailyReportTable.TypeID AS "Type", 
--         DailyReportTable.CheckInTime  AS "CheckInTime", 
--         DailyReportTable.CheckOutTime  AS "CheckOutTime",  
--         DailyReportTable.CheckInSnap  AS "CheckInSnap", 
--         DailyReportTable.CheckOutSnap  AS "CheckOutSnap",  
--         DailyReportTable.TimeWorked  AS "TimeWorked",
--         Employee.EmpID AS "EmpID",
--         Employee.CID AS "CID"
--     FROM 
--         Employee
--     JOIN 
--         DailyReportTable 
--     ON 
--         Employee.EmpID = DailyReportTable.EmpID 
--     AND 
--         Employee.CID = DailyReportTable.CID 
--     WHERE 
--         DailyReportTable.Date = reportDate;
-- END //

-- DELIMITER ;




DELIMITER //

CREATE PROCEDURE spGetCompanyDailyReportFromDateRange(IN cid char(36), IN startDate DATE, IN endDate Date)
BEGIN
    SELECT 
        CONCAT(Employee.FName, " ", Employee.LName) AS "Name", 
        Employee.PIN AS "Pin", 
        DailyReportTable.TypeID AS "Type", 
        DailyReportTable.CheckInTime  AS "CheckInTime", 
        DailyReportTable.CheckOutTime  AS "CheckOutTime",  
        DailyReportTable.TimeWorked  AS "TimeWorked"
    FROM 
        Employee
    JOIN 
        DailyReportTable 
    ON 
        Employee.EmpID = DailyReportTable.EmpID 
    AND 
        Employee.CID = DailyReportTable.CID 
    WHERE 
    
    Date >= startDate AND Date < endDate + INTERVAL 1 DAY AND CID = cid;
END //

DELIMITER ;









-- SET SQL_SAFE_UPDATES = 0; 

-- CREATE TABLE `Device` (
-- 	`DeviceID` char(36),
--     `CID` char(36),
--     `DeviceName` char(36),
--     `AccessKey` char(36),
-- 	`AccessKeyGeneratedTime` datetime,
--     PRIMARY KEY (`CID`, `AccessKey`)
--     );
    

-- ALTER TABLE `Device` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);


-- DELIMITER //

-- CREATE PROCEDURE spGetAllDevices(
-- IN p_cid CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM Device WHERE CID = p_cid;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE spDeleteDevice(
--     IN p_accessKey CHAR(36),
--     IN p_cid CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     DELETE FROM Device WHERE AccessKey = p_accessKey AND CID = p_cid;

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spCreateDevice(
--     IN p_deviceID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_deviceName VARCHAR(255),
--     IN p_accessKey VARCHAR(255),
--     IN p_accessKeyCreatedDateTime DATETIME 
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO Device (DeviceID, CID, DeviceName, AccessKey, AccessKeyGeneratedTime)
--     VALUES (p_deviceID, p_CID, p_deviceName, p_accessKey, p_accessKeyCreatedDateTime);

--     COMMIT;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- CREATE PROCEDURE spUpdateDevice(
--     IN p_deviceID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_deviceName VARCHAR(255),
--     IN p_accessKey VARCHAR(255),
--     IN p_accessKeyCreatedDateTime DATETIME 
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE Device
--     SET 
--         DeviceID = p_deviceID,
--         DeviceName = p_deviceName,
--         AccessKeyGeneratedTime = p_accessKeyCreatedDateTime
--     WHERE 
--         AccessKey = p_accessKey AND
--         CID = p_CID;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE `spGetEmployeeDailyBasisReport`(
-- IN p_eid CHAR(36),
-- IN reportDate DATE)
-- BEGIN
--     SELECT  * FROM  DailyReportTable 

--     WHERE EmpID = p_eid AND Date = reportDate;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE `spGetAllDevicesWithoutBasedOnCID`()
-- BEGIN
--     SELECT * FROM Device ;
-- END //

-- DELIMITER ;

















-- CREATE TABLE `Device` (
--   `TimeZone` char(36) DEFAULT NULL,
--   `DeviceID` char(36) DEFAULT NULL,
--   `CID` char(36) NOT NULL,
--   `DeviceName` char(36) DEFAULT NULL,
--   `AccessKey` char(36) NOT NULL,
--   `AccessKeyGeneratedTime` datetime DEFAULT NULL,
--   `IsActive` boolean,
--   PRIMARY KEY (`CID`,`AccessKey`),
--   CONSTRAINT `Device` FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`)
-- )

-- DELIMITER //

-- CREATE PROCEDURE `spCreateDevice`(
-- 	IN p_timezone CHAR(36),
--     IN p_deviceID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_deviceName VARCHAR(255),
--     IN p_accessKey VARCHAR(255),
--     IN p_accessKeyCreatedDateTime DATETIME,
--     IN p_IsActive BOOLEAN
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     INSERT INTO Device (TimeZone, DeviceID, CID, DeviceName, AccessKey, AccessKeyGeneratedTime, IsActive)
--     VALUES (p_timezone, p_deviceID, p_CID, p_deviceName, p_accessKey, p_accessKeyCreatedDateTime, p_IsActive);

--     COMMIT;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE `spGetAllDevices`(
-- IN p_cid CHAR(36)
-- )
-- BEGIN
--     SELECT * FROM Device WHERE CID = p_cid AND IsActive = true;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE `spDeleteDevice`(
--     IN p_accessKey CHAR(36),
--     IN p_cid CHAR(36)
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE Device
--     SET IsActive = false
--     WHERE 
--         AccessKey = p_accessKey AND
--         CID = p_CID;
-- END //

-- DELIMITER ;

-- DELIMITER //

-- CREATE PROCEDURE `spUpdateDevice`(
-- 	IN p_timezone CHAR(36),
--     IN p_deviceID CHAR(36),
--     IN p_CID CHAR(36),
--     IN p_deviceName VARCHAR(255),
--     IN p_accessKey VARCHAR(255),
--     IN p_accessKeyCreatedDateTime DATETIME,
--     IN p_IsActive BOOLEAN
-- )
-- BEGIN
--     DECLARE EXIT HANDLER FOR SQLEXCEPTION
--     BEGIN
--         ROLLBACK;
--     END;

--     START TRANSACTION;

--     UPDATE Device
--     SET 
-- 		TimeZone = p_timezone,
--         DeviceID = p_deviceID,
--         DeviceName = p_deviceName,
--         AccessKeyGeneratedTime = p_accessKeyCreatedDateTime,
--         IsActive = p_IsActive
--     WHERE 
--         AccessKey = p_accessKey AND
--         CID = p_CID;
-- END //

-- DELIMITER ;





create database icode;
use icode;

CREATE TABLE `Company` (
  `CID` char(36),
  `CName` varchar(36),
  `CLogo` blob,
  `CAddress` varchar(255),
  `UserName` varchar(255),
  `Password` varchar(255),
  PRIMARY KEY (`CID`, `UserName`)
);
ALTER TABLE Company
ADD ReportType VARCHAR(255) AFTER CAddress;

CREATE TABLE `Customer` (
  `CustomerID` char(36) PRIMARY KEY,
  `CID` char(36),
  `FName` varchar(255),
  `LName` varchar(255),
  `Address` varchar(255),
  `PhoneNumber` varchar(255),
  `Email` varchar(255),
  `IsActive` boolean
);

ALTER TABLE `Customer` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

CREATE TABLE `Employee` (
  `EmpID` char(36) PRIMARY KEY,
  `CID` char(36),
  `FName` varchar(255),
  `LName` varchar(255),
  `IsActive` boolean,
  `PhoneNumber` varchar(255),
  `Pin` int
);

ALTER TABLE `Employee` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);


CREATE TABLE `DeviceSetting` (
  `DeviceID` char(36),
  `CID` char(36),
  `DeviceName` varchar(255),
  `RegID` varchar(255),
  `IsActive` boolean,
  PRIMARY KEY (`DeviceID`, `CID`)
);

ALTER TABLE `DeviceSetting` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);


CREATE TABLE `ContactUS` (
    `RequestID` CHAR(36) PRIMARY KEY,
    `CID` CHAR(36),
    `Name` CHAR(36),
    `RequestorEmail` VARCHAR(255) NOT NULL,
    `ConcernsQuestions` TEXT,
    `PhoneNumber` VARCHAR(20),
    `Status` VARCHAR(50)
);

ALTER TABLE `ContactUS` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

CREATE TABLE `Device` (
  `TimeZone` char(36) DEFAULT NULL,
  `DeviceID` char(36) DEFAULT NULL,
  `CID` char(36) NOT NULL,
  `DeviceName` char(36) DEFAULT NULL,
  `AccessKey` char(36) NOT NULL,
  `AccessKeyGeneratedTime` datetime DEFAULT NULL,
  `IsActive` boolean,
  PRIMARY KEY (`CID`,`AccessKey`),
  CONSTRAINT `Device` FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`)
)

CREATE TABLE `ReportRecipients` (
  `CheckinID` char(36) PRIMARY KEY,
  `CID` char(36),
  `EmailId` varchar(255),
  `Exec` boolean
);

ALTER TABLE `ReportRecipients` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

CREATE TABLE `CheckInType` (
  `TypeID` char(36) PRIMARY KEY,
  `CID` char(36),
  `TypeNames` varchar(255)
);

ALTER TABLE `CheckInType` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

CREATE TABLE `ReportType` (
  `ReportTypeID` char(36) PRIMARY KEY,
  `ReportTypeName` varchar(255)
);

CREATE TABLE `CompanyReportType` (
  `CompanyReporterEmail` char(255),
  `CID` char(36),
  `IsDailyReportActive` boolean DEFAULT FALSE,
  `IsWeeklyReportActive` boolean DEFAULT FALSE,
  `IsBiWeeklyReportActive` boolean DEFAULT FALSE,
  `IsMonthlyReportActive` boolean DEFAULT FALSE,
  `IsBiMonthlyReportActive` boolean DEFAULT FALSE,
  PRIMARY KEY (`CompanyReporterEmail`, `CID`)
);

ALTER TABLE `CompanyReportType` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);

CREATE TABLE `ReportSchedule` (
  `ReportID` char(36),
  `CID` char(36),
  `ReportTypeID` char(36),
  `IsDelivered` boolean,
  `IsActive` boolean,
  `ReportTimeGenerated` datetime,
  `ReportTimeSent` datetime,
  `TextReportTime` varchar(255),
  `CreatedAt` datetime,
  `UpdatedAt` datetime,
  PRIMARY KEY (`ReportID`, `CID`)
);

ALTER TABLE `ReportSchedule` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);
ALTER TABLE `ReportSchedule` ADD FOREIGN KEY (`ReportTypeID`) REFERENCES `ReportType` (`ReportTypeID`);

CREATE TABLE `TransactionStatus` (
  `TransactionID` char(36),
  `CID` char(36),
  `UserName` varchar(255),
  `CreditCardEncrypted` varchar(255),
  `ExpiryDate` date,
  `CVV` int ,
  `TransactionAmount` decimal(10,2),
  `TransactionStartTime` datetime,
  `TransactionEndTime` datetime,
  `TransactionStatus` varchar(255),
  `BillingAddress` varchar(255),
  PRIMARY KEY (`TransactionID`,`CID`,`UserName`)
);

ALTER TABLE `TransactionStatus` ADD FOREIGN KEY (`CID`, `UserName`) REFERENCES `Company` (`CID`,`UserName`);

CREATE TABLE `DailyReportTable` (
  `EmpID` char(36),
  `CID` char(36),
  `TypeID` char(36),
  `CheckInSnap` blob,
  `CheckInTime` datetime,
  `CheckOutSnap` blob,
  `CheckOutTime` datetime,
  `TimeWorked` decimal(10,2),
  `Date` date,
  PRIMARY KEY (`CheckInTime`,`EmpID`,`CID`)
);

ALTER TABLE DailyReportTable
MODIFY COLUMN TimeWorked VARCHAR(255);

ALTER TABLE `DailyReportTable` ADD FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`);
ALTER TABLE `DailyReportTable` ADD FOREIGN KEY (`EmpID`) REFERENCES `Employee` (`EmpID`);


-- Stored Procedures-- 
-- Store Procedures for Company Table-- 

DELIMITER //

CREATE PROCEDURE spCreateCompany(
  IN p_cid CHAR(36),
  IN p_cname VARCHAR(36),
  IN p_clogo BLOB,
  IN p_caddress VARCHAR(255),
  IN p_username VARCHAR(255),
  IN p_password VARCHAR(255),
  IN p_reportType VARCHAR(255)
)
BEGIN
    INSERT INTO Company (CID, CName, CLogo, CAddress, UserName, Password, ReportType)
  VALUES (p_cid, p_cname, p_clogo, p_caddress, p_username, p_password, p_reportType);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spUpdateAdminReportType(
  IN p_cid CHAR(36),
  IN p_reportType VARCHAR(255)
)
BEGIN
  UPDATE Company
  SET ReportType = p_reportType
  WHERE CID = p_cid;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetAllCompanies ()
BEGIN
  SELECT * FROM Company;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetCompany (
IN p_cid CHAR(36)
)
BEGIN
  SELECT * FROM Company WHERE CID = p_cid;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetUser (
IN p_username CHAR(36)
)
BEGIN
  SELECT * FROM Company WHERE UserName = p_username;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spUpdateCompany (
  IN p_cid CHAR(36),
  IN p_cname VARCHAR(36),
  IN p_clogo BLOB,
  IN p_caddress VARCHAR(255),
  IN p_username VARCHAR(255),
  IN p_password VARCHAR(255),
  IN p_reportType VARCHAR(255)
)
BEGIN
  UPDATE Company
  SET CName = p_cname,
      CLogo = p_clogo,
      CAddress = p_caddress,
      UserName = p_username,
      Password = p_password,
      ReportType = p_reportType
  WHERE CID = p_cid;
END//

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spUpdateCompanyReport(
    IN p_company_id CHAR(36),
    IN p_report_type VARCHAR(255)
)
BEGIN
    UPDATE Company
    SET ReportType = p_report_type
    WHERE CID = p_company_id;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spDeleteCompany (
  IN p_cid CHAR(36)
)
BEGIN
  DELETE FROM Company WHERE CID = p_cid;
END//

DELIMITER ;

-- Store Procedures for Customer Table-- 
DELIMITER //

CREATE PROCEDURE spCreateCustomer(
    IN p_CustomerID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_Address VARCHAR(255),
    IN p_PhoneNumber VARCHAR(255),
    IN p_Email VARCHAR(255),
    IN p_IsActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO Customer (CustomerID, CID, FName, LName, Address, PhoneNumber, Email, IsActive)
    VALUES (p_CustomerID, p_CID, p_FName, p_LName, p_Address, p_PhoneNumber, p_Email, p_IsActive);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetCustomerUsingCID (
IN p_cid CHAR(36)
)
BEGIN
  SELECT * FROM Customer WHERE CID = p_cid;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetCustomer(
    IN p_CustomerID CHAR(36)
)
BEGIN
    SELECT *
    FROM Customer
    WHERE CustomerID = p_CustomerID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spUpdateCustomer(
    IN p_CustomerID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_Address VARCHAR(255),
    IN p_PhoneNumber VARCHAR(255),
    IN p_Email VARCHAR(255),
    IN p_IsActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Customer
    SET CID = p_CID,
        FName = p_FName,
        LName = p_LName,
        Address = p_Address,
        PhoneNumber = p_PhoneNumber,
        Email = p_Email,
        IsActive = p_IsActive
    WHERE CustomerID = p_CustomerID;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spDeleteCustomer(
    IN p_CustomerID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM Customer WHERE CustomerID = p_CustomerID;

    COMMIT;
END //

DELIMITER ;


-- Store Procedures for Employee Table-- 

DELIMITER //

CREATE PROCEDURE spCreateEmployee(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_IsActive BOOLEAN,
    IN p_PhoneNo VARCHAR(255),
    IN p_Pin INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO Employee (EmpID, CID, FName, LName, IsActive, PhoneNumber, Pin)
    VALUES (p_EmpID, p_CID, p_FName, p_LName, p_IsActive, p_PhoneNo, p_Pin);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetAllEmployee (
	IN p_CID CHAR(36)
)
BEGIN
  SELECT * FROM Employee WHERE CID = p_CID AND IsActive = true;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetEmployee(
    IN p_EmpID CHAR(36)
)
BEGIN
    SELECT * FROM Employee WHERE EmpID = p_EmpID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spGetEmployeeCount`(
	IN p_CID CHAR(36)
)
BEGIN
  SELECT COUNT(EmpID) AS employee_count FROM Employee WHERE CID = p_CID AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spUpdateEmployee(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_IsActive BOOLEAN,
    IN p_PhoneNo VARCHAR(255),
    IN p_Pin INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Employee
    SET CID = p_CID,
        FName = p_FName,
        LName = p_LName,
        IsActive = p_IsActive,
        PhoneNumber = p_PhoneNo,
        Pin = p_Pin
    WHERE EmpID = p_EmpID;

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spDeleteEmployee(
    IN p_EmpID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Employee
    SET 
        IsActive = false
    WHERE EmpID = p_EmpID;

    COMMIT;
END //

DELIMITER ;


-- Store Procedures for DeviceSetting Table-- 

DELIMITER //

CREATE PROCEDURE spCreateDeviceSetting(
    IN p_DeviceID CHAR(36),
    IN p_CID CHAR(36),
    IN p_DeviceName VARCHAR(255),
    IN p_RegID VARCHAR(255),
    IN p_IsActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO DeviceSetting (DeviceID, CID, DeviceName, RegID, IsActive)
    VALUES (p_DeviceID, p_CID, p_DeviceName, p_RegID, p_IsActive);

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spGetDeviceSetting(
    IN p_DeviceID CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    SELECT * FROM DeviceSetting WHERE DeviceID = p_DeviceID AND CID = p_CID;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spUpdateDeviceSetting(
    IN p_DeviceID CHAR(36),
    IN p_CID CHAR(36),
    IN p_DeviceName VARCHAR(255),
    IN p_RegID VARCHAR(255),
    IN p_IsActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE DeviceSetting
    SET DeviceName = p_DeviceName,
        RegID = p_RegID,
        IsActive = p_IsActive
    WHERE DeviceID = p_DeviceID AND CID = p_CID;

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spDeleteDeviceSetting(
    IN p_DeviceID CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM DeviceSetting WHERE DeviceID = p_DeviceID AND CID = p_CID;

    COMMIT;
END //


DELIMITER ;

-- Store Procedures for ContactUS Table-- 

DELIMITER //

CREATE PROCEDURE spCreateContact(
    IN p_requestId CHAR(36),
    IN p_CID CHAR(36),
    IN p_Name CHAR(36),
    IN p_requestorEmail VARCHAR(255),
    IN p_concerns_questions TEXT,
    IN p_phoneNumber VARCHAR(20),
    IN p_status VARCHAR(50)
)
BEGIN
    INSERT INTO ContactUS (
        RequestID, 
        CID, 
        Name,
        RequestorEmail, 
        ConcernsQuestions, 
        PhoneNumber, 
        Status
    ) VALUES (
        p_requestId, 
        p_CID, 
        p_Name,
        p_requestorEmail, 
        p_concerns_questions, 
        p_phoneNumber, 
        p_status
    );
END //

DELIMITER :

DELIMITER //

CREATE PROCEDURE spGetContact(
    IN p_requestId CHAR(36)
)
BEGIN
    SELECT 
        *
    FROM 
        ContactUS
    WHERE 
        RequestID = p_requestId;
END //

DELIMITER :

DELIMITER //

CREATE PROCEDURE spDeleteContact(
    IN p_requestId CHAR(36)
)
BEGIN
    DELETE FROM ContactUS
    WHERE RequestID = p_requestId;
END //

DELIMITER :

DELIMITER //

CREATE PROCEDURE spUpdateContact(
    IN p_requestId CHAR(36),
    IN p_CID CHAR(36),
    IN p_Name CHAR(36),
    IN p_requestorEmail VARCHAR(255),
    IN p_concerns_questions TEXT,
    IN p_phoneNumber VARCHAR(20),
    IN p_status VARCHAR(50)
)
BEGIN
    UPDATE ContactUS
    SET 
        CID = p_CID,
        Name = p_Name,
        RequestorEmail = p_requestorEmail, 
        ConcernsQuestions = p_concerns_questions, 
        PhoneNumber = p_phoneNumber, 
        Status = p_status
    WHERE 
        RequestID = p_requestId;
END //

DELIMITER :

-- Store Procedures for ReportRecipient Table-- 

DELIMITER //

CREATE PROCEDURE spCreateReportRecipient(
    IN p_CheckinID CHAR(36),
    IN p_CID CHAR(36),
    IN p_EmailID VARCHAR(255),
    IN p_Exec boolean
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO ReportRecipients (CheckinID, CID, EmailId, Exec)
    VALUES (p_CheckinID, p_CID, p_EmailID, p_Exec);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetReportRecipient(
    IN p_CheckinID CHAR(36)
)
BEGIN
    SELECT * FROM ReportRecipients WHERE CheckinID = p_CheckinID;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spUpdateReportRecipient(
    IN p_CheckinID CHAR(36),
    IN p_CID CHAR(36),
    IN p_EmailID VARCHAR(255),
    IN p_Exec VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE ReportRecipients
    SET CID = p_CID,
        EmailId = p_EmailID,
        Exec = p_Exec
    WHERE CheckinID = p_CheckinID;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spDeleteReportRecipient(
    IN p_CheckinID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM ReportRecipients WHERE CheckinID = p_CheckinID;

    COMMIT;
END //

DELIMITER ;

-- Store Procedures for CheckinType Table-- 

DELIMITER //

CREATE PROCEDURE spCreateCheckInType(
    IN p_TypeID CHAR(36),
    IN p_CID CHAR(36),
    IN p_TypeNames VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO CheckInType (TypeID, CID, TypeNames)
    VALUES (p_TypeID, p_CID, p_TypeNames);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetCheckInType(
    IN p_TypeID CHAR(36)
)
BEGIN
    SELECT * FROM CheckInType WHERE TypeID = p_TypeID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spUpdateCheckInType(
    IN p_TypeID CHAR(36),
    IN p_CID CHAR(36),
    IN p_TypeNames VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE CheckInType
    SET CID = p_CID,
        TypeNames = p_TypeNames
    WHERE TypeID = p_TypeID;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spDeleteCheckInType(
    IN p_TypeID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM CheckInType WHERE TypeID = p_TypeID;

    COMMIT;
END //

DELIMITER ;

-- Store Procedures for Report-type Table-- 

DELIMITER //

CREATE PROCEDURE spCreateReportType(
    IN p_ReportTypeID CHAR(36),
    IN p_ReportTypeName VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO ReportType (ReportTypeID, ReportTypeName)
    VALUES (p_ReportTypeID, p_ReportTypeName);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetReportType(
    IN p_ReportTypeID CHAR(36)
)
BEGIN
    SELECT * FROM ReportType WHERE ReportTypeID = p_ReportTypeID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spUpdateReportType(
    IN p_ReportTypeID CHAR(36),
    IN p_ReportTypeName VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE ReportType
    SET ReportTypeName = p_ReportTypeName
    WHERE ReportTypeID = p_ReportTypeID;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spDeleteReportType(
    IN p_ReportTypeID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM ReportType WHERE ReportTypeID = p_ReportTypeID;

    COMMIT;
END //

DELIMITER ;


-- Store Procedures for Company Report-type Table-- 

DELIMITER //

CREATE PROCEDURE spCreateCompanyReportType(
    IN p_CompanyReporterEmail CHAR(36),
    IN p_CID CHAR(36),
    IN p_IsDailyReportActive BOOLEAN,
    IN p_IsWeeklyReportActive BOOLEAN,
    IN p_IsBiWeeklyReportActive BOOLEAN,
    IN p_IsMonthlyReportActive BOOLEAN,
    IN p_IsBiMonthlyReportActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO CompanyReportType(CompanyReporterEmail, CID, IsDailyReportActive,
        IsWeeklyReportActive,
        IsBiWeeklyReportActive,
        IsMonthlyReportActive,
        IsBiMonthlyReportActive)
    VALUES (p_CompanyReporterEmail, p_CID, p_IsDailyReportActive,
        p_IsWeeklyReportActive,
        p_IsBiWeeklyReportActive,
        p_IsMonthlyReportActive,
        p_IsBiMonthlyReportActive);

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spGetCompanyReportType(
    IN p_CompanyReporterEmail CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    SELECT * FROM CompanyReportType WHERE CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE spGetAllCompanyReportType(
    IN p_CID CHAR(36)
)
BEGIN
    SELECT * FROM CompanyReportType WHERE CID = p_CID;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spUpdateCompanyReportType(
    IN p_CompanyReporterEmail CHAR(36),
    IN p_CID CHAR(36),
    IN p_IsDailyReportActive BOOLEAN,
    IN p_IsWeeklyReportActive BOOLEAN,
    IN p_IsBiWeeklyReportActive BOOLEAN,
    IN p_IsMonthlyReportActive BOOLEAN,
    IN p_IsBiMonthlyReportActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE CompanyReportType
    SET IsDailyReportActive = p_IsDailyReportActive,
        IsWeeklyReportActive = p_IsWeeklyReportActive,
        IsBiWeeklyReportActive = p_IsBiWeeklyReportActive,
        IsMonthlyReportActive = p_IsMonthlyReportActive,
        IsBiMonthlyReportActive = p_IsBiMonthlyReportActive
    WHERE CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID;

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spDeleteCompanyReportType(
    IN p_CompanyReporterEmail CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM CompanyReportType WHERE CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID;

    COMMIT;
END //

DELIMITER ;

-- Store Procedures for Report Schedule Table-- 

DELIMITER //

CREATE PROCEDURE spCreateReportSchedule(
    IN p_ReportID CHAR(36),
    IN p_CID CHAR(36),
    IN p_ReportTypeID CHAR(36),
    IN p_IsDelivered BOOLEAN,
    IN p_IsActive BOOLEAN,
    IN p_ReportTimeGenerated DATETIME,
    IN p_ReportTimeSent DATETIME,
    IN p_TextReportTime VARCHAR(255),
    IN p_CreatedAt DATETIME,
    IN p_UpdatedAt DATETIME
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO ReportSchedule (ReportID, CID, ReportTypeID, IsDelivered, IsActive, ReportTimeGenerated, ReportTimeSent, TextReportTime, CreatedAt, UpdatedAt)
    VALUES (p_ReportID, p_CID, p_ReportTypeID, p_IsDelivered, p_IsActive, p_ReportTimeGenerated, p_ReportTimeSent, p_TextReportTime, p_CreatedAt, p_UpdatedAt);

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spGetReportSchedule(
    IN p_ReportID CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    SELECT * FROM ReportSchedule WHERE ReportID = p_ReportID AND CID = p_CID;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spUpdateReportSchedule(
    IN p_ReportID CHAR(36),
    IN p_CID CHAR(36),
    IN p_ReportTypeID CHAR(36),
    IN p_IsDelivered BOOLEAN,
    IN p_IsActive BOOLEAN,
    IN p_ReportTimeGenerated DATETIME,
    IN p_ReportTimeSent DATETIME,
    IN p_TextReportTime VARCHAR(255),
    IN p_CreatedAt DATETIME,
    IN p_UpdatedAt DATETIME
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE ReportSchedule
    SET ReportTypeID = p_ReportTypeID,
        IsDelivered = p_IsDelivered,
        IsActive = p_IsActive,
        ReportTimeGenerated = p_ReportTimeGenerated,
        ReportTimeSent = p_ReportTimeSent,
        TextReportTime = p_TextReportTime,
        CreatedAt = p_CreatedAt,
        UpdatedAt = p_UpdatedAt
    WHERE ReportID = p_ReportID AND CID = p_CID;

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE spDeleteReportSchedule(
    IN p_ReportID CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM ReportSchedule WHERE ReportID = p_ReportID AND CID = p_CID;

    COMMIT;
END //

DELIMITER ;


-- Store Procedures for Transaction status Table-- 

DELIMITER //

CREATE PROCEDURE spCreateTransactionStatus(
    IN p_transactionid CHAR(36),
    IN p_cid CHAR(36),
    IN p_username VARCHAR(255),
    IN p_creditcardencrypted VARCHAR(255),
    IN p_expirydate DATE,
    IN p_cvv INT,
    IN p_transactionamount DECIMAL(10, 2),
    IN p_transactionstarttime DATETIME,
    IN p_transactionendtime DATETIME,
    IN p_transactionstatus VARCHAR(255),
    IN p_billingaddress VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO TransactionStatus (TransactionID, CID, UserName, CreditCardEncrypted, ExpiryDate, CVV, TransactionAmount, TransactionStartTime, TransactionEndTime, TransactionStatus, BillingAddress)
    VALUES (p_transactionid, p_cid, p_username, p_creditcardencrypted, p_expirydate, p_cvv, p_transactionamount, p_transactionstarttime, p_transactionendtime, p_transactionstatus, p_billingaddress);

    COMMIT;
END //

DELIMITER :

DELIMITER //

CREATE PROCEDURE spGetTransactionStatus(
    IN p_transactionid CHAR(36)
)
BEGIN
    SELECT * FROM TransactionStatus WHERE TransactionID = p_transactionid;
END //

DELIMITER :

DELIMITER //

CREATE PROCEDURE spDeleteTransactionStatus(
    IN p_transactionid CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM TransactionStatus WHERE TransactionID = p_transactionid;

    COMMIT;
END //

DELIMITER :


DELIMITER //

CREATE PROCEDURE spUpdateTransactionStatus(
    IN p_transactionid CHAR(36),
    IN p_cid CHAR(36),
    IN p_username VARCHAR(255),
    IN p_creditcardencrypted VARCHAR(255),
    IN p_expirydate DATE,
    IN p_cvv INT,
    IN p_transactionamount DECIMAL(10,2),
    IN p_transactionstarttime DATETIME,
    IN p_transactionendtime DATETIME,
    IN p_transactionstatus VARCHAR(255),
    IN p_billingaddress VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE TransactionStatus
    SET CID = p_cid,
        UserName = p_username,
        CreditCardEncrypted = p_creditcardencrypted,
        ExpiryDate = p_expirydate,
        CVV = p_cvv,
        TransactionAmount = p_transactionamount,
        TransactionStartTime = p_transactionstarttime,
        TransactionEndTime = p_transactionendtime,
        TransactionStatus = p_TransactionStatus,
        BillingAddress = p_billingaddress
    WHERE TransactionID = p_transactionid;

    COMMIT;
END //

DELIMITER :

-- Store Procedures for Daily Report Table-- 

DELIMITER //

CREATE PROCEDURE spCreateDailyReport(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_TypeID CHAR(36),
    IN p_CheckInSnap BLOB,
    IN p_CheckInTime DATETIME,
    IN p_CheckOutSnap BLOB,
    IN p_CheckOutTime DATETIME,
    IN p_TimeWorked VARCHAR(255),
    IN p_Date DATE
)
BEGIN
    INSERT INTO DailyReportTable (
        EmpID, 
        CID, 
        TypeID, 
        CheckInSnap, 
        CheckInTime, 
        CheckOutSnap, 
        CheckOutTime, 
        TimeWorked,
        Date
    ) VALUES (
        p_EmpID, 
        p_CID, 
        p_TypeID, 
        p_CheckInSnap, 
        p_CheckInTime, 
        p_CheckOutSnap, 
        p_CheckOutTime, 
        p_TimeWorked,
        p_Date
    );
END //

DELIMITER :


DELIMITER //

CREATE PROCEDURE spDeleteDailyReport(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_CheckInTime DATETIME
)
BEGIN
    DELETE FROM DailyReportTable
    WHERE EmpID = p_EmpID AND CID = p_CID AND CheckInTime = p_CheckInTime;
END //

DELIMITER :


DELIMITER //

CREATE PROCEDURE spGetDailyReport(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_CheckInTime DATETIME
)
BEGIN
    SELECT 
        EmpID, 
        CID, 
        TypeID, 
        CheckInSnap, 
        CheckInTime, 
        CheckOutSnap, 
        CheckOutTime, 
        TimeWorked,
        Date
    FROM 
        DailyReportTable
    WHERE 
        EmpID = p_EmpID AND
        CID = p_CID AND
        CheckInTime = p_CheckInTime;
END //

DELIMITER :


DELIMITER //

CREATE PROCEDURE spUpdateDailyReport(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_Date DATE,
    IN p_TypeID CHAR(36),
    IN p_CheckInSnap BLOB,
    IN p_CheckInTime DATETIME,
    IN p_CheckOutSnap BLOB,
    IN p_CheckOutTime DATETIME,
    IN p_TimeWorked VARCHAR(255)
)
BEGIN
    UPDATE DailyReportTable
    SET 
        TypeID = p_TypeID,
        Date = p_Date,
        CheckInSnap = p_CheckInSnap,
        CheckOutSnap = p_CheckOutSnap,
        CheckOutTime = p_CheckOutTime,
        TimeWorked = p_TimeWorked
    WHERE 
        EmpID = p_EmpID AND
        CID = p_CID AND
        CheckInTime = p_CheckInTime;
END //

DELIMITER :



DELIMITER //

CREATE PROCEDURE spGetEmployeeDailyReport(IN reportDate DATE)
BEGIN
    SELECT 
        CONCAT(Employee.FName, " ", Employee.LName) AS "Name", 
        Employee.PIN AS "Pin", 
        DailyReportTable.TypeID AS "Type", 
        DailyReportTable.CheckInTime  AS "CheckInTime", 
        DailyReportTable.CheckOutTime  AS "CheckOutTime",  
        DailyReportTable.CheckInSnap  AS "CheckInSnap", 
        DailyReportTable.CheckOutSnap  AS "CheckOutSnap",  
        DailyReportTable.TimeWorked  AS "TimeWorked",
        Employee.EmpID AS "EmpID",
        Employee.CID AS "CID"
    FROM 
        Employee
    JOIN 
        DailyReportTable 
    ON 
        Employee.EmpID = DailyReportTable.EmpID 
    AND 
        Employee.CID = DailyReportTable.CID 
    WHERE 
        DailyReportTable.Date = reportDate;
END //

DELIMITER ;




DELIMITER //

CREATE PROCEDURE spGetCompanyDailyReportFromRange(IN cid char(36), IN startDate DATE, IN endDate Date)
BEGIN
    SELECT 
        CONCAT(Employee.FName, " ", Employee.LName) AS "Name", 
        Employee.PIN AS "Pin", 
        DailyReportTable.TypeID AS "Type", 
        DailyReportTable.CheckInTime  AS "CheckInTime", 
        DailyReportTable.CheckOutTime  AS "CheckOutTime",  
        DailyReportTable.TimeWorked  AS "TimeWorked"
    FROM 
        Employee
    JOIN 
        DailyReportTable 
    ON 
        Employee.EmpID = DailyReportTable.EmpID 
    AND 
        Employee.CID = DailyReportTable.CID 
    WHERE 
    
    Date >= startDate AND Date < endDate + INTERVAL 1 DAY AND CID = cid;
END //

DELIMITER ;









SET SQL_SAFE_UPDATES = 0; 

CREATE TABLE `Device` (
  `TimeZone` char(36) DEFAULT NULL,
  `DeviceID` char(36) DEFAULT NULL,
  `CID` char(36) NOT NULL,
  `DeviceName` char(36) DEFAULT NULL,
  `AccessKey` char(36) NOT NULL,
  `AccessKeyGeneratedTime` datetime DEFAULT NULL,
  `IsActive` boolean,
  PRIMARY KEY (`CID`,`AccessKey`),
  CONSTRAINT `Device` FOREIGN KEY (`CID`) REFERENCES `Company` (`CID`)
)

DELIMITER //

CREATE PROCEDURE `spCreateDevice`(
	IN p_timezone CHAR(36),
    IN p_deviceID CHAR(36),
    IN p_CID CHAR(36),
    IN p_deviceName VARCHAR(255),
    IN p_accessKey VARCHAR(255),
    IN p_accessKeyCreatedDateTime DATETIME,
    IN p_IsActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO Device (TimeZone, DeviceID, CID, DeviceName, AccessKey, AccessKeyGeneratedTime, IsActive)
    VALUES (p_timezone, p_deviceID, p_CID, p_deviceName, p_accessKey, p_accessKeyCreatedDateTime, p_IsActive);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spGetAllDevices`(
IN p_cid CHAR(36)
)
BEGIN
    SELECT * FROM Device WHERE CID = p_cid AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spDeleteDevice`(
    IN p_accessKey CHAR(36),
    IN p_cid CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Device
    SET IsActive = false
    WHERE 
        AccessKey = p_accessKey AND
        CID = p_CID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spUpdateDevice`(
	IN p_timezone CHAR(36),
    IN p_deviceID CHAR(36),
    IN p_CID CHAR(36),
    IN p_deviceName VARCHAR(255),
    IN p_accessKey VARCHAR(255),
    IN p_accessKeyCreatedDateTime DATETIME,
    IN p_IsActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Device
    SET 
		TimeZone = p_timezone,
        DeviceID = p_deviceID,
        DeviceName = p_deviceName,
        AccessKeyGeneratedTime = p_accessKeyCreatedDateTime,
        IsActive = p_IsActive
    WHERE 
        AccessKey = p_accessKey AND
        CID = p_CID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spGetEmployeeDailyBasisReport`(
IN p_eid CHAR(36),
IN reportDate DATE)
BEGIN
    SELECT  * FROM  DailyReportTable 

    WHERE EmpID = p_eid AND Date = reportDate;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spGetAllDevicesWithoutBasedOnCID`()
BEGIN
    SELECT * FROM Device ;
END //

DELIMITER ;

DELIMITER // 

CREATE PROCEDURE `spGetCompanyDailyReportFromRange`(IN cid char(36), IN startDate DATE, IN endDate Date)
BEGIN
    SELECT 
        CONCAT(Employee.FName, " ", Employee.LName) AS "Name", 
        Employee.PIN AS "Pin", 
        DailyReportTable.TypeID AS "Type", 
        DailyReportTable.CheckInTime  AS "CheckInTime", 
        DailyReportTable.CheckOutTime  AS "CheckOutTime",  
        DailyReportTable.TimeWorked  AS "TimeWorked"
    FROM 
		DailyReportTable
    JOIN
        Employee
 
    ON 
        Employee.EmpID = DailyReportTable.EmpID 
    AND 
        Employee.CID = DailyReportTable.CID 
    WHERE 
    
    Date >= startDate AND Date < endDate + INTERVAL 1 DAY AND DailyReportTable.CID = cid;
END //

DELIMITER ;



DELIMITER //
CREATE PROCEDURE `spGetAllDevicesWithoutBasedOnCID`()
BEGIN
    SELECT * FROM Device WHERE IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spGetCompanyBasedDailyReport`(IN p_cid CHAR(36),  IN startDateTime DATETIME, endDateTime DATETIME)
BEGIN
    SELECT 
        CONCAT(Employee.FName, " ", Employee.LName) AS "Name", 
        Employee.PIN AS "Pin", 
        DailyReportTable.TypeID AS "Type", 
        DailyReportTable.CheckInTime  AS "CheckInTime", 
        DailyReportTable.CheckOutTime  AS "CheckOutTime",  
        DailyReportTable.CheckInSnap  AS "CheckInSnap", 
        DailyReportTable.CheckOutSnap  AS "CheckOutSnap",  
        DailyReportTable.TimeWorked  AS "TimeWorked",
        Employee.EmpID AS "EmpID",
        Employee.CID AS "CID"
    FROM 
        Employee
    JOIN 
        DailyReportTable 
    ON 
        Employee.EmpID = DailyReportTable.EmpID 
    AND 
        Employee.CID = DailyReportTable.CID 
    WHERE 
        DailyReportTable.CID = p_cid AND  `CheckInTime` BETWEEN `startDateTime` AND `endDateTime`;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spGetCompanyDailyReportFromRange`(IN cid char(36), IN startDate DATETIME, IN endDate DATETIME)
BEGIN
    SELECT 
        CONCAT(Employee.FName, " ", Employee.LName) AS "Name", 
        Employee.PIN AS "Pin", 
        DailyReportTable.TypeID AS "Type", 
        DailyReportTable.CheckInTime  AS "CheckInTime", 
        DailyReportTable.CheckOutTime  AS "CheckOutTime",  
        DailyReportTable.TimeWorked  AS "TimeWorked"
    FROM 
		DailyReportTable
    JOIN
        Employee
 
    ON 
        Employee.EmpID = DailyReportTable.EmpID 
    AND 
        Employee.CID = DailyReportTable.CID 
    WHERE 
    
    `CheckInTime` BETWEEN `startDate` AND `endDate` AND DailyReportTable.CID = cid;
END //

DELIMITER ;


CREATE TABLE `WebsiteContactUs` (
  `FirstName` char(36) NOT NULL,
  `LastName` char(36) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `WhatsappNumber` varchar(20) DEFAULT NULL,
  `Subject` text,
  `PhoneNumber` varchar(20) DEFAULT NULL,
  `Message` text,
  `Address` varchar(255) DEFAULT NULL
);

DELIMITER //

CREATE  PROCEDURE `spCreateWebsiteContactUs`(
    IN p_FirstName CHAR(36),
    IN p_LastName CHAR(36),
    IN p_Email VARCHAR(255),
    IN p_WhatsappNumber VARCHAR(20),
    IN p_Subject TEXT,
    IN p_phoneNumber VARCHAR(20),
    IN p_Message TEXT,
    IN p_Address VARCHAR(255)
)
BEGIN
    INSERT INTO ContactUS (
        RequestID, 
        CID, 
        Name,
        RequestorEmail, 
        ConcernsQuestions, 
        PhoneNumber, 
        Status
    ) VALUES (
        p_requestId, 
        p_CID, 
        p_Name,
        p_requestorEmail, 
        p_concerns_questions, 
        p_phoneNumber, 
        p_status
    );
END //

DELIMITER ;