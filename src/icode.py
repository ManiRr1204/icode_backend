from fastapi import FastAPI, Body
import mangum
import pymysql

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "http://localhost:5500",  
#     "https://your-production-domain.com"  
# ]

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials = True, allow_methods=["*"], allow_headers=["*"]
)

def connect_to_database():
    try:
        connection = pymysql.connect(
            host="mydb.cxms2oikutcu.us-west-2.rds.amazonaws.com",
            user="admin",
            password="databasepass",
            database="icodeTest",
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
            sql = 'CALL get_all_companies'
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
            sql = 'CALL get_company(%s)'
            cursor.execute(sql, (company_id,))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"message": f"Company with ID '{company_id}' not found"}
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
            cid = company.get("cid")
            cname = company.get("cname")
            clogo = company.get("clogo")  # Assuming clogo is a byte stream
            caddress = company.get("caddress")
            username = company.get("username")
            password = company.get("password")

            sql = "CALL CreateCompany(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (cid, cname, clogo, caddress, username, password))
            connection.commit()  # Commit changes

            return {"message": "Company created successfully"}

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
            sql = "CALL delete_company(%s)"
            cursor.execute(sql, (company_id,))
            connection.commit()  # Commit changes

            return {"message": f"Company with ID '{company_id}' deleted successfully"}

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
        with connection.cursor() as mycursor:
            # Extract data from request body and path parameter
            cid = company_id
            cname = company.get("cname")
            clogo = company.get("clogo")  # Assuming clogo is a byte stream
            caddress = company.get("caddress")
            username = company.get("username")
            password = company.get("password")

            sql = "CALL update_company(%s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, ( cname, clogo, caddress, username, password, cid))

            connection.commit()

            return {"message": f"Company with ID '{company_id}' updated successfully"}

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
            sql = "CALL GetCustomer(%s)" 
            mycursor.execute(sql, (customer_id,))
            customer = mycursor.fetchone()
            if customer:
                return customer
            else:
                return {"message": f"Customer with ID '{customer_id}' not found"}

    except pymysql.connector.Error as err:
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
        with connection.cursor() as mycursor:
            # Extract data from request body (assuming it matches stored procedure parameters)

            sql = "CALL CreateCustomer(%(customerid)s, %(cid)s, %(fname)s, %(lname)s, %(address)s, %(phonenumber)s, %(centername)s, %(email)s, %(isactive)s)"
            mycursor.execute(sql, customer)
            connection.commit()

            return {"message": "Customer created successfully"}

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
        with connection.cursor() as mycursor:
            sql = "CALL DeleteCustomer(%s)"
            mycursor.execute(sql, (customer_id,))
            connection.commit()

            return {"message": f"Customer with ID '{customer_id}' deleted successfully"}

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
        with connection.cursor() as mycursor:

            sql = "CALL UpdateCustomer(%(customerid)s, %(cid)s, %(fname)s, %(lname)s, %(address)s, %(phonenumber)s, %(centername)s, %(email)s, %(isactive)s)"
            mycursor.execute(sql, customer)
            connection.commit()  # Commit changes

            return {"message": f"Customer with ID '{customer_id}' updated successfully"}

    except pymysql.connector.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/login/get/{username}")
async def get_login(username: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL GetLogin(%s);"
            mycursor.execute(sql, (username,)) 
            myresult = mycursor.fetchall()
            if myresult:
                return myresult
            else:
                return {"message": f"Username '{username}' not found"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


# POST request to create a employee
@app.post("/login/create")
async def create_login(login: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            # Extract data from request body
            username = login.get("username")
            cid = login.get("cid")
            password = login.get("password")  

            sql = "CALL CreateLogin(%s, %s, %s);"
            mycursor.execute(sql, (username, cid, password))
            connection.commit()  
            return {"message": "Login created successfully"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a company
@app.delete("/login/delete/{username}")
async def delete_login(username: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL DeleteLogin(%s)"

            mycursor.execute(sql, (username,))
            connection.commit()

            return {"message": f"login with ID '{username}' deleted successfully"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# PUT request to update a employee
@app.put("/login/update/{username}")
async def update_login(username: str, login: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            # Extract data from request body and path parameter
            username = login.get("username")
            cid = login.get("cid")
            password = login.get("password")  

            sql = "CALL UpdateLogin(%s, %s, %s)"
            mycursor.execute(sql, (username, cid, password))
            connection.commit()

            return {"message": f"Login with ID '{username}' updated successfully"}

    except pymysql.Error as err:
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
            sql = "CALL GetDeviceSetting(%s, %s);"
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
        with connection.cursor() as mycursor:
            # Extract data from request body
            deviceid = deviceSetting.get("deviceid")
            cid = deviceSetting.get("cid")
            devicename = deviceSetting.get("devicename")  # Assuming clogo is a byte stream
            regid = deviceSetting.get("regid")
            isactive =  bool(deviceSetting.get("isactive").lower())

            # Call the stored procedure
            sql = "CALL CreateDeviceSetting(%s, %s, %s, %s, %s);"
            mycursor.execute(sql, (deviceid, cid, devicename, regid, isactive))
            connection.commit()  # Commit changes

            return {"message": "deviceSetting created successfully"}

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
        with connection.cursor() as mycursor:
            sql = "CALL DeleteDeviceSetting(%s,%s)"

            mycursor.execute(sql, (deviceId,companyId,))
            connection.commit()

            return {"message": f"deviceSetting with ID '{deviceId}' deleted successfully"}

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
        with connection.cursor() as mycursor:
            # Extract data from request body and path parameter
            deviceid = deviceSetting.get("deviceid")
            cid = deviceSetting.get("cid")
            devicename = deviceSetting.get("devicename") 
            regid = deviceSetting.get("regid")
            isactive =  bool(deviceSetting.get("isactive").lower())

            sql = "CALL UpdateDeviceSetting(%s, %s, %s, %s, %s)"
            mycursor.execute(sql, (deviceid, cid, devicename, regid, isactive))
            connection.commit()

            return {"message": f"deviceSetting with ID '{deviceId}' updated successfully"}

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
            sql = "CALL GetEmployee(%s);"
            mycursor.execute(sql, (emp_id,))  # Enclose emp_id in a tuple
            employee = mycursor.fetchall()
            if employee:
                return employee
            else:
                return {"message": f"Employee with ID '{emp_id}' not found"}

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
        with connection.cursor() as mycursor:
            # Extract data from request body
            empid = employee.get("empid")
            cid = employee.get("cid")
            fname = employee.get("fname")  # Assuming clogo is a byte stream
            lname = employee.get("lname")
            isactive =  bool(employee.get("isactive").lower())
            phoneno = employee.get("phoneno")
            pin = employee.get("pin")

            # Call the stored procedure
            sql = "CALL CreateEmployee(%s, %s, %s, %s, %s, %s, %s);"
            mycursor.execute(sql, (empid, cid, fname, lname, isactive, phoneno,pin))
            connection.commit()  # Commit changes

            return {"message": "Company created successfully"}

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
        with connection.cursor() as mycursor:
            sql = "CALL DeleteEmployee(%s)"

            mycursor.execute(sql, (emp_id,))
            connection.commit()

            return {"message": f"employee with ID '{emp_id}' deleted successfully"}

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
        with connection.cursor() as mycursor:
            # Extract data from request body and path parameter
            empid = employee.get("empid")
            cid = employee.get("cid")
            fname = employee.get("fname")  # Assuming clogo is a byte stream
            lname = employee.get("lname")
            isactive =  bool(employee.get("isactive").lower())
            phoneno = employee.get("phoneno")
            pin = employee.get("pin")

            sql = "CALL UpdateEmployee(%s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, (empid, cid, fname, lname, isactive, phoneno,pin))
            connection.commit()

            return {"message": f"Company with ID '{emp_id}' updated successfully"}

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
            # Extract data from request body
            checkin_id = report_recipient.get("checkinid")
            cid = report_recipient.get("cid")
            email_id = report_recipient.get("emailid")
            exec_flag = report_recipient.get("exec")

            sql = "CALL CreateReportRecipient(%s, %s, %s, %s)"
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
            sql = 'CALL GetReportRecipient(%s)'
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
            # Extract data from request body
            checkin_id = report_recipient.get("checkinid")
            cid = report_recipient.get("cid")
            email_id = report_recipient.get("emailid")
            exec_flag = report_recipient.get("exec")

            sql = 'CALL UpdateReportRecipient(%s, %s, %s, %s)'
            cursor.execute(sql, (checkin_id, cid, email_id, exec_flag))
            connection.commit()  # Commit changes

            return {"message": "Report recipient updated successfully"}
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
            sql = 'CALL DeleteReportRecipient(%s)'
            cursor.execute(sql, (checkin_id,))
            connection.commit()  # Commit changes

            return {"message": f"Report recipient with checkin ID '{checkin_id}' deleted successfully"}
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
            # Extract data from request body
            type_id = checkin_type.get("typeid")
            cid = checkin_type.get("cid")
            type_names = checkin_type.get("typenames")

            sql = "CALL CreateCheckInType(%s, %s, %s)"
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
            sql = 'CALL ReadCheckInType(%s)'
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
            # Extract data from request body
            cid = checkin_type.get("cid")
            type_names = checkin_type.get("typenames")

            sql = 'CALL UpdateCheckInType(%s, %s, %s)'
            cursor.execute(sql, (type_id, cid, type_names))
            connection.commit()  # Commit changes

            return {"message": "Check-in type updated successfully"}
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
            sql = 'CALL DeleteCheckInType(%s)'
            cursor.execute(sql, (type_id,))
            connection.commit()  # Commit changes

            return {"message": f"Check-in type with ID '{type_id}' deleted successfully"}
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
            sql = 'CALL GetReportType(%s)'
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

@app.put("/report-type/update/{report_type_id}")
def update_report_type(report_type_id: str, report_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            report_type_name = report_type.get("reporttypename")

            sql = 'CALL UpdateReportType(%s, %s)'
            cursor.execute(sql, (report_type_id, report_type_name))
            connection.commit()  # Commit changes

            return {"message": "Report type updated successfully"}
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
            sql = 'CALL DeleteReportType(%s)'
            cursor.execute(sql, (report_type_id,))
            connection.commit()  # Commit changes

            return {"message": f"Report type with ID '{report_type_id}' deleted successfully"}
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
            
            company_report_type_id = company_report_type.get("reporttypeid")
            cid = company_report_type.get("cid")
            report_type_id = company_report_type.get("reporttypeid")
            company_isdailyreportactive = company_report_type.get("isdailyreportactive")

            sql = "CALL CreateCompanyReportType(%s, %s, %s, %s)"
            cursor.execute(sql, (company_report_type_id, cid, report_type_id, company_isdailyreportactive))
            connection.commit()

            return {"message": "Company Report type created successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


@app.get("/company-report-type/get/{company_report_type_id}")
def get_report_type(company_report_type_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}
    try:
        with connection.cursor() as cursor:
            sql = 'CALL GetCompanyReportType(%s)'
            cursor.execute(sql, (company_report_type_id,))
            myresult = cursor.fetchone()
            if myresult:
                return myresult
            else:
                return {"message": f"Report type with ID '{company_report_type_id}' not found"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.put("/company-report-type/update/{company_report_type_id}")
def update_report_type(company_report_type_id: str, company_report_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            company_report_type_id = company_report_type.get("reporttypeid")
            cid = company_report_type.get("cid")
            report_type_id = company_report_type.get("reporttypeid")
            company_isdailyreportactive = company_report_type.get("isdailyreportactive")

            sql = 'CALL UpdateCompanyReportType(%s, %s, %s, %s)'
            cursor.execute(sql, (company_report_type_id, cid, report_type_id, company_isdailyreportactive))
            connection.commit()  # Commit changes

            return {"message": "Company Report type updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.delete("/company-report-type/delete/{company_report_type_id}")
def delete_report_type(company_report_type_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL DeleteCompanyReportType(%s)'
            cursor.execute(sql, (company_report_type_id,))
            connection.commit()  # Commit changes

            return {"message": f"Report type with ID '{company_report_type_id}' deleted successfully"}
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
        
        report_id = report_schedule_data.get("reportid")
        cid = report_schedule_data.get("cid")
        report_type_id = report_schedule_data.get("reporttypeid") 
        is_delivered = report_schedule_data.get("isdelivered") 
        is_active = report_schedule_data.get("isactive") 
        report_time_generated = report_schedule_data.get("reporttimegenerated") 
        report_time_sent = report_schedule_data.get("reporttimesent")
        text_report_time = report_schedule_data.get("textreporttime") 
        created_at = report_schedule_data.get("createdat") 
        updated_at = report_schedule_data.get("updatedat")  

        with connection.cursor() as cursor:
            
            sql = """
                CALL CreateReportSchedule(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        report_id = update_data.get("reportid")
        c_id = update_data.get("cid")
        report_type_id = update_data.get("reportypeid")
        is_delivered = update_data.get("isdelivered")  
        is_active = update_data.get("isactive")  
        report_time_generated = update_data.get("reporttimegenerated")
        report_time_sent = update_data.get("reporttimesent")
        text_report_time = update_data.get("textreporttime")
        created_at = update_data.get("createdat")
        updated_at = update_data.get("updatedat")

        with connection.cursor() as cursor:
            
            sql = """
                CALL UpdateReportSchedule(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (reportid, cid, report_type_id, is_delivered, is_active,
                                 report_time_generated, report_time_sent, text_report_time, created_at, updated_at))
            connection.commit()

            return {"message": "Report schedule updated successfully"}

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
            sql = "CALL DeleteReportSchedule(%s, %s)"
            cursor.execute(sql, (reportid, cid))
            connection.commit()

            return  {"message": "Report schedule deleted successfully"} 

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
            sql = "CALL GetReportSchedule(%s, %s)"
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


handler=mangum.Mangum(app)