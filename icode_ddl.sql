create database icodeTest;
use icodeTest;

-- 68f9bafc-2390-11ef-82b6-02d83582ee21
CREATE TABLE `company` (
  `cid` char(36) PRIMARY KEY,
  `cname` varchar(36),
  `clogo` blob,
  `caddress` varchar(255),
  `username` varchar(255),
  `password` varchar(255)
);


-- Store Procedures for Companyu Table-- 

DELIMITER //

CREATE PROCEDURE CreateCompany(
  IN p_cid CHAR(36),
  IN p_cname VARCHAR(36),
  IN p_clogo BLOB,
  IN p_caddress VARCHAR(255),
  IN p_username VARCHAR(255),
  IN p_password VARCHAR(255)
)
BEGIN
    INSERT INTO company (cid, cname, clogo, caddress, username, password)
  VALUES (p_cid, p_cname, p_clogo, p_caddress, p_username, p_password);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE get_all_companies ()
BEGIN
  SELECT * FROM company;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE get_company (
IN p_cid CHAR(36)
)
BEGIN
  SELECT * FROM company WHERE cid = p_cid;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE update_company (
  IN p_cid CHAR(36),
  IN p_cname VARCHAR(36),
  IN p_clogo BLOB,
  IN p_caddress VARCHAR(255),
  IN p_username VARCHAR(255),
  IN p_password VARCHAR(255)
)
BEGIN
  UPDATE company
  SET cname = p_cname,
      clogo = p_clogo,
      caddress = p_caddress,
      username = p_username,
      password = p_password
  WHERE cid = p_cid;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE delete_company (
  IN p_cid CHAR(36)
)
BEGIN
  DELETE FROM company WHERE cid = p_cid;
END//

DELIMITER ;

-- 68f9bafc-2390-11ef-82b6-02d83582ee21
CALL CreateCompany("68f9bafc-2390-11ef-82b6-02d83582ee21", 'CompanyName', NULL, '1234 Address St.', 'username', 'password');
select * from company;

-- 9052c6d8-2391-11ef-82b6-02d83582ee21
CREATE TABLE `customer` (
  `customerid` char(36) PRIMARY KEY,
  `cid` char(36),
  `fname` varchar(255),
  `lname` varchar(255),
  `address` varchar(255),
  `phonenumber` varchar(255),
  `centername` varchar(255),
  `email` varchar(255),
  `isactive` boolean
);


DELIMITER //

CREATE PROCEDURE CreateCustomer(
    IN p_CustomerID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_Address VARCHAR(255),
    IN p_PhoneNumber VARCHAR(255),
    IN p_CenterName VARCHAR(255),
    IN p_Email VARCHAR(255),
    IN p_IsActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO customer (customerid, cid, fname, lname, address, phonenumber, centername, email, isactive)
    VALUES (p_CustomerID, p_CID, p_FName, p_LName, p_Address, p_PhoneNumber, p_CenterName, p_Email, p_IsActive);

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetCustomer(
    IN p_CustomerID CHAR(36)
)
BEGIN
    SELECT customerid, cid, fname, lname, address, phonenumber, centername, email, isactive
    FROM customer
    WHERE customerid = p_CustomerID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UpdateCustomer(
    IN p_CustomerID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_Address VARCHAR(255),
    IN p_PhoneNumber VARCHAR(255),
    IN p_CenterName VARCHAR(255),
    IN p_Email VARCHAR(255),
    IN p_IsActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE customer
    SET cid = p_CID,
        fname = p_FName,
        lname = p_LName,
        address = p_Address,
        phonenumber = p_PhoneNumber,
        centername = p_CenterName,
        email = p_Email,
        isactive = p_IsActive
    WHERE customerid = p_CustomerID;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE DeleteCustomer(
    IN p_CustomerID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM customer WHERE customerid = p_CustomerID;

    COMMIT;
END //

DELIMITER ;


CREATE TABLE `login` (
  `username` varchar(255) PRIMARY KEY,
  `cid` char(36),
  `password` varchar(255)
);

DELIMITER //

CREATE PROCEDURE CreateLogin(
    IN p_UserName VARCHAR(255),
    IN p_CID CHAR(36),
    IN p_Password VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO login (username, cid, password)
    VALUES (p_UserName, p_CID, p_Password);

    COMMIT;
END //

DELIMITER ;

select * from login;

DELIMITER //

CREATE PROCEDURE GetLogin(
    IN p_UserName VARCHAR(255)
)
BEGIN
    SELECT *
    FROM login
    WHERE username = p_UserName;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UpdateLogin(
    IN p_UserName VARCHAR(255),
    IN p_CID CHAR(36),
    IN p_Password VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE login
    SET cid = p_CID,
        password = p_Password
    WHERE username = p_UserName;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE DeleteLogin(
    IN p_UserName VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM login WHERE username = p_UserName;

    COMMIT;
END //

DELIMITER ;

CREATE TABLE `deviceSetting` (
  `deviceid` char(36),
  `cid` char(36),
  `devicename` varchar(255),
  `regid` varchar(255),
  `isactive` boolean,
  PRIMARY KEY (`deviceid`, `cid`)
);

DELIMITER //

CREATE PROCEDURE CreateDeviceSetting(
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

    INSERT INTO deviceSetting (deviceid, cid, devicename, regid, isactive)
    VALUES (p_DeviceID, p_CID, p_DeviceName, p_RegID, p_IsActive);

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetDeviceSetting(
    IN p_DeviceID CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    SELECT * FROM deviceSetting WHERE deviceid = p_DeviceID AND cid = p_CID;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE UpdateDeviceSetting(
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

    UPDATE deviceSetting
    SET devicename = p_DeviceName,
        regid = p_RegID,
        isactive = p_IsActive
    WHERE deviceid = p_DeviceID AND cid = p_CID;

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE DeleteDeviceSetting(
    IN p_DeviceID CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM deviceSetting WHERE deviceid = p_DeviceID AND cid = p_CID;

    COMMIT;
END //


DELIMITER ;

CREATE TABLE `employee` (
  `empid` char(36) PRIMARY KEY,
  `cid` char(36),
  `fname` varchar(255),
  `lname` varchar(255),
  `isactive` boolean,
  `phoneno` varchar(255),
  `pin` int
);


DELIMITER //

CREATE PROCEDURE CreateEmployee(
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

    INSERT INTO employee (empid, cid, fname, lname, isactive, phoneno, pin)
    VALUES (p_EmpID, p_CID, p_FName, p_LName, p_IsActive, p_PhoneNo, p_Pin);

    COMMIT;
END //

DELIMITER ;
CALL CreateEmployee('68f9bafc-2390-11ef-82b6-02d83582ee21', '68f9bafc-2390-11ef-82b6-02d83582ee21', 'John', 'Doe', TRUE, '555-1234', 1234);
select * from employee;

DELIMITER //

CREATE PROCEDURE GetEmployee(
    IN p_EmpID CHAR(36)
)
BEGIN
    SELECT * FROM employee WHERE empid = p_EmpID;
END //

DELIMITER ;
CALL GetEmployee('68f9bafc-2390-11ef-82b6-02d83582ee21');

DELIMITER //

CREATE PROCEDURE UpdateEmployee(
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

    UPDATE employee
    SET cid = p_CID,
        fname = p_FName,
        lname = p_LName,
        isactive = p_IsActive,
        phoneno = p_PhoneNo,
        pin = p_Pin
    WHERE empid = p_EmpID;

    COMMIT;
END //

DELIMITER ;
CALL UpdateEmployee('68f9bafc-2390-11ef-82b6-02d83582ee21', '68f9bafc-2390-11ef-82b6-02d83582ee21', 'John', 'Jackes', TRUE, '555-1234', 1234);


DELIMITER //

CREATE PROCEDURE DeleteEmployee(
    IN p_EmpID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM employee WHERE empid = p_EmpID;

    COMMIT;
END //

DELIMITER ;
CALL DeleteEmployee('68f9bafc-2390-11ef-82b6-02d83582ee21');



CREATE TABLE `reportRecipients` (
  `checkinid` char(36) PRIMARY KEY,
  `cid` char(36),
  `emailid` varchar(255),
  `exec` boolean
);


DELIMITER //

CREATE PROCEDURE CreateReportRecipient(
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

    INSERT INTO reportRecipients (checkinid, cid, emailid, exec)
    VALUES (p_CheckinID, p_CID, p_EmailID, p_Exec);

    COMMIT;
END //

DELIMITER ;
CALL CreateReportRecipient('ba6ab250-23aa-11ef-82b6-02d83582ee22', '68f9bafc-2390-11ef-82b6-02d83582ee22', 'email@example.com', True);
select * from reportRecipients;
DELIMITER //

CREATE PROCEDURE GetReportRecipient(
    IN p_CheckinID CHAR(36)
)
BEGIN
    SELECT * FROM reportRecipients WHERE checkinid = p_CheckinID;
END //

DELIMITER ;
CALL GetReportRecipient('ba6ab250-23aa-11ef-82b6-02d83582ee22');

DELIMITER //

CREATE PROCEDURE UpdateReportRecipient(
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

    UPDATE reportRecipients
    SET cid = p_CID,
        emailid = p_EmailID,
        exec = p_Exec
    WHERE checkinid = p_CheckinID;

    COMMIT;
END //

DELIMITER ;
CALL UpdateReportRecipient('ba6ab250-23aa-11ef-82b6-02d83582ee22', '68f9bafc-2390-11ef-82b6-02d83582ee22', 'updated@example.com', FALSE);

DELIMITER //

CREATE PROCEDURE DeleteReportRecipient(
    IN p_CheckinID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM reportRecipients WHERE checkinid = p_CheckinID;

    COMMIT;
END //

DELIMITER ;
CALL DeleteReportRecipient('ba6ab250-23aa-11ef-82b6-02d83582ee22');


CREATE TABLE `checkInType` (
  `typeid` char(36) PRIMARY KEY,
  `cid` char(36),
  `typenames` varchar(255)
);

DELIMITER //

CREATE PROCEDURE CreateCheckInType(
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

    INSERT INTO checkInType (typeid, cid, typenames)
    VALUES (p_TypeID, p_CID, p_TypeNames);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE ReadCheckInType(
    IN p_TypeID CHAR(36)
)
BEGIN
    SELECT * FROM checkInType WHERE typeid = p_TypeID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UpdateCheckInType(
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

    UPDATE checkInType
    SET cid = p_CID,
        typenames = p_TypeNames
    WHERE typeid = p_TypeID;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE DeleteCheckInType(
    IN p_TypeID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM checkInType WHERE typeid = p_TypeID;

    COMMIT;
END //

DELIMITER ;


CREATE TABLE `reportType` (
  `reporttypeid` char(36) PRIMARY KEY,
  `reporttypename` varchar(255)
);

DELIMITER //

CREATE PROCEDURE CreateReportType(
    IN p_ReportTypeID CHAR(36),
    IN p_ReportTypeName VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO reportType (reporttypeid, reporttypename)
    VALUES (p_ReportTypeID, p_ReportTypeName);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE GetReportType(
    IN p_ReportTypeID CHAR(36)
)
BEGIN
    SELECT * FROM reportType WHERE reporttypeid = p_ReportTypeID;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UpdateReportType(
    IN p_ReportTypeID CHAR(36),
    IN p_ReportTypeName VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE reportType
    SET reporttypename = p_ReportTypeName
    WHERE reporttypeid = p_ReportTypeID;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE DeleteReportType(
    IN p_ReportTypeID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM reportType WHERE reporttypeid = p_ReportTypeID;

    COMMIT;
END //

DELIMITER ;


CREATE TABLE `companyReportType` (
  `companyreporttypeid` char(36) PRIMARY KEY,
  `cid` char(36),
  `reporttypeid` char(36),
  `isdailyreportactive` boolean
);


DELIMITER //

CREATE PROCEDURE CreateCompanyReportType(
    IN p_CompanyReportTypeID CHAR(36),
    IN p_CID CHAR(36),
    IN p_ReportTypeID CHAR(36),
    IN p_IsDailyReportActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO companyReportType(companyreporttypeid, cid, reporttypeid, isdailyreportactive)
    VALUES (p_CompanyReportTypeID, p_CID, p_ReportTypeID, p_IsDailyReportActive);

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetCompanyReportType(
    IN p_CompanyReportTypeID CHAR(36)
)
BEGIN
    SELECT * FROM companyReportType WHERE companyreporttypeid = p_CompanyReportTypeID;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE UpdateCompanyReportType(
    IN p_CompanyReportTypeID CHAR(36),
    IN p_CID CHAR(36),
    IN p_ReportTypeID CHAR(36),
    IN p_IsDailyReportActive BOOLEAN
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE companyReportType
    SET cid = p_CID,
        reporttypeid = p_ReportTypeID,
        isdailyreportactive = p_IsDailyReportActive
    WHERE companyreporttypeid = p_CompanyReportTypeID;

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE DeleteCompanyReportType(
    IN p_CompanyReportTypeID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM companyReportType WHERE companyreporttypeid = p_CompanyReportTypeID;

    COMMIT;
END //

DELIMITER ;


CREATE TABLE `reportSchedule` (
  `reportid` char(36),
  `cid` char(36),
  `reporttypeid` char(36),
  `isdelivered` boolean,
  `isactive` boolean,
  `reporttimegenerated` datetime,
  `reporttimesent` datetime,
  `textreporttime` varchar(255),
  `createdat` datetime,
  `updatedat` datetime,
  PRIMARY KEY (`reportid`, `cid`)
);

DELIMITER //

CREATE PROCEDURE CreateReportSchedule(
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

    INSERT INTO reportSchedule (reportid, cid, reporttypeid, isdelivered, isactive, reporttimegenerated, reporttimesent, textreporttime, createdat, updatedat)
    VALUES (p_ReportID, p_CID, p_ReportTypeID, p_IsDelivered, p_IsActive, p_ReportTimeGenerated, p_ReportTimeSent, p_TextReportTime, p_CreatedAt, p_UpdatedAt);

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetReportSchedule(
    IN p_ReportID CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    SELECT * FROM reportSchedule WHERE reportid = p_ReportID AND cid = p_CID;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE UpdateReportSchedule(
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

    UPDATE reportSchedule
    SET reporttypeid = p_ReportTypeID,
        isdelivered = p_IsDelivered,
        isactive = p_IsActive,
        reporttimegenerated = p_ReportTimeGenerated,
        reporttimesent = p_ReportTimeSent,
        textreporttime = p_TextReportTime,
        createdat = p_CreatedAt,
        updatedat = p_UpdatedAt
    WHERE reportid = p_ReportID AND cid = p_CID;

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE DeleteReportSchedule(
    IN p_ReportID CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    DELETE FROM reportSchedule WHERE reportid = p_ReportID AND cid = p_CID;

    COMMIT;
END //

DELIMITER ;


ALTER TABLE `customer` ADD FOREIGN KEY (`cid`) REFERENCES `company` (`cid`);

ALTER TABLE `login` ADD FOREIGN KEY (`cid`) REFERENCES `company` (`cid`);

ALTER TABLE `deviceSetting` ADD FOREIGN KEY (`cid`) REFERENCES `company` (`cid`);

ALTER TABLE `employee` ADD FOREIGN KEY (`cid`) REFERENCES `company` (`cid`);

ALTER TABLE `reportRecipients` ADD FOREIGN KEY (`cid`) REFERENCES `company` (`cid`);

ALTER TABLE `checkInType` ADD FOREIGN KEY (`cid`) REFERENCES `company` (`cid`);

ALTER TABLE `companyReportType` ADD FOREIGN KEY (`cid`) REFERENCES `company` (`cid`);
ALTER TABLE `companyReportType` ADD FOREIGN KEY (`reporttypeid`) REFERENCES `reportType` (`reporttypeid`);

ALTER TABLE `reportSchedule` ADD FOREIGN KEY (`cid`) REFERENCES `company` (`cid`);
ALTER TABLE `reportSchedule` ADD FOREIGN KEY (`reporttypeid`) REFERENCES `reportType` (`reporttypeid`);

