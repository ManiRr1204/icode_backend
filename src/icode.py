from datetime import date
from fastapi import FastAPI, Body
import mangum
import pymysql

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials = True, allow_methods=["*"], allow_headers=["*"]
)

def connect_to_database():
    try:
        connection = pymysql.connect(
            host="mydb.cxms2oikutcu.us-west-2.rds.amazonaws.com",
            user="admin",
            password="databasepass",
            database="icode",
            cursorclass=pymysql.cursors.DictCursor 
        )
        return connection
    except pymysql.MySQLError as err:
        print(f"Error connecting to database: {err}")
        return None

@app.get("/test")
def get_test():
   return {"response": "Test get call successfully called"}

@app.get("/company/get")
def get_all_companies():
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetAllCompanies'
            cursor.execute(sql)
            myresult = cursor.fetchall()
            return myresult
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/company/get/{company_id}")
def get_company(company_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetCompany(%s)'
            cursor.execute(sql, (company_id,))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"error": f"Company with ID '{company_id}' not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/company/getuser/{userName}")
def get_company(userName: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetUser(%s)'
            cursor.execute(sql, (userName,))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"error": "UserName not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# POST request to create a company
@app.post("/company/create")
async def create_company(company: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            cid = company.get("CID")
            cname = company.get("CName")
            clogo = company.get("CLogo") 
            caddress = company.get("CAddress")
            username = company.get("UserName")
            password = company.get("Password")
            reportType = company.get("ReportType")

            # Check if username is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Company WHERE UserName = %s"
            cursor.execute(check_sql, (username,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "UserName already exists"}

            else:
                sql = "CALL spCreateCompany(%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (cid, cname, clogo, caddress, username, password, reportType))
                connection.commit()

                return {"message": "Company created successfully", "CID": cid, "UserName": username}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a company
@app.delete("/company/delete/{company_id}")
async def delete_company(company_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            # Check if username is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Company WHERE CID = %s"
            cursor.execute(check_sql, (company_id,))
            result = cursor.fetchone()

            if result['count'] > 0:
                sql = "CALL spDeleteCompany(%s)"
                cursor.execute(sql, (company_id,))
                connection.commit()  # Commit changes

                return {"message": f"Company with ID '{company_id}' deleted successfully"}
            else:
                return {"error": "Company id not found"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# PUT request to update a company
@app.put("/company/update/{company_id}")
async def update_company(company_id: str, company: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
           # Extract data from request body
            cname = company.get("CName")
            clogo = company.get("CLogo") 
            caddress = company.get("CAddress")
            username = company.get("UserName")
            password = company.get("Password")
            reportType = company.get("ReportType")
            
            
            check_sql = "SELECT COUNT(*) AS count FROM Company WHERE UserName = %s"
            cursor.execute(check_sql, (username))
            result = cursor.fetchone()
            if result['count'] > 0:

                check_sql_2 = "SELECT COUNT(*) AS count FROM Company WHERE UserName = %s AND CID = %s"
                cursor.execute(check_sql_2, (username, company_id))
                result_2 = cursor.fetchone()

                if result_2['count'] > 0:
                    sql = "CALL spUpdateCompany(%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (company_id, cname, clogo, caddress, username, password, reportType))
                    connection.commit()
                    return {"message": "Company updated successfully", "CID": company_id, "UserName": username}
                
                else:
                    return {"error": "UserName already exists with different company"}

            else:

                sql = "CALL spUpdateCompany(%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (company_id, cname, clogo, caddress, username, password, reportType))
                connection.commit()

                return {"message": "Company updated successfully", "CID": company_id, "UserName": username}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.put("/company/update/report_type/{company_id}")
async def update_report_type(company_id: str, report_type: str = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Call the stored procedure to update the ReportType
            sql = "CALL spUpdateReportType(%s, %s)"
            cursor.execute(sql, (company_id, report_type))
            connection.commit()
            return {"message": "Company Report type updated successfully", "CID": company_id, "ReportType": report_type}
    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/customer/get/{customer_id}")
async def get_customer_by_id(customer_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetCustomer(%s)" 
            mycursor.execute(sql, (customer_id,))
            customer = mycursor.fetchone()
            if customer:
                return customer
            else:
                return {"error": "Customer id not found"}

    except pymysql.connector.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/customer/getUsingCID/{c_id}")
def get_company(c_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetCustomerUsingCID(%s)'
            cursor.execute(sql, (c_id,))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"error": "Customer ID not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# POST request to create a company
@app.post("/customer/create")
async def create_customer(customer = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            
            customer_id = customer.get("CustomerID")
            cid = customer.get("CID")
            fname = customer.get("FName")
            lname = customer.get("LName")
            address = customer.get("Address")
            phone_number = customer.get("PhoneNumber")
            email = customer.get("Email")
            is_active = customer.get("IsActive")
            
            check_sql = "SELECT COUNT(*) AS count FROM Customer WHERE CustomerID = %s"
            cursor.execute(check_sql, (customer_id))
            result = cursor.fetchone()

            if result['count'] > 0:
                return {"error": "Customer id already exists"}

            else:
                sql = "CALL spCreateCustomer(%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (customer_id, cid, fname, lname, address, phone_number, email, is_active))
                connection.commit()

                return {"message": "Customer created successfully", "CustomerID": customer_id}

    except pymysql.connector.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a customer_id
@app.delete("/customer/delete/{customer_id}")
async def delete_customer(customer_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM Customer WHERE CustomerID = %s"
            cursor.execute(check_sql, (customer_id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                sql = "CALL spDeleteCustomer(%s)"
                cursor.execute(sql, (customer_id,))
                connection.commit()

                return {"message": f"Customer with ID '{customer_id}' deleted successfully"}
            else:
                return {"error": "Customer id not found", "CustomerID": customer_id}                

    except pymysql.connector.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# PUT request to update a company
@app.put("/customer/update/{customer_id}")
async def update_customer(customer_id: str, customer = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM Customer WHERE CustomerID = %s"
            cursor.execute(check_sql, (customer_id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                sql = "CALL spUpdateCustomer(%(CustomerID)s, %(CID)s, %(FName)s, %(LName)s, %(Address)s, %(PhoneNumber)s, %(Email)s, %(IsActive)s)"
                cursor.execute(sql, customer)
                connection.commit()  # Commit changes
                return {"message": f"Customer with ID '{customer_id}' updated successfully"}
            else:
                return {"error": "Customer id not found", "CustomerID": customer_id} 

    except pymysql.connector.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/deviceSetting/get/{deviceId},{companyId}")
async def get_device_setting(deviceId: str,companyId : str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetDeviceSetting(%s, %s);"
            mycursor.execute(sql, (deviceId,companyId,))  # Enclose emp_id in a tuple
            myresult = mycursor.fetchall()
            if myresult:
                return myresult
            else:
                return {"message": f"{companyId} with device id '{deviceId}' not found"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


# POST request to create a employee
@app.post("/deviceSetting/create")
async def create_device_setting(deviceSetting: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            
            deviceid = deviceSetting.get("DeviceID")
            cid = deviceSetting.get("CID")
            devicename = deviceSetting.get("DeviceName") 
            regid = deviceSetting.get("RegID")
            isactive =  deviceSetting.get("IsActive")

            # Check if device id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM DeviceSetting WHERE DeviceID = %s"
            cursor.execute(check_sql, (deviceid,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "DeviceID already exists"}

            else:
                sql = "CALL spCreateDeviceSetting(%s, %s, %s, %s, %s);"
                cursor.execute(sql, (deviceid, cid, devicename, regid, isactive))
                connection.commit()  
                return {"message": "deviceSetting created successfully", "DeviceID": deviceid}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a company
@app.delete("/deviceSetting/delete/{deviceId},{companyId}")
async def delete_device_setting(deviceId: str,companyId: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Check if device id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM DeviceSetting WHERE DeviceID = %s"
            cursor.execute(check_sql, (deviceId,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = "CALL spDeleteDeviceSetting(%s,%s)"
                cursor.execute(sql, (deviceId,companyId,))
                connection.commit()

                return {"message": f"deviceSetting with ID '{deviceId}' deleted successfully"}
            else:
                return {"error": "DeviceID not found", "DeviceID": deviceId, "CompanyID": companyId}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# PUT request to update a employee
@app.put("/deviceSetting/update/{deviceId},{companyId}")
async def update_device_setting(deviceId: str, companyId: str, deviceSetting: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            devicename = deviceSetting.get("DeviceName") 
            regid = deviceSetting.get("RegID")
            isactive =  deviceSetting.get("IsActive")

            # Check if device id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM DeviceSetting WHERE DeviceID = %s"
            cursor.execute(check_sql, (deviceId,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = "CALL spUpdateDeviceSetting(%s, %s, %s, %s, %s)"
                cursor.execute(sql, (deviceId, companyId, devicename, regid, isactive))
                connection.commit()

                return {"message": f"deviceSetting with ID '{deviceId}' updated successfully"}
            else:
               return {"error": "DeviceID not found", "DeviceID": deviceId, "CompanyID": companyId}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/employee/getall/{cid}")
async def get__all_employee(cid : str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetAllEmployee(%s);"
            mycursor.execute(sql, (cid,)) 
            employee = mycursor.fetchall()

            if employee:
                return employee
            else:
                return {"error": f"Company with ID '{cid}' not found"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()



@app.get("/employee/get/{emp_id}")
async def get_employee(emp_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetEmployee(%s);"
            mycursor.execute(sql, (emp_id,))  # Enclose emp_id in a tuple
            employee = mycursor.fetchall()
            if employee:
                return employee
            else:
                return {"error": f"Employee with ID '{emp_id}' not found"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


# POST request to create a employee
@app.post("/employee/create")
async def create_employee(employee: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            empid = employee.get("EmpID")
            cid = employee.get("CID")
            fname = employee.get("FName")
            lname = employee.get("LName")
            isactive =  employee.get("IsActive")
            phoneno = employee.get("PhoneNumber")
            pin = employee.get("Pin")
            
            # Check if username is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Employee WHERE EmpID = %s"
            cursor.execute(check_sql, (empid,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Employee already exists"}
            else:
                
                sql = "CALL spCreateEmployee(%s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (empid, cid, fname, lname, isactive, phoneno,pin))
                connection.commit()

                return {"message": "Employee created successfully", "EmpID": empid}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a company
@app.delete("/employee/delete/{emp_id}")
async def delete_employee(emp_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            # Check if Employee id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Employee WHERE EmpID = %s"
            cursor.execute(check_sql, (emp_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = "CALL spDeleteEmployee(%s)"
                cursor.execute(sql, (emp_id,))
                connection.commit()

                return {"message": f"Employee with ID '{emp_id}' deleted successfully"}
            else:
                return {"error": "Employee ID not found"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# PUT request to update a employee
@app.put("/employee/update/{emp_id}")
async def update_employee(emp_id: str, employee: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            cid = employee.get("CID")
            fname = employee.get("FName")
            lname = employee.get("LName")
            isactive =  employee.get("IsActive")
            phoneno = employee.get("PhoneNumber")
            pin = employee.get("Pin")
            
            # Check if Employee id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Employee WHERE EmpID = %s"
            cursor.execute(check_sql, (emp_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = "CALL spUpdateEmployee(%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (emp_id, cid, fname, lname, isactive, phoneno,pin))
                connection.commit()

                return {"message": f"Company with ID '{emp_id}' updated successfully"}
            else:
                return {"error": "Employee ID not found"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.post("/contact-us/create")
async def create_contact(contact: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            request_id = contact.get("RequestID")
            cid = contact.get("CID")
            name = contact.get("Name")
            requestor_email = contact.get("RequestorEmail")
            concerns_questions = contact.get("ConcernsQuestions")
            phone_number = contact.get("PhoneNumber")
            status = contact.get("Status")

            # Check if request id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM ContactUS WHERE RequestID = %s"
            cursor.execute(check_sql, (request_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Request ID already exists" , "ReportID": request_id}
            else:
                sql = """
                    CALL spCreateContact(
                        %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    request_id, cid, name, requestor_email,
                    concerns_questions, phone_number, status
                ))
                connection.commit()

                return {"message": "Contact created successfully"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# Endpoint to get a contact
@app.get("/contact-us/get/{request_id}")
async def get_contact(request_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetContact(%s);"
            cursor.execute(sql, (request_id,))
            contact = cursor.fetchall()
            if contact:
                return contact
            else:
                return {"error": "Request id not found", "RequestID": request_id}
            
    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# Endpoint to update a contact
@app.put("/contact-us/update/{request_id}")
async def update_contact(request_id : str, contact: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            
            cid = contact.get("CID")
            name = contact.get("Name")
            requestor_email = contact.get("RequestorEmail")
            concerns_questions = contact.get("ConcernsQuestions")
            phone_number = contact.get("PhoneNumber")
            status = contact.get("Status")

            # Check if request id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM ContactUS WHERE RequestID = %s"
            cursor.execute(check_sql, (request_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = """
                    CALL spUpdateContact(
                        %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    request_id, cid, name, requestor_email,
                    concerns_questions, phone_number, status
                ))
                connection.commit()  # Commit changes

                return {"message": "Contact updated successfully"}
            
            else:
                return {"error": "Request ID not found" , "ReportID": request_id}
           

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# Endpoint to delete a contact
@app.delete("/contact-us/delete/{request_id}")
async def delete_contact(request_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Check if request id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM ContactUS WHERE RequestID = %s"
            cursor.execute(check_sql, (request_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = "CALL spDeleteContact(%s);"
                cursor.execute(sql, (request_id,))
                connection.commit()  # Commit changes

                return {"message": "Contact deleted successfully"}
            else:
                return {"error": "Request ID not found" , "ReportID": request_id}  

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.post("/report-recipient/create")
async def create_report_recipient(report_recipient: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            checkin_id = report_recipient.get("CheckinID")
            cid = report_recipient.get("CID")
            email_id = report_recipient.get("EmailId")
            exec_flag = report_recipient.get("Exec")

            check_sql = "SELECT COUNT(*) AS count FROM ReportRecipients WHERE CheckinID = %s"
            cursor.execute(check_sql, (checkin_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Check-in id already exists", "CheckinID": checkin_id}
            else:
                sql = "CALL spCreateReportRecipient(%s, %s, %s, %s)"
                cursor.execute(sql, (checkin_id, cid, email_id, exec_flag))
                connection.commit()

                return {"message": "Report recipient created successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/report-recipient/get/{checkin_id}")
def get_report_recipient(checkin_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}
    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetReportRecipient(%s)'
            cursor.execute(sql, (checkin_id,))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"message": f"Report recipient with checkin ID '{checkin_id}' not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.put("/report-recipient/update/{checkin_id}")
def update_report_recipient(checkin_id: str, report_recipient: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            cid = report_recipient.get("CID")
            email_id = report_recipient.get("EmailId")
            exec_flag = report_recipient.get("Exec")

            check_sql = "SELECT COUNT(*) AS count FROM ReportRecipients WHERE CheckinID = %s"
            cursor.execute(check_sql, (checkin_id,))
            result = cursor.fetchone()
            if result['count'] > 0:

                sql = 'CALL spUpdateReportRecipient(%s, %s, %s, %s)'
                cursor.execute(sql, (checkin_id, cid, email_id, exec_flag))
                connection.commit() 

                return {"message": "Report recipient updated successfully"}
            else:
                return {"error": "Check-in id not found", "CheckinID": checkin_id}
            
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.delete("/report-recipient/delete/{checkin_id}")
def delete_report_recipient(checkin_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM ReportRecipients WHERE CheckinID = %s"
            cursor.execute(check_sql, (checkin_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = 'CALL spDeleteReportRecipient(%s)'
                cursor.execute(sql, (checkin_id,))
                connection.commit()  # Commit changes

                return {"message": f"Report recipient with checkin ID '{checkin_id}' deleted successfully"}
            else:
                return {"error": "Check-in id not found", "CheckinID": checkin_id}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.post("/checkin-type/create")
async def create_checkin_type(checkin_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            
            type_id = checkin_type.get("TypeID")
            cid = checkin_type.get("CID")
            type_names = checkin_type.get("TypeNames")

            check_sql = "SELECT COUNT(*) AS count FROM CheckInType WHERE TypeID = %s"
            cursor.execute(check_sql, (type_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Check-in Type Id already exists", "TypeID": type_id}
            else:
                sql = "CALL spCreateCheckInType(%s, %s, %s)"
                cursor.execute(sql, (type_id, cid, type_names))
                connection.commit()

                return {"message": "Check-in type created successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/checkin-type/get/{type_id}")
def get_checkin_type(type_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}
    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetCheckInType(%s)'
            cursor.execute(sql, (type_id,))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"message": f"Check-in type with ID '{type_id}' not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.put("/checkin-type/update/{type_id}")
def update_checkin_type(type_id: str, checkin_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            cid = checkin_type.get("CID")
            type_names = checkin_type.get("TypeNames")

            check_sql = "SELECT COUNT(*) AS count FROM CheckInType WHERE TypeID = %s"
            cursor.execute(check_sql, (type_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = 'CALL spUpdateCheckInType(%s, %s, %s)'
                cursor.execute(sql, (type_id, cid, type_names))
                connection.commit()  # Commit changes

                return {"message": "Check-in type updated successfully"}
            else:
                return {"error": "Check-in Type Id not found", "TypeID": type_id}
            
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.delete("/checkin-type/delete/{type_id}")
def delete_checkin_type(type_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM CheckInType WHERE TypeID = %s"
            cursor.execute(check_sql, (type_id,))
            result = cursor.fetchone()
            if result['count'] > 0:

                sql = 'CALL spDeleteCheckInType(%s)'
                cursor.execute(sql, (type_id,))
                connection.commit()  # Commit changes

                return {"message": f"Check-in type with ID '{type_id}' deleted successfully"}
            else:
                return {"error": "Check-in Type Id not found", "TypeID": type_id}
            
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/report-type/get/{report_type_id}")
def get_report_type(report_type_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}
    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetReportType(%s)'
            cursor.execute(sql, (report_type_id,))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"message": f"Report type with ID '{report_type_id}' not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.post("/report-type/create")
def create_report_type( report_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            report_type_id = report_type.get("ReportTypeID")
            report_type_name = report_type.get("ReportTypeName")
            
            check_sql = "SELECT COUNT(*) AS count FROM ReportType WHERE ReportTypeID = %s"
            cursor.execute(check_sql, (report_type_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Report Type ID already exists", "ReportTypeID": report_type_id}
            else:
                sql = 'CALL spCreateReportType(%s, %s)'
                cursor.execute(sql, (report_type_id, report_type_name))
                connection.commit()
                return {"message": "Report type updated successfully"}
            
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.put("/report-type/update/{report_type_id}")
def update_report_type(report_type_id: str, report_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            report_type_name = report_type.get("reporttypename")
            check_sql = "SELECT COUNT(*) AS count FROM ReportType WHERE ReportTypeID = %s"
            cursor.execute(check_sql, (report_type_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = 'CALL spUpdateReportType(%s, %s)'
                cursor.execute(sql, (report_type_id, report_type_name))
                connection.commit()  # Commit changes

                return {"message": "Report type updated successfully"}
            else:
                return {"error": "Report Type ID not found", "ReportTypeID": report_type_id}
          
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.delete("/report-type/delete/{report_type_id}")
def delete_report_type(report_type_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM ReportType WHERE ReportTypeID = %s"
            cursor.execute(check_sql, (report_type_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = 'CALL spDeleteReportType(%s)'
                cursor.execute(sql, (report_type_id,))
                connection.commit()  # Commit changes

                return {"message": f"Report type with ID '{report_type_id}' deleted successfully"}
            else:
                return {"error": "Report Type ID not found", "ReportTypeID": report_type_id}
          
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.post("/company-report-type/create")
async def company_create_report_type(company_report_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            
            company_reporter_email = company_report_type.get("CompanyReporterEmail")
            cid = company_report_type.get("CID")
            company_isdailyreportactive = company_report_type.get("IsDailyReportActive")
            company_isweeklyreportactive = company_report_type.get("IsWeeklyReportActive")
            company_isbiweeklyreportactive = company_report_type.get("IsBiWeeklyReportActive")
            company_ismonthlyreportactive = company_report_type.get("IsMonthlyReportActive")
            company_isbimonthlyreportactive = company_report_type.get("IsBiMonthlyReportActive")
            
            check_sql = "SELECT COUNT(*) AS count FROM CompanyReportType WHERE CompanyReporterEmail = %s AND CID = %s"
            cursor.execute(check_sql, (company_reporter_email,cid))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "company Report Email already exists", "CompanyReportEmail": company_reporter_email}
            else:
                sql = "CALL spCreateCompanyReportType(%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (company_reporter_email, cid, company_isdailyreportactive, company_isweeklyreportactive, company_isbiweeklyreportactive, company_ismonthlyreportactive, company_isbimonthlyreportactive))
                connection.commit()
                return {"message": "Company Report Email ID with data created successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/company-report-type/getAllReportEmail/{cid}")
def get_report_type(cid: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}
    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetAllCompanyReportType(%s)'
            cursor.execute(sql, (cid,))
            myresult = cursor.fetchall()
            if myresult:
                return myresult
            else:
                return {"error": f"Company Report type with ID '{cid}' not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/company-report-type/get/{company_reporter_email}/{cid}")
def get_report_type(company_reporter_email: str, cid : str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}
    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetCompanyReportType(%s, %s)'
            cursor.execute(sql, (company_reporter_email,cid))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"error": f"Report type with Email '{company_reporter_email}' not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.put("/company-report-type/update/{company_reporteremail}/{cid}")
def update_report_type(company_reporteremail: str, cid: str, company_report_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            company_isdailyreportactive = company_report_type.get("IsDailyReportActive")
            company_isweeklyreportactive = company_report_type.get("IsWeeklyReportActive")
            company_isbiweeklyreportactive = company_report_type.get("IsBiWeeklyReportActive")
            company_ismonthlyreportactive = company_report_type.get("IsMonthlyReportActive")
            company_isbimonthlyreportactive = company_report_type.get("IsBiMonthlyReportActive")
            
            check_sql = "SELECT COUNT(*) AS count FROM CompanyReportType WHERE CompanyReporterEmail = %s AND CID = %s"
            cursor.execute(check_sql, (company_reporteremail,cid))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = 'CALL spUpdateCompanyReportType(%s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(sql, (company_reporteremail, cid , company_isdailyreportactive, company_isweeklyreportactive, company_isbiweeklyreportactive, company_ismonthlyreportactive, company_isbimonthlyreportactive))
                connection.commit()  # Commit changes
                return {"message": "Company Report Email updated successfully"}
            else:
                 return {"error": "company Report Email Id not found", "CompanyReportEmailID": company_reporteremail}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.delete("/company-report-type/delete/{company_reporteremail}/{cid}")
def delete_report_type(company_reporteremail: str, cid: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM CompanyReportType WHERE CompanyReporterEmail = %s AND CID = %s"
            cursor.execute(check_sql, (company_reporteremail,cid))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = 'CALL spDeleteCompanyReportType(%s, %s)'
                cursor.execute(sql, (company_reporteremail,cid))
                connection.commit()  # Commit changes

                return {"message": f"Report type with Email '{company_reporteremail}' deleted successfully"}
            else:
                 return {"error": "company Report Type Email not found", "CompanyReportEmail": company_reporteremail}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.post("/report-schedules/create")
async def create_report_schedule(report_schedule_data: dict = Body(...)):

    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        
        report_id = report_schedule_data.get("ReportID")
        cid = report_schedule_data.get("CID")
        report_type_id = report_schedule_data.get("ReportTypeID") 
        is_delivered = report_schedule_data.get("IsDelivered") 
        is_active = report_schedule_data.get("IsActive") 
        report_time_generated = report_schedule_data.get("ReportTimeGenerated") 
        report_time_sent = report_schedule_data.get("ReportTimeSent")
        text_report_time = report_schedule_data.get("TextReportTime") 
        created_at = report_schedule_data.get("CreatedAt") 
        updated_at = report_schedule_data.get("UpdatedAt")  

        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM ReportSchedule WHERE ReportID = %s"
            cursor.execute(check_sql, (report_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Report schedule Report id already exists", "ReportID": report_id}
            else:
                sql = """
                    CALL spCreateReportSchedule(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (report_id, cid, report_type_id, is_delivered, is_active,
                                    report_time_generated, report_time_sent, text_report_time, created_at, updated_at))
                connection.commit()

                return {"message": "Report schedule created successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)} 

    finally:
        connection.close()

@app.put("/report-schedules/update/{reportid},{cid}")
async def update_report_schedule(reportid: str ,
                                 cid: str,
                                 update_data: dict = Body(...)):

    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        report_type_id = update_data.get("ReportTypeID") 
        is_delivered = update_data.get("IsDelivered") 
        is_active = update_data.get("IsActive") 
        report_time_generated = update_data.get("ReportTimeGenerated") 
        report_time_sent = update_data.get("ReportTimeSent")
        text_report_time = update_data.get("TextReportTime") 
        created_at = update_data.get("CreatedAt") 
        updated_at = update_data.get("UpdatedAt")

        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM ReportSchedule WHERE ReportID = %s"
            cursor.execute(check_sql, (reportid,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                sql = """
                    CALL spUpdateReportSchedule(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (reportid, cid, report_type_id, is_delivered, is_active,
                                    report_time_generated, report_time_sent, text_report_time, created_at, updated_at))
                connection.commit()

                return {"message": "Report schedule updated successfully"}
            else:
                return {"error": "Report schedule Report id not found", "ReportID": reportid}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}

    finally:
        connection.close()

@app.delete("/report-schedules/delete/{reportid},{cid}")
async def delete_report_schedule(reportid: str,
                                 cid: str):


    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM ReportSchedule WHERE ReportID = %s"
            cursor.execute(check_sql, (reportid,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                sql = "CALL spDeleteReportSchedule(%s, %s)"
                cursor.execute(sql, (reportid, cid))
                connection.commit()

                return  {"message": "Report schedule deleted successfully"} 
            else:
                return {"error": "Report schedule Report id not found", "ReportID": reportid}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    
    finally:
        connection.close()

@app.get("/report-schedules/get/{reportid},{cid}", response_model=dict)
async def get_report_schedule(reportid: str ,
                              cid: str ):


    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"},

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetReportSchedule(%s, %s)"
            cursor.execute(sql, (reportid, cid))
            myresult = cursor.fetchone()  

            if myresult:
                return myresult
            else:
                return {"message": f"Report schedule with ID '{reportid}' and company ID '{cid}' not found"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}

    finally:
        connection.close()

#getting the transaction Status

@app.get("/transaction/get/{transaction_id}")
async def get_transaction(transaction_id: str):
  connection = connect_to_database()
  if not connection:
      return {"error": "Failed to connect to database"}

  try:
      with connection.cursor() as mycursor:
          sql = "CALL spGetTransactionStatus(%s);"
          mycursor.execute(sql, (transaction_id,))
          transaction = mycursor.fetchone()  # Fetch only one row (if found)
          if transaction:
              return transaction
          else:
              return {"message": f"Transaction with ID '{transaction_id}' not found"}

  except pymysql.Error as err:
      print(f"Error calling stored procedure: {err}")
      return {"error": str(err)}
  finally:
      connection.close()

# Creating transaction status
@app.post("/transaction/create")
async def create_transaction(transaction: dict = Body(...)):
  connection = connect_to_database()
  if not connection:
      return {"error": "Failed to connect to database"}

  try:
      with connection.cursor() as mycursor:
          # Extract data from request body
          TransactionID = transaction.get("TransactionID")
          CID = transaction.get("CID")
          UserName = transaction.get("UserName")
          CreditCardEncrypted = transaction.get("CreditCardEncrypted")
          ExpiryDate = transaction.get("ExpiryDate")  
          CVV = transaction.get("CVV")
          TransactionAmount = transaction.get("TransactionAmount")
          TransactionStartTime = transaction.get("TransactionStartTime")  
          TransactionEndTime = transaction.get("TransactionEndTime")  
          TransactionStatus = transaction.get("TransactionStatus")
          BillingAddress = transaction.get("BillingAddress")

          check_sql = "SELECT COUNT(*) AS count FROM TransactionStatus WHERE TransactionID = %s"
          mycursor.execute(check_sql,(TransactionID))
          result = mycursor.fetchone()
          if result['count'] > 0:
            return {"error": "Transaction Id already exists", "TransactionID": TransactionID}
          else:
            # Call the stored procedure
            sql = "CALL spCreateTransactionStatus(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, (TransactionID, CID, UserName, CreditCardEncrypted, ExpiryDate, CVV, TransactionAmount, TransactionStartTime, TransactionEndTime, TransactionStatus, BillingAddress))
            connection.commit() 

            return {"message": "Transaction created successfully"}

  except pymysql.Error as err:
      print(f"Error calling stored procedure: {err}")
      return {"error": str(err)}
  finally:
      connection.close()

# updating the transaction status 
@app.put("/transaction/update/{transaction_id}")
async def update_transaction(transaction_id: str, transaction: dict = Body(...)):
  connection = connect_to_database()
  if not connection:
      return {"error": "Failed to connect to database"}

  try:
      with connection.cursor() as mycursor:
          # Extract data from request body and path parameter
          CID = transaction.get("CID")
          UserName = transaction.get("UserName")
          CreditCardEncrypted = transaction.get("CreditCardEncrypted")
          ExpiryDate = transaction.get("ExpiryDate")  # Assuming a valid date format
          CVV = transaction.get("CVV")
          TransactionAmount = transaction.get("TransactionAmount")
          TransactionStartTime = transaction.get("TransactionStartTime")  # Assuming a valid datetime format
          TransactionEndTime = transaction.get("TransactionEndTime")  # Assuming a valid datetime format
          TransactionStatus = transaction.get("TransactionStatus")
          BillingAddress = transaction.get("BillingAddress")

          # Call the stored procedure
          check_sql = "SELECT COUNT(*) AS count FROM TransactionStatus WHERE TransactionID = %s"
          mycursor.execute(check_sql,(transaction_id))
          result = mycursor.fetchone()
          if result['count'] > 0:
              sql = "CALL spUpdateTransactionStatus(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
              mycursor.execute(sql, (transaction_id, CID, UserName, CreditCardEncrypted, ExpiryDate, CVV, TransactionAmount, TransactionStartTime, TransactionEndTime, TransactionStatus, BillingAddress))
              connection.commit()  # Commit changes

              return {"message": f"Transaction with ID '{transaction_id}' updated successfully"}
          else:
              return {"error":"Transaction Id not found", "TransactionID": transaction_id}
  

  except pymysql.Error as err:
      print(f"Error calling stored procedure: {err}")
      return {"error": str(err)}
  finally:
      connection.close()

# deleting the transaction status 
@app.delete("/transaction/delete/{transaction_id}")
async def delete_transaction(transaction_id: str):
  connection = connect_to_database()
  if not connection:
      return {"error": "Failed to connect to database"}

  try:
      with connection.cursor() as mycursor:
          
          check_sql = "SELECT COUNT(*) AS count FROM TransactionStatus WHERE TransactionID = %s"
          mycursor.execute(check_sql,(transaction_id))
          result = mycursor.fetchone()
          if result['count'] > 0:
          # Call the stored procedure
            sql = "CALL spDeleteTransactionStatus(%s);"
            mycursor.execute(sql, (transaction_id,))
            connection.commit()  # Commit changes

            return {"message": f"Transaction with ID '{transaction_id}' deleted successfully"}
          else:
              return {"error": "Transaction Id not found", "TransactionID": transaction_id}

  except pymysql.Error as err:
      print(f"Error calling stored procedure: {err}")
      return {"error": str(err)}
  finally:
      connection.close()

@app.post("/dailyreport/create")
async def create_daily_report(report: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            emp_id = report.get("EmpID")
            cid = report.get("CID")
            report_date = report.get("Date")
            type_id = report.get("TypeID")
            check_in_snap = report.get("CheckInSnap")
            check_in_time = report.get("CheckInTime")
            check_out_snap = report.get("CheckOutSnap")
            check_out_time = report.get("CheckOutTime")
            time_worked = report.get("TimeWorked")

            check_sql = "SELECT COUNT(*) AS count FROM DailyReportTable WHERE EmpID = %s AND CID = %s AND CheckInTime = %s"
            cursor.execute(check_sql,(emp_id, cid, check_in_time))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Employee Id already exists", "EmpID": emp_id}
            else:
                sql = """
                    CALL spCreateDailyReport(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    emp_id, cid, type_id, check_in_snap,
                    check_in_time, check_out_snap, check_out_time,
                    time_worked, report_date
                ))
                connection.commit()  # Commit changes

                return {"message": "Daily report created successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# Endpoint to get a daily report
@app.get("/dailyreport/get/{emp_id}/{cid}/{CheckInTime}")
async def get_daily_report(emp_id: str, cid: str, CheckInTime: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetDailyReport(%s, %s, %s);"
            cursor.execute(sql, (emp_id, cid, CheckInTime))
            report = cursor.fetchall()
            if report:
                return report
            else:
                return {"error" : f"Daily report for EmpID '{emp_id}', CID '{cid}' on '{CheckInTime}' not found"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# Endpoint to update a daily report
@app.put("/dailyreport/update/{emp_id}/{cid}/{CheckInTime}")
async def update_daily_report(emp_id: str,cid: str, CheckInTime: str, report: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            
            type_id = report.get("TypeID")
            current_date = report.get("Date")
            check_in_snap = report.get("CheckInSnap")
            check_out_snap = report.get("CheckOutSnap")
            check_out_time = report.get("CheckOutTime")
            time_worked = report.get("TimeWorked")

            check_sql = "SELECT COUNT(*) AS count FROM DailyReportTable WHERE EmpID = %s AND CID = %s AND CheckInTime = %s"
            cursor.execute(check_sql,(emp_id, cid, CheckInTime))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = """
                    CALL spUpdateDailyReport(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    emp_id, cid, current_date, type_id, check_in_snap, CheckInTime,
                    check_out_snap, check_out_time,
                    time_worked
                ))
                connection.commit() 

                return {"message": "Daily report updated successfully"}
            else:
                return {"error": "Employee Id not found", "EmpID": emp_id}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# Endpoint to delete a daily report
@app.delete("/dailyreport/delete/{emp_id}/{cid}/{checkinTime}")
async def delete_daily_report(emp_id: str, cid: str, checkinTime: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            check_sql = "SELECT COUNT(*) AS count FROM DailyReportTable WHERE EmpID = %s AND CID = %s AND CheckInTime = %s"
            cursor.execute(check_sql,(emp_id, cid, checkinTime))
            result = cursor.fetchone()
            if result['count'] > 0:

                sql = "CALL spDeleteDailyReport(%s, %s, %s);"
                cursor.execute(sql, (emp_id, cid, checkinTime))
                connection.commit()

                return {"message": "Daily report deleted successfully"}
            else:
                return {"error": "Employee Id not found", "EmpID": emp_id}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


@app.get("/dailyreport/getdatebasedata/{date_value}")
async def get_employee(date_value: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetEmployeeDailyReport(%s);"
            mycursor.execute(sql, (date_value,))  # Enclose emp_id in a tuple
            daily_report = mycursor.fetchall()
            if daily_report:
                return daily_report
            else:
                return {"error": f"Daily report '{date_value}' not found"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


@app.get("/dailyReport/getDateRangeReport/{cid}/{startDate}/{endDate}")
def get_daily_report_from(cid: str, startDate: str,endDate: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetCompanyDailyReportFromRange(%s, %s, %s);'
            cursor.execute(sql, (cid,startDate,endDate))
            myresult = cursor.fetchall()
            if myresult:
                return myresult
            else:
                return {"error": f"Report for comany with ID '{cid}' for given  not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/dailyreport/get/{emp_id}/{date_value}")
async def get_employee_report(emp_id : str , date_value: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetEmployeeDailyBasisReport(%s, %s);"
            mycursor.execute(sql, (emp_id, date_value,))  # Enclose emp_id in a tuple
            daily_report = mycursor.fetchall()
            if daily_report:
                return daily_report
            else:
                return {"error": f"Daily report '{date_value}' not found"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


@app.get("/device/getAll/{cid}")
def get_all_devices(cid: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetAllDevices(%s);'
            cursor.execute(sql, (cid))
            myresult = cursor.fetchall()
            if myresult:
                return myresult
            else:
                return {"error": f"No devices found !"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


@app.get("/device/getAllDevices")
def get_all_devices_wobased_on_cid():
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetAllDevicesWithoutBasedOnCID();'
            cursor.execute(sql)
            myresult = cursor.fetchall()
            if myresult:
                return myresult
            else:
                return {"error": f"No devices found !"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


# POST request to create a device
@app.post("/device/create")
async def create_device(device: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            timezone = device.get("TimeZone") 
            device_id = device.get("DeviceID")  # Assuming "deviceID" is the key in the request body
            cid = device.get("CID")
            device_name = device.get("DeviceName")
            access_key = device.get("AccessKey")
            access_key_created_datetime = device.get("AccessKeyCreatedDateTime")

            # Execute the stored procedure
            sql = "CALL spCreateDevice(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (timezone, device_id, cid, device_name, access_key, access_key_created_datetime))
            connection.commit()

            return {"message": "Device created successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()




# DELETE request to delete a Device
@app.delete("/device/delete/{access_key}/{cid}")
async def delete_device(access_key: str, cid: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            # Check if device is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Device WHERE AccessKey = %s AND CID = %s"
            cursor.execute(check_sql, (access_key, cid))
            result = cursor.fetchone()
        
            if result['count'] > 0:
                sql = "CALL spDeleteDevice(%s, %s);"  # Using positional parameter here
                cursor.execute(sql, (access_key, cid))
                connection.commit()  # Commit changes

                return {"message": f"Device with Access Key '{access_key}' deleted successfully"}
            else:
                return {"error": "Device not found"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# Endpoint to update a daily report
@app.put("/device/update/{access_key}/{cid}")
async def update_daily_report(access_key: str,cid: str, device: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            timezone = device.get("TimeZone") 
            device_id = device.get("DeviceID")
            device_name = device.get("DeviceName")
            access_key_created_datetime = device.get("AccessKeyCreatedDateTime")


            check_sql = "SELECT COUNT(*) AS count FROM Device WHERE AccessKey = %s AND CID = %s"
            cursor.execute(check_sql,(access_key, cid))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = """
                    CALL spUpdateDevice(
                        %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    timezone, device_id, cid, device_name, access_key, access_key_created_datetime
                ))
                connection.commit() 

                return {"message": "Device updated successfully"}
            else:
                return {"error": "Access key not found", "AccessKey": access_key}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


handler=mangum.Mangum(app)