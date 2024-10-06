CREATE TABLE `Company` (
  `CID` char(36) NOT NULL,
  `CName` varchar(36) DEFAULT NULL,
  `CLogo` blob,
  `CAddress` varchar(255) DEFAULT NULL,
  `ReportType` varchar(255) DEFAULT NULL,
  `UserName` varchar(255) NOT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `InsertedDateTime` varchar(255) DEFAULT NULL,
  `LastModifiedDateTime` varchar(255) DEFAULT NULL,
  `LastModifiedBy` varchar(255) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`CID`,`UserName`)
);



DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateEmployee`(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_IsActive BOOLEAN,
    IN p_PhoneNo VARCHAR(255),
    IN p_Pin char(10),
    IN p_IsAdmin BOOLEAN,
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Employee
    SET CID =  COALESCE(p_CID,CID),
        FName = COALESCE(p_FName,FName),
        LName = COALESCE(p_LName,LName),
        IsActive = COALESCE(p_IsActive,IsActive),
        PhoneNumber = COALESCE(p_PhoneNo,PhoneNumber),
        Pin = COALESCE(p_Pin,Pin),
        IsAdmin = COALESCE(p_IsAdmin,IsAdmin),
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE EmpID = p_EmpID AND IsActive = TRUE;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateDevice`(
	IN p_timezone CHAR(36),
    IN p_deviceID CHAR(36),
    IN p_CID CHAR(36),
    IN p_deviceName VARCHAR(255),
    IN p_accessKey VARCHAR(255),
    IN p_accessKeyCreatedDateTime DATETIME,
    IN p_IsActive BOOLEAN,
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Device
    SET 
		TimeZone = COALESCE(p_timezone,TimeZone),
        DeviceID = COALESCE(p_deviceID,DeviceID),
        DeviceName = COALESCE(p_deviceName,DeviceName),
        AccessKeyGeneratedTime = COALESCE(p_accessKeyCreatedDateTime,AccessKeyGeneratedTime),
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE 
        AccessKey = p_accessKey AND
        CID = p_CID AND IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateDailyReport`(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_Date DATE,
    IN p_TypeID CHAR(36),
    IN p_CheckInSnap BLOB,
    IN p_CheckInTime DATETIME,
    IN p_CheckOutSnap BLOB,
    IN p_CheckOutTime DATETIME,
    IN p_TimeWorked VARCHAR(255),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    UPDATE DailyReportTable
    SET 
        TypeID = COALESCE(p_TypeID,TypeID),
        Date = COALESCE(p_Date,Date),
        CheckInSnap = COALESCE(p_CheckInSnap,CheckInSnap),
        CheckOutSnap = COALESCE(p_CheckOutSnap,CheckOutSnap),
        CheckOutTime = COALESCE(p_CheckOutTime,CheckOutTime),
        TimeWorked = COALESCE(p_TimeWorked,TimeWorked),
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE 
        EmpID = p_EmpID AND
        CID = p_CID AND
        CheckInTime = p_CheckInTime AND IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateCustomer`(
    IN p_CustomerID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_Address VARCHAR(255),
    IN p_PhoneNumber VARCHAR(255),
    IN p_Email VARCHAR(255),
    IN p_IsActive BOOLEAN,
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Customer
    SET CID = COALESCE(p_CID,CID),
        FName = COALESCE(p_FName,FName),
        LName = COALESCE(p_LName,LName),
        Address = COALESCE(p_Address,Address),
        PhoneNumber = COALESCE(p_PhoneNumber,PhoneNumber),
        Email = COALESCE(p_Email,Email),
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE CustomerID = p_CustomerID AND IsActive = TRUE;

    COMMIT;
END

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateContact`(
    IN p_requestId CHAR(36),
    IN p_CID CHAR(36),
    IN p_Name CHAR(36),
    IN p_requestorEmail VARCHAR(255),
    IN p_concerns_questions TEXT,
    IN p_phoneNumber VARCHAR(20),
    IN p_status VARCHAR(50),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    UPDATE ContactUS
    SET 
        CID = COALESCE(p_CID,CID),
        Name = COALESCE(p_Name,Name),
        RequestorEmail = COALESCE(p_requestorEmail, RequestorEmail),
        ConcernsQuestions = COALESCE(p_concerns_questions,ConcernsQuestions),
        PhoneNumber = COALESCE(p_phoneNumber,PhoneNumber),
        Status = COALESCE(p_status,Status),
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE 
        RequestID = p_requestId AND IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateCompanyReportType`(
    IN p_CompanyReporterEmail CHAR(36),
    IN p_CID CHAR(36),
    IN p_IsDailyReportActive BOOLEAN,
    IN p_IsWeeklyReportActive BOOLEAN,
    IN p_IsBiWeeklyReportActive BOOLEAN,
    IN p_IsMonthlyReportActive BOOLEAN,
    IN p_IsBiMonthlyReportActive BOOLEAN,
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE CompanyReportType
    SET IsDailyReportActive = COALESCE(p_IsDailyReportActive,IsDailyReportActive),
        IsWeeklyReportActive = COALESCE(p_IsWeeklyReportActive,IsWeeklyReportActive),
        IsBiWeeklyReportActive = COALESCE(p_IsBiWeeklyReportActive,IsBiWeeklyReportActive),
        IsMonthlyReportActive = COALESCE(p_IsMonthlyReportActive,IsMonthlyReportActive),
        IsBiMonthlyReportActive = COALESCE(p_IsBiMonthlyReportActive,IsBiMonthlyReportActive),
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID AND IsActive = TRUE;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateCompanyReport`(
    IN p_company_id CHAR(36),
    IN p_report_type VARCHAR(255),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    UPDATE Company
    SET ReportType = COALESCE(p_report_type,ReportType),
    LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
	LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE CID = p_company_id AND IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateCompany`(
  IN p_cid CHAR(36),
  IN p_cname VARCHAR(36),
  IN p_clogo BLOB,
  IN p_caddress VARCHAR(255),
  IN p_username VARCHAR(255),
  IN p_password VARCHAR(255),
  IN p_reportType VARCHAR(255),
  IN p_LastModifiedDateTime VARCHAR(255),
  IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
  UPDATE Company
  SET CName = COALESCE(p_cname,CName),
      CLogo = COALESCE(p_clogo,CLogo),
      CAddress = COALESCE(p_caddress,CAddress),
      UserName = COALESCE(p_username,UserName),
      Password = COALESCE(p_password,Password),
      ReportType = COALESCE(p_reportType,ReportType),
      LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
	  LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
  WHERE CID = p_cid AND IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spUpdateAdminReportType`(
  IN p_cid CHAR(36),
  IN p_reportType VARCHAR(255),
  IN p_LastModifiedDateTime VARCHAR(255),
  IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
  UPDATE Company
  SET ReportType = COALESCE(p_reportType,ReportType),
	  LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
	  LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
  WHERE CID = p_cid AND IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetUser`(
IN p_username CHAR(36)
)
BEGIN
  SELECT * FROM Company WHERE UserName = p_username AND IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //CREATE DEFINER=`admin`@`%` PROCEDURE `spGetEmployeeDailyReport`(IN p_cid CHAR(36),  IN reportDate DATE)
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
        DailyReportTable.CID = p_cid AND  DailyReportTable.Date = reportDate AND Employee.IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetEmployeeDailyBasisReport`(
IN p_eid CHAR(36),
IN reportDate DATE)
BEGIN
    SELECT  * FROM  DailyReportTable 

    WHERE EmpID = p_eid AND Date = reportDate AND IsActive = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetEmployeeCount`(
	IN p_CID CHAR(36)
)
BEGIN
  SELECT COUNT(EmpID) AS employee_count FROM Employee WHERE CID = p_CID AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetEmployee`(
    IN p_EmpID CHAR(36)
)
BEGIN
    SELECT * FROM Employee WHERE EmpID = p_EmpID AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetDailyReport`(
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
        CheckInTime = p_CheckInTime AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetCustomerUsingCID`(
IN p_cid CHAR(36)
)
BEGIN
  SELECT * FROM Customer WHERE CID = p_cid AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetCustomer`(
    IN p_CustomerID CHAR(36)
)
BEGIN
    SELECT *
    FROM Customer
    WHERE CustomerID = p_CustomerID AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetContact`(
    IN p_requestId CHAR(36)
)
BEGIN
    SELECT 
        *
    FROM 
        ContactUS
    WHERE 
        RequestID = p_requestId AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetCompanyReportType`(
    IN p_CompanyReporterEmail CHAR(36),
    IN p_CID CHAR(36)
)
BEGIN
    SELECT * FROM CompanyReportType WHERE CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetCompanyDailyReportFromRange`(IN cid char(36), IN startDate DATETIME, IN endDate DATETIME)
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
    
    `CheckInTime` BETWEEN `startDate` AND `endDate` AND DailyReportTable.CID = cid AND Employee.IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetCompanyDailyReportFromDateRange`(IN cid char(36), IN startDate DATE, IN endDate Date)
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
    
    Date >= startDate AND Date < endDate + INTERVAL 1 DAY AND CID = cid AND Employee.IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetCompanyBasedDailyReport`(IN p_cid CHAR(36),  IN startDateTime DATETIME, endDateTime DATETIME)
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
        DailyReportTable.CID = p_cid AND Employee.IsActive = true AND  `CheckInTime` BETWEEN `startDateTime` AND `endDateTime`;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetCompany`(
IN p_cid CHAR(36)
)
BEGIN
  SELECT * FROM Company WHERE CID = p_cid AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetAllEmployee`(
	IN p_CID CHAR(36)
)
BEGIN
  SELECT * FROM Employee WHERE CID = p_CID AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetAllDevicesWithoutBasedOnCID`()
BEGIN
    SELECT * FROM Device WHERE IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetAllDevices`(
IN p_cid CHAR(36)
)
BEGIN
    SELECT * FROM Device WHERE CID = p_cid AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetAllCompanyReportType`(
    IN p_CID CHAR(36)
)
BEGIN
    SELECT * FROM CompanyReportType WHERE CID = p_CID AND IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetAllCompanies`()
BEGIN
  SELECT * FROM Company WHERE IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetAllCustomers`()
BEGIN
  SELECT * FROM Customer WHERE IsActive = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spGetAdmin`(
	IN p_CID CHAR(36)
)
BEGIN
  SELECT * FROM Employee WHERE CID = p_CID AND IsActive = true AND IsAdmin = true;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spDeleteEmployee`(
    IN p_EmpID CHAR(36),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Employee
    SET 
        IsActive = false,
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE EmpID = p_EmpID AND IsActive = true;

    COMMIT;
END //

DELIMITER ;



DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spDeleteDevice`(
    IN p_accessKey CHAR(36),
    IN p_cid CHAR(36),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Device
    SET 
        IsActive = false,
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE  AccessKey = p_accessKey AND CID = p_CID AND IsActive = true;

    COMMIT;
END //

DELIMITER ;



DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spDeleteDailyReport`(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_CheckInTime DATETIME,
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE DailyReportTable
    SET 
        IsActive = false,
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE  EmpID = p_EmpID AND CID = p_CID AND CheckInTime = p_CheckInTime AND IsActive = true;

    COMMIT;
END //

DELIMITER ;




DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spDeleteCustomer`(
    IN p_CustomerID CHAR(36),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Customer
    SET 
        IsActive = false,
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE  CustomerID = p_CustomerID AND IsActive = true;

    COMMIT;
END //

DELIMITER ;



DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spDeleteContact`(
    IN p_requestId CHAR(36),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE ContactUS
    SET 
        IsActive = false,
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE  RequestID = p_requestId AND IsActive = true;

    COMMIT;
END //

DELIMITER ;



DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spDeleteCompanyReportType`(
    IN p_CompanyReporterEmail CHAR(36),
    IN p_CID CHAR(36),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE CompanyReportType
    SET 
        IsActive = false,
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE  CompanyReporterEmail = p_CompanyReporterEmail AND CID = p_CID AND IsActive = true;

    COMMIT;
END //

DELIMITER ;



DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spDeleteCompany`(
    IN p_cid CHAR(36),
    IN p_LastModifiedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    UPDATE Company
    SET 
        IsActive = false,
        LastModifiedDateTime = COALESCE(p_LastModifiedDateTime,LastModifiedDateTime),
        LastModifiedBy = COALESCE(p_LastModifiedBy,LastModifiedBy)
    WHERE  CID = p_cid AND IsActive = true;

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spCreateWebsiteContactUs`(
    IN p_FirstName CHAR(36),
    IN p_LastName CHAR(36),
    IN p_Email VARCHAR(255),
    IN p_WhatsappNumber VARCHAR(20),
    IN p_Subject TEXT,
    IN p_phoneNumber VARCHAR(20),
    IN p_Message TEXT,
    IN p_Address VARCHAR(255),
    IN p_InsertedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    INSERT INTO WebsiteContactUs (
        FirstName, 
        LastName, 
        Email,
        WhatsappNumber, 
        Subject, 
        PhoneNumber, 
        Message,
        Address,
        InsertedDateTime,
        LastModifiedBy
        
    ) VALUES (
        p_FirstName, 
        p_LastName, 
        p_Email,
        p_WhatsappNumber, 
        p_Subject, 
        p_phoneNumber, 
        p_Message,
        p_Address,
        p_InsertedDateTime,
        p_LastModifiedBy
    );
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spCreateEmployee`(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_IsActive BOOLEAN,
    IN p_PhoneNo VARCHAR(255),
    IN p_Pin char(10),
    IN p_IsAdmin BOOLEAN,
    IN p_InsertedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO Employee (EmpID, CID, FName, LName, IsActive, PhoneNumber, Pin, IsAdmin, InsertedDateTime,
        LastModifiedBy)
    VALUES (p_EmpID, p_CID, p_FName, p_LName, p_IsActive, p_PhoneNo, p_Pin, p_IsAdmin,p_InsertedDateTime,
        p_LastModifiedBy);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spCreateDevice`(
	IN p_timezone CHAR(36),
    IN p_deviceID CHAR(36),
    IN p_CID CHAR(36),
    IN p_deviceName VARCHAR(255),
    IN p_accessKey VARCHAR(255),
    IN p_accessKeyCreatedDateTime DATETIME,
    IN p_IsActive BOOLEAN,
    IN p_InsertedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO Device (TimeZone, DeviceID, CID, DeviceName, AccessKey, AccessKeyGeneratedTime, IsActive, InsertedDateTime,
        LastModifiedBy)
    VALUES (p_timezone, p_deviceID, p_CID, p_deviceName, p_accessKey, p_accessKeyCreatedDateTime, p_IsActive,p_InsertedDateTime,
        p_LastModifiedBy);

    COMMIT;
END

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spCreateDailyReport`(
    IN p_EmpID CHAR(36),
    IN p_CID CHAR(36),
    IN p_TypeID CHAR(36),
    IN p_CheckInSnap BLOB,
    IN p_CheckInTime DATETIME,
    IN p_CheckOutSnap BLOB,
    IN p_CheckOutTime DATETIME,
    IN p_TimeWorked VARCHAR(255),
    IN p_Date DATE,
    IN p_InsertedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
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
        Date,
        InsertedDateTime,
        LastModifiedBy
    ) VALUES (
        p_EmpID, 
        p_CID, 
        p_TypeID, 
        p_CheckInSnap, 
        p_CheckInTime, 
        p_CheckOutSnap, 
        p_CheckOutTime, 
        p_TimeWorked,
        p_Date,
        p_InsertedDateTime,
        p_LastModifiedBy
    );
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spCreateCustomer`(
    IN p_CustomerID CHAR(36),
    IN p_CID CHAR(36),
    IN p_FName VARCHAR(255),
    IN p_LName VARCHAR(255),
    IN p_Address VARCHAR(255),
    IN p_PhoneNumber VARCHAR(255),
    IN p_Email VARCHAR(255),
    IN p_IsActive BOOLEAN,
    IN p_InsertedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    INSERT INTO Customer (CustomerID, CID, FName, LName, Address, PhoneNumber, Email, IsActive, InsertedDateTime,
        LastModifiedBy)
    VALUES (p_CustomerID, p_CID, p_FName, p_LName, p_Address, p_PhoneNumber, p_Email, p_IsActive, p_InsertedDateTime,
        p_LastModifiedBy);

    COMMIT;
END //

DELIMITER ;


DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spCreateContact`(
    IN p_requestId CHAR(36),
    IN p_CID CHAR(36),
    IN p_Name CHAR(36),
    IN p_requestorEmail VARCHAR(255),
    IN p_concerns_questions TEXT,
    IN p_phoneNumber VARCHAR(20),
    IN p_status VARCHAR(50),
    IN p_InsertedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    INSERT INTO ContactUS (
        RequestID, 
        CID, 
        Name,
        RequestorEmail, 
        ConcernsQuestions, 
        PhoneNumber, 
        Status,
        InsertedDateTime,
        LastModifiedBy
    ) VALUES (
        p_requestId, 
        p_CID, 
        p_Name,
        p_requestorEmail, 
        p_concerns_questions, 
        p_phoneNumber, 
        p_status,
        p_InsertedDateTime,
        p_LastModifiedBy
    );
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spCreateCompanyReportType`(
    IN p_CompanyReporterEmail CHAR(36),
    IN p_CID CHAR(36),
    IN p_IsDailyReportActive BOOLEAN,
    IN p_IsWeeklyReportActive BOOLEAN,
    IN p_IsBiWeeklyReportActive BOOLEAN,
    IN p_IsMonthlyReportActive BOOLEAN,
    IN p_IsBiMonthlyReportActive BOOLEAN,
    IN p_InsertedDateTime VARCHAR(255),
    IN p_LastModifiedBy VARCHAR(255)
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
        IsBiMonthlyReportActive, InsertedDateTime,
        LastModifiedBy)
    VALUES (p_CompanyReporterEmail, p_CID, p_IsDailyReportActive,
        p_IsWeeklyReportActive,
        p_IsBiWeeklyReportActive,
        p_IsMonthlyReportActive,
        p_IsBiMonthlyReportActive, p_InsertedDateTime,
        p_LastModifiedBy);

    COMMIT;
END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`admin`@`%` PROCEDURE `spCreateCompany`(
  IN p_cid CHAR(36),
  IN p_cname VARCHAR(36),
  IN p_clogo BLOB,
  IN p_caddress VARCHAR(255),
  IN p_username VARCHAR(255),
  IN p_password VARCHAR(255),
  IN p_reportType VARCHAR(255),
  IN p_InsertedDateTime VARCHAR(255),
  IN p_LastModifiedBy VARCHAR(255)
)
BEGIN
    INSERT INTO Company (CID, CName, CLogo, CAddress, UserName, Password, ReportType, InsertedDateTime,
        LastModifiedBy)
  VALUES (p_cid, p_cname, p_clogo, p_caddress, p_username, p_password, p_reportType, p_InsertedDateTime,
        p_LastModifiedBy);
END //

DELIMITER ;
