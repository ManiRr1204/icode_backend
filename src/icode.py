from datetime import date
from fastapi import FastAPI, HTTPException, Body, Request
import mangum
import pymysql
import stripe
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
import yagmail

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["https://arjavatech.github.io", "http://127.0.0.1:5504", "https://arunkavitha1982.github.io/icode","*"], allow_credentials = True, allow_methods=["*"], allow_headers=["https://arjavatech.github.io", "http://127.0.0.1:5504", "https://arunkavitha1982.github.io/icode","*"]
)

sender_mail = "contact@tap-time.com"
app_passcode = "vavx hkdp rfwa wfgc"

# Initialize Stripe with your secret key
stripe.api_key = 'sk_test_51OB8JlIPoM7JHRT2Dz4UeKOU5Snexc9lFpmu2Hp6d0PfCZKCwqWE4NanolwHC5fSd5hbLwsnpHAEJphTByN5c93w00pEpp1vJt'


def connect_to_database():
    try:
        connection = pymysql.connect(
            host="taptime.ccvfbf5xwxwq.us-west-2.rds.amazonaws.com",
            user="developer",
            password="Arjavapass01#",
            database="taptimeprod",
            cursorclass=pymysql.cursors.DictCursor 
        )
        return connection
    except pymysql.MySQLError as err:
        print(f"Error connecting to database: {err}")
        return None

@app.get("/test")
def get_test():
   return {"response": "Test get call successfully called"}

@app.get("/getAppData")
def get_test():
   return {"appData": {
            "androidVersion" : "1.0.0",
            "androidAppLink": "",
            "hereForValueList" : ["Belt", "Path", "Camp", "External", "Trial", "Reception"]
        }}

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
            LastModifiedBy = company.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")


            # Check if username is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Company WHERE UserName = %s"
            cursor.execute(check_sql, (username,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "UserName already exists"}

            else:
                sql = "CALL spCreateCompany(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (cid, cname, clogo, caddress, username, password, reportType, LastModifiedBy, utc_datetime_string))
                connection.commit()

                return {"message": "Company created successfully", "CID": cid, "UserName": username}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a company
@app.put("/company/delete/{company_id}/{LastModifiedBy}")
async def delete_company(company_id: str, LastModifiedBy: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            # Check if username is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Company WHERE CID = %s"
            cursor.execute(check_sql, (company_id,))
            result = cursor.fetchone()

            if result['count'] > 0:
                sql = "CALL spDeleteCompany(%s, %s, %s)"
                cursor.execute(sql, (company_id, LastModifiedBy, utc_datetime_string))
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
            LastModifiedBy = company.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")
            
            
            check_sql = "SELECT COUNT(*) AS count FROM Company WHERE UserName = %s"
            cursor.execute(check_sql, (username))
            result = cursor.fetchone()
            if result['count'] > 0:

                check_sql_2 = "SELECT COUNT(*) AS count FROM Company WHERE UserName = %s AND CID = %s"
                cursor.execute(check_sql_2, (username, company_id))
                result_2 = cursor.fetchone()

                if result_2['count'] > 0:
                    sql = "CALL spUpdateCompany(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (company_id, cname, clogo, caddress, username, password, reportType, LastModifiedBy, utc_datetime_string))
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
async def update_report_type(company_id: str, report_type_dict: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            report_type = report_type_dict.get("report_type")
            LastModifiedBy = report_type_dict.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            # Call the stored procedure to update the ReportType
            sql = "CALL spUpdateReportType(%s, %s, %s, %s)"
            cursor.execute(sql, (company_id, report_type, LastModifiedBy, utc_datetime_string))
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
            LastModifiedBy = customer.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")
            
            check_sql = "SELECT COUNT(*) AS count FROM Customer WHERE CustomerID = %s"
            cursor.execute(check_sql, (customer_id))
            result = cursor.fetchone()

            if result['count'] > 0:
                return {"error": "Customer id already exists"}

            else:
                sql = "CALL spCreateCustomer(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (customer_id, cid, fname, lname, address, phone_number, email, is_active, LastModifiedBy, utc_datetime_string))
                connection.commit()

                return {"message": "Customer created successfully", "CustomerID": customer_id}

    except pymysql.connector.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a customer_id
@app.put("/customer/delete/{customer_id}/{LastModifiedBy}")
async def delete_customer(customer_id: str, LastModifiedBy: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            check_sql = "SELECT COUNT(*) AS count FROM Customer WHERE CustomerID = %s"
            cursor.execute(check_sql, (customer_id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                sql = "CALL spDeleteCustomer(%s, %s, %s)"
                cursor.execute(sql, (customer_id, LastModifiedBy, utc_datetime_string))
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

            customer_id = customer.get("CustomerID")
            cid = customer.get("CID")
            fname = customer.get("FName")
            lname = customer.get("LName")
            address = customer.get("Address")
            phone_number = customer.get("PhoneNumber")
            email = customer.get("Email")
            is_active = customer.get("IsActive")
            LastModifiedBy = customer.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            check_sql = "SELECT COUNT(*) AS count FROM Customer WHERE CustomerID = %s"
            cursor.execute(check_sql, (customer_id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                sql = "CALL spUpdateCustomer(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (customer_id, cid, fname, lname, address, phone_number, email, is_active, LastModifiedBy, utc_datetime_string))
                connection.commit()  # Commit changes
                return {"message": f"Customer with ID '{customer_id}' updated successfully"}
            else:
                return {"error": "Customer id not found", "CustomerID": customer_id} 

    except pymysql.connector.Error as err:
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

@app.get("/employee/getcount/{cid}")
async def get__all_employee(cid : str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetEmployeeCount(%s);"
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


@app.get("/getadmin/{cid}")
async def get__admins(cid : str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetAdmin(%s);"
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


@app.post("/employee/create")
async def create_employee(employee: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")
    
    try:
        with connection.cursor() as cursor:
            
            # Extract data from request body
            empid = employee.get("EmpID")
            cid = employee.get("CID")
            fname = employee.get("FName")
            lname = employee.get("LName")
            isactive = employee.get("IsActive")
            phoneno = employee.get("PhoneNumber")
            pin = employee.get("Pin")
            isadmin = employee.get("IsAdmin")
            LastModifiedBy = employee.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Check if employee already exists
            check_sql = "SELECT COUNT(*) AS count FROM Employee WHERE EmpID = %s"
            cursor.execute(check_sql, (empid,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                return {"error": "Employee already exists", "EmpID": empid}
            else:
                sql = "CALL spCreateEmployee(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (empid, cid, fname, lname, isactive, phoneno, pin, isadmin, LastModifiedBy, utc_datetime_string))
                connection.commit()
                return {"message": "Employee created successfully", "EmpID": empid}

    except pymysql.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        connection.close()

# DELETE request to delete a company
@app.put("/employee/delete/{emp_id}/{LastModifiedBy}")
async def delete_employee(emp_id: str, LastModifiedBy: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            # Check if Employee id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Employee WHERE EmpID = %s"
            cursor.execute(check_sql, (emp_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = "CALL spDeleteEmployee(%s, %s, %s)"
                cursor.execute(sql, (emp_id, LastModifiedBy, utc_datetime_string))
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
            isadmin = employee.get("IsAdmin")
            LastModifiedBy = employee.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Check if Employee id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Employee WHERE EmpID = %s"
            cursor.execute(check_sql, (emp_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = "CALL spUpdateEmployee(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (emp_id, cid, fname, lname, isactive, phoneno,pin, isadmin, LastModifiedBy, utc_datetime_string))
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
            LastModifiedBy = contact.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            # Check if request id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM ContactUS WHERE RequestID = %s"
            cursor.execute(check_sql, (request_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Request ID already exists" , "ReportID": request_id}
            else:
                sql = """
                    CALL spCreateContact(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    request_id, cid, name, requestor_email,
                    concerns_questions, phone_number, status, LastModifiedBy, utc_datetime_string
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
            LastModifiedBy = contact.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            # Check if request id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM ContactUS WHERE RequestID = %s"
            cursor.execute(check_sql, (request_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = """
                    CALL spUpdateContact(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    request_id, cid, name, requestor_email,
                    concerns_questions, phone_number, status, LastModifiedBy, utc_datetime_string
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
@app.put("/contact-us/delete/{request_id}/{LastModifiedBy}")
async def delete_contact(request_id: str, LastModifiedBy: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            # Check if request id is already exists
            check_sql = "SELECT COUNT(*) AS count FROM ContactUS WHERE RequestID = %s"
            cursor.execute(check_sql, (request_id,))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = "CALL spDeleteContact(%s, %s, %s);"
                cursor.execute(sql, (request_id, LastModifiedBy, utc_datetime_string))
                connection.commit()  # Commit changes

                return {"message": "Contact deleted successfully"}
            else:
                return {"error": "Request ID not found" , "ReportID": request_id}  

    except pymysql.Error as err:
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
            LastModifiedBy = company_report_type.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")
            
            check_sql = "SELECT COUNT(*) AS count FROM CompanyReportType WHERE CompanyReporterEmail = %s AND CID = %s"
            cursor.execute(check_sql, (company_reporter_email,cid))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "company Report Email already exists", "CompanyReportEmail": company_reporter_email}
            else:
                sql = "CALL spCreateCompanyReportType(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (company_reporter_email, cid, company_isdailyreportactive, company_isweeklyreportactive, company_isbiweeklyreportactive, company_ismonthlyreportactive, company_isbimonthlyreportactive, LastModifiedBy, utc_datetime_string))
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
            LastModifiedBy = company_report_type.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")
            
            check_sql = "SELECT COUNT(*) AS count FROM CompanyReportType WHERE CompanyReporterEmail = %s AND CID = %s"
            cursor.execute(check_sql, (company_reporteremail,cid))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = 'CALL spUpdateCompanyReportType(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(sql, (company_reporteremail, cid , company_isdailyreportactive, company_isweeklyreportactive, company_isbiweeklyreportactive, company_ismonthlyreportactive, company_isbimonthlyreportactive, LastModifiedBy, utc_datetime_string))
                connection.commit()  # Commit changes
                return {"message": "Company Report Email updated successfully"}
            else:
                 return {"error": "company Report Email Id not found", "CompanyReportEmailID": company_reporteremail}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.put("/company-report-type/delete/{company_reporteremail}/{cid}/{LastModifiedBy}")
def delete_report_type(company_reporteremail: str, cid: str, LastModifiedBy: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            check_sql = "SELECT COUNT(*) AS count FROM CompanyReportType WHERE CompanyReporterEmail = %s AND CID = %s"
            cursor.execute(check_sql, (company_reporteremail,cid))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = 'CALL spDeleteCompanyReportType(%s, %s, %s, %s)'
                cursor.execute(sql, (company_reporteremail,cid, LastModifiedBy, utc_datetime_string))
                connection.commit()  # Commit changes

                return {"message": f"Report type with Email '{company_reporteremail}' deleted successfully"}
            else:
                 return {"error": "company Report Type Email not found", "CompanyReportEmail": company_reporteremail}
    except pymysql.MySQLError as err:
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
            LastModifiedBy = report.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            check_sql = "SELECT COUNT(*) AS count FROM DailyReportTable WHERE EmpID = %s AND CID = %s AND CheckInTime = %s"
            cursor.execute(check_sql,(emp_id, cid, check_in_time))
            result = cursor.fetchone()
            if result['count'] > 0:
                return {"error": "Employee Id already exists", "EmpID": emp_id}
            else:
                sql = """
                    CALL spCreateDailyReport(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    emp_id, cid, type_id, check_in_snap,
                    check_in_time, check_out_snap, check_out_time,
                    time_worked, report_date, LastModifiedBy, utc_datetime_string
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
            LastModifiedBy = report.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            check_sql = "SELECT COUNT(*) AS count FROM DailyReportTable WHERE EmpID = %s AND CID = %s AND CheckInTime = %s"
            cursor.execute(check_sql,(emp_id, cid, CheckInTime))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = """
                    CALL spUpdateDailyReport(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    emp_id, cid, current_date, type_id, check_in_snap, CheckInTime,
                    check_out_snap, check_out_time,
                    time_worked, LastModifiedBy, utc_datetime_string
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
@app.put("/dailyreport/delete/{emp_id}/{cid}/{checkinTime}/{LastModifiedBy}")
async def delete_daily_report(emp_id: str, cid: str, checkinTime: str, LastModifiedBy: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            check_sql = "SELECT COUNT(*) AS count FROM DailyReportTable WHERE EmpID = %s AND CID = %s AND CheckInTime = %s"
            cursor.execute(check_sql,(emp_id, cid, checkinTime))
            result = cursor.fetchone()
            if result['count'] > 0:

                sql = "CALL spDeleteDailyReport(%s, %s, %s, %s, %s);"
                cursor.execute(sql, (emp_id, cid, checkinTime, LastModifiedBy, utc_datetime_string))
                connection.commit()

                return {"message": "Daily report deleted successfully"}
            else:
                return {"error": "Employee Id not found", "EmpID": emp_id}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


@app.get("/dailyreport/getdatebasedata/{cid}/{date_value}")
async def get_employee(cid: str, date_value: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "CALL spGetEmployeeDailyReport(%s, %s);"
            mycursor.execute(sql, (cid, date_value,)) 
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

@app.post("/dailyReport/getDateRangeReport/{cid}")
def get_daily_report_from(cid: str, dateRange: dict= Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            startdate = dateRange.get("startdate")
            enddate = dateRange.get("enddate")
            sql = 'CALL spGetCompanyDailyReportFromRange(%s, %s, %s);'
            cursor.execute(sql, (cid,startdate,enddate))
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

@app.get("/report/dateRangeReportGet/{cid}/{startDate}/{endDate}")
async def get_date_range_report_from(cid: str, startDate: str,endDate: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s, %s);'
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


@app.post("/dailyreportBasedonCID/get/{cid}")
async def get_company_based_report(cid : str , dateRange: dict= Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            startdate = dateRange.get("startdate")
            enddate = dateRange.get("enddate")
            sql = "CALL spGetCompanyBasedDailyReport(%s, %s, %s);"
            mycursor.execute(sql, (cid, startdate, enddate))  # Enclose emp_id in a tuple
            daily_report = mycursor.fetchall()
            if daily_report:
                return daily_report
            else:
                return {"error": "Daily report not found"}

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
            time_zone = device.get("TimeZone") 
            device_id = device.get("DeviceID")
            cid = device.get("CID")
            device_name = device.get("DeviceName")
            access_key = device.get("AccessKey")
            access_key_created_datetime = device.get("AccessKeyCreatedDateTime")
            is_active = True
            LastModifiedBy = device.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            # Execute the stored procedure
            sql = "CALL spCreateDevice(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (time_zone, device_id, cid, device_name, access_key, access_key_created_datetime,is_active, LastModifiedBy, utc_datetime_string))
            connection.commit()

            return {"message": "Device created successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a Device
@app.put("/device/delete/{access_key}/{cid}/{LastModifiedBy}")
async def delete_device(access_key: str, cid: str, LastModifiedBy: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            # Check if device is already exists
            check_sql = "SELECT COUNT(*) AS count FROM Device WHERE AccessKey = %s AND CID = %s"
            cursor.execute(check_sql, (access_key, cid))
            result = cursor.fetchone()
        
            if result['count'] > 0:
                sql = "CALL spDeleteDevice(%s, %s, %s, %s);"  # Using positional parameter here
                cursor.execute(sql, (access_key, cid, LastModifiedBy, utc_datetime_string))
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
            is_active = True
            LastModifiedBy = device.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            check_sql = "SELECT COUNT(*) AS count FROM Device WHERE AccessKey = %s AND CID = %s"
            cursor.execute(check_sql,(access_key, cid))
            result = cursor.fetchone()
            if result['count'] > 0:
                sql = """
                    CALL spUpdateDevice(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                cursor.execute(sql, (
                    timezone, device_id, cid, device_name, access_key, access_key_created_datetime, is_active, LastModifiedBy, utc_datetime_string
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

@app.put("/admin-report-type/update/{cid}")
def update_report_type(cid: str, report_type: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            # Extract data from request body
            report_type_val = report_type.get("ReportType")
            LastModifiedBy = report_type.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            sql = 'CALL spUpdateAdminReportType(%s, %s, %s, %s)'
            cursor.execute(sql, (cid,report_type_val, LastModifiedBy, utc_datetime_string))
            connection.commit()

            return {"message": "Report type updated successfully"}

    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

class CheckoutRequest(BaseModel):
    url: str
    productName : str
    amount: int

@app.post('/create-checkout-session')
async def create_checkout_session(request: CheckoutRequest):
    try:
        print('Creating checkout session')
        # Create a new Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': request.productName,
                    },
                    'unit_amount': request.amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{request.url}/success.html",
            cancel_url=f"{request.url}/singup.html", 
        )
        print('Checkout session created:', session.id)
        return JSONResponse(content={'id': session.id})
    except Exception as e:
        print('Error creating checkout session:', str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report_mail_trigger")
def mail_trigger():
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        company_with_device_dict = {}
        with connection.cursor() as cursor:
            company_detail_sql = 'CALL spGetAllCompanies'
            cursor.execute(company_detail_sql)
            company_result = cursor.fetchall()
            if company_result:
                for company_details in company_result:
                    device_get_sql = 'CALL spGetAllDevices(%s);'
                    cursor.execute(device_get_sql, (company_details['CID']))
                    device_result = cursor.fetchall()

                    if device_result:
                        for device in device_result:
                            if(device["DeviceID"] != "Not Registered"):
                                company_with_device_dict[company_details['CID']] = {"Timezone" : device["TimeZone"],}                       
                                
                                report_type_sql = 'CALL spGetAllCompanyReportType(%s)'
                                cursor.execute(report_type_sql, (company_details['CID'],))
                                report_type_result = cursor.fetchall()

                                if report_type_result:
                                    # Initialize an empty dictionary for the output
                                    consolidated_output = {"Daily": [], "Weekly": [], "Monthly": [], "Bimonthly": [], "Biweekly": []}

                                    # Loop through the list of dictionaries
                                    for item in report_type_result:
                                        if item['IsDailyReportActive'] == 1:
                                            consolidated_output["Daily"].append(item['CompanyReporterEmail'])
                                        if item['IsWeeklyReportActive'] == 1:
                                            consolidated_output["Weekly"].append(item['CompanyReporterEmail'])
                                        if item['IsBiWeeklyReportActive'] == 1:
                                            consolidated_output["Biweekly"].append(item['CompanyReporterEmail'])
                                        if item['IsBiMonthlyReportActive'] == 1:
                                            consolidated_output["Bimonthly"].append(item['CompanyReporterEmail'])
                                        if item['IsMonthlyReportActive'] == 1:
                                            consolidated_output["Monthly"].append(item['CompanyReporterEmail'])

                                    company_with_device_dict[company_details['CID']]["ReportTypeList"] = consolidated_output


                for company_det in company_with_device_dict:  
                    is_monday = is_today_monday()
                    is_month_start_date = is_first_day_of_month()
                    is_second_half_of_month_start_date = is_today_in_second_half_of_month()

                    if( "ReportTypeList" in company_with_device_dict[company_det] and "Daily" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Daily"] != []):
                        today = datetime.now().date()
                        yesterday = today - timedelta(days=1)
                        sql = "CALL spGetEmployeeDailyReport(%s, %s);"
                        cursor.execute(sql, (company_det , yesterday,))  
                        daily_report = cursor.fetchall()
                        if daily_report:
                            message = create_daily_report_html_table(daily_report, yesterday)
                            to_address = company_with_device_dict[company_det]["ReportTypeList"]["Daily"]
                            sender = sender_mail
                            app_password = app_passcode
                            subject = f'{yesterday} Report Data'

                            # Initialize Yagmail with the sender's Gmail credentials
                            yag = yagmail.SMTP(user=sender, password=app_password)

                            # Sending the email
                            yag.send(to= to_address, subject=subject, contents=message, )


                    if(is_monday):
                        if("ReportTypeList" in company_with_device_dict[company_det] and "Weekly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Weekly"] != []):
                            
                            dateRange = get_last_week_date_range()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()
                            
                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Weekly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Weekly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Weekly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )


                        if("ReportTypeList" in company_with_device_dict[company_det] and "Biweekly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Biweekly"] != []):
                            dateRange = get_last_two_weeks_date_range()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()

                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Biweekly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Biweekly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Biweekly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )
                        

                    if(is_month_start_date):
                        if("ReportTypeList" in company_with_device_dict[company_det] and "Bimonthly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Bimonthly"] != []):
                            dateRange = get_bimonthly_start_and_end_dates()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()
                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Bimonthly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Bimonthly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Bimonthly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )

                        if("ReportTypeList" in company_with_device_dict[company_det] and "Monthly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Monthly"] != []):
                            dateRange = get_last_month_start_and_end_dates()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()
                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Monthly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Monthly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Monthly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )

                    if(is_second_half_of_month_start_date ):
                        if("ReportTypeList" in company_with_device_dict[company_det] and "Bimonthly" in company_with_device_dict[company_det]["ReportTypeList"] and company_with_device_dict[company_det]["ReportTypeList"]["Bimonthly"] != []):
                            dateRange = get_bimonthly_start_and_end_dates()

                            report_type_sql = 'CALL spGetCompanyDailyReportFromDateRange(%s, %s,%s)'
                            cursor.execute(report_type_sql, (company_details['CID'], dateRange["startRange"], dateRange["endRange"]))
                            report_result = cursor.fetchall()
                            if(report_result):
                                message = create_salaried_report_html_table( calculate_total_time_worked(report_result) , "Bimonthly", dateRange["startRange"], dateRange["endRange"])
                                to_address = company_with_device_dict[company_det]["ReportTypeList"]["Bimonthly"]
                                
                                sender = sender_mail
                                app_password = app_passcode
                                subject = f'Bimonthly Report Data - {dateRange["startRange"]} to {dateRange["endRange"]}'

                                # Initialize Yagmail with the sender's Gmail credentials
                                yag = yagmail.SMTP(user=sender, password=app_password)

                                # Sending the email
                                yag.send(to= to_address, subject=subject, contents=message, )
       
                return {"message" : "Output Got it!!!!!"}
            else:
                return {"message": "No one companies is registered in our app!!"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


def get_last_week_date_range(today=None):
    if today is None:
        today = datetime.now().date()

    # Monday of the current week  
    start_of_week = today - timedelta(days=today.weekday())
  
    # Last Monday
    last_monday = start_of_week - timedelta(weeks=1)
  
    # Last Sunday
    last_sunday = last_monday + timedelta(days=6)
  
    return {
        "startRange": last_monday.strftime("%Y-%m-%d"),
        "endRange": last_sunday.strftime("%Y-%m-%d")
    }

def get_last_two_weeks_date_range(today=None):
    if today is None:
        today = datetime.now().date()

    # Monday of the current week
    start_of_week = today - timedelta(days=today.weekday())
  
    # Start of the last two weeks (Monday two weeks ago)
    start_date = start_of_week - timedelta(weeks=2)
  
    # End of the last two weeks (Sunday two weeks later)
    end_date = start_date + timedelta(days=13)
  
    return {
        "startRange": start_date.strftime("%Y-%m-%d"),
        "endRange": end_date.strftime("%Y-%m-%d")
    }

def get_bimonthly_start_and_end_dates():
    today = datetime.now()   

    # Calculate the number of days in the current month
    days_in_month = (datetime(today.year, today.month + 1, 1) - timedelta(days=1)).day
    mid_month_day = (days_in_month + 1) // 2

    if today.day >= mid_month_day:
        # Second half of the month, so return the first half
        start_date = datetime(today.year, today.month, 1)
        end_date = datetime(today.year, today.month, mid_month_day - 1)
    else:
        # First half of the month, so return the second half of the previous month
        previous_month = datetime(today.year, today.month - 1, 1)
        days_in_prev_month = (datetime(previous_month.year, previous_month.month + 1, 1) - timedelta(days=1)).day
        start_date = datetime(previous_month.year, previous_month.month, (days_in_prev_month + 1) // 2)
        end_date = datetime(previous_month.year, previous_month.month, days_in_prev_month)

    return {
        'startRange': start_date.strftime('%Y-%m-%d'),
        'endRange': end_date.strftime('%Y-%m-%d')
    }

def get_last_month_start_and_end_dates(today=None):
    if today is None:
        today = datetime.now().date()

    # Start date of the last full month
    start_date_last_month = datetime(today.year, today.month - 1, 1)
  
    # End date of the last full month
    end_date_last_month = datetime(today.year, today.month, 1) - timedelta(days=1)
  
    return {
        "startRange": start_date_last_month.strftime("%Y-%m-%d"),
        "endRange": end_date_last_month.strftime("%Y-%m-%d")
    }

def is_today_monday():
    now = datetime.now()
    
    return now.weekday() == 0

def is_first_day_of_month():
    now = datetime.now()
    
    return now.day == 1

def is_today_in_second_half_of_month():
    today = datetime.now()

    next_month = today.replace(day=28) + timedelta(days=4)  # Move to next month
    last_day_of_month = next_month - timedelta(days=next_month.day)
    days_in_month = last_day_of_month.day
    
    # Determine the start date of the second half of the month
    if days_in_month in [28, 29]:
        second_half_start = 15
    else:  # 30 or 31 days
        second_half_start = 16

    second_half_start_date = today.replace(day=second_half_start, hour=0, minute=0, second=0, microsecond=0)
    
    return today >= second_half_start_date


def format_timedelta(td):
   # Convert timedelta to total minutes
    total_minutes = int(td.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)
    # Format as HH:MM
    return f"{hours:02}:{minutes:02}"

def consolitaded_result(report_result):
    print(report_result)
    formatted_result = [
        {
            # 'EmpID': item['EmpID'],
            # 'FullName': item['FullName'],
            # 'TotalTimeWorked': format_timedelta(item['TotalTimeWorked'])
            'EmpID': item['Pin'],
            'FullName': item['Name'],
            'TotalTimeWorked': item['TimeWorked']
        }
        for item in report_result
    ]

    return formatted_result


def create_salaried_report_html_table(data, reportType, startDate, endDate):
    html = f"<html><body style='text-align: center;'><h4>{reportType} Report - {startDate} to {endDate}</h4><table border='1' cellpadding='5' cellspacing='0' style='margin: 0 auto;'>"
    # Create table header
    html += "<tr><th style='text-align: center;'>Name</th><th>Pin</th><th>Total Worked Hours (HH:MM)</th></tr>"
    
    # index = 1

    # Add table rows
    for key, value in data.items():
        html += f"<tr><td style='text-align: center;'>{data[key]['name']}</td><td>{key}</td><td style='text-align: center;'>{data[key]['total_hours_worked']}</td></tr>"
        # index = index + 1
    html += "</table></body></html>"
    return html

def create_daily_report_html_table(data, date):
    html = f"<html><body style='text-align: center;'><h4>{date} Report</h4><table border='1' cellpadding='5' cellspacing='0' style='margin: 0 auto;'>"
    # Create table header
    html += "<tr><th style='text-align: center;'>S.No</th><th>Employee ID</th><th>Employee Name</th><th>Class Type</th><th>Check-In Time</th><th>Check-Out Time</th><th>TimeWorked (HH:MM)</th></tr>"
    # Add table rows
    index =1
    for item in data:
        html += f"<tr><td style='text-align: center;'>{index}</td><td style='text-align: center;'>{item['Pin']}</td><td>{item['Name']}</td><td style='text-align: center;'>{item['Type']}</td><td>{item['CheckInTime']}</td><td>{item['CheckOutTime']}</td><td style='text-align: center;'>{item['TimeWorked']}</td></tr>"
        index = index+1
    html += "</table></body></html>"
    return html

# Functions to convert time and calculate totals

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}:{str(mins).zfill(2)}"

def calculate_total_time_worked(data):
    employee_times = {}

    for entry in data:
        name = entry.get('Name')
        pin = entry.get('Pin')
        time_worked = entry.get('TimeWorked')

        if time_worked:
            minutes_worked = time_to_minutes(time_worked)

            if pin not in employee_times:
                employee_times[pin] = {'name': name, 'total_minutes': 0}

            employee_times[pin]['total_minutes'] += minutes_worked

    # Convert total minutes to time string
    for pin, details in employee_times.items():
        details['total_hours_worked'] = minutes_to_time(details['total_minutes'])

    return employee_times

@app.post("/contact/send")
async def parent_invite_create(company_details: dict=Body(...)):

    Name = company_details.get("Name")
    companyName = company_details.get("CompanyName")
    phoneNumber = company_details.get("PhoneNumber")
    email = company_details.get("email")
    street = company_details.get("street")
    state = company_details.get("state")
    zipval = company_details.get("zip")
    # Set up email parameters
    sender = sender_mail
    app_password = app_passcode
    subject = "New User Registration: Company Details Submitted for App Access"

    # Email content in HTML
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1; color: #333;">
        <p>Dear Support Team,</p>

    <p>A new user has registered and provided their company details to access our app. Below are the updated details:</p>

    <ul>
        <li><strong>Customer Name:</strong> {Name}</li>
        <li><strong>Company Name:</strong> {companyName}</li>
        <li><strong>Phone Number:</strong> {phoneNumber}</li>
        <li><strong>Email:</strong> {email}</li>
        <li><strong>Street Address:</strong> {street}</li>
        <li><strong>State:</strong> {state}</li>
        <li><strong>Zip:</strong> {zipval}</li>
    </ul>

    <p>Please reach out to the user with further instructions for completing the registration process.</p>

    <p>Best regards,<br>Tap-Time Team</p>
    </body>
    </html>
    """

    # Initialize Yagmail with the sender's Gmail credentials
    yag = yagmail.SMTP(user=sender, password=app_password)

    # Sending the email
    yag.send(to=["mani.arjava@gmail.com","nachiappan1406@gmail.com", "sivagami.arunachalam@icodeschool.com"], subject=subject, contents=html_content)

    return {"message": "Email sent successfully!"}

@app.post("/web_contact_us/create")
async def set_create_contact(contact: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            # Extract data from request body
            FirstName = contact.get("FirstName")
            LastName = contact.get("LastName")
            Email = contact.get("Email")
            WhatsappNumber = contact.get("WhatsappNumber")
            Subject = contact.get("Subject")
            phone_number = contact.get("PhoneNumber")
            Message = contact.get("Message")
            Address = contact.get("Address")
            LastModifiedBy = contact.get("LastModifiedBy")

            # Get current UTC datetime
            utc_now = datetime.now(timezone.utc)
            # Format as a string
            utc_datetime_string = utc_now.strftime("%Y-%m-%d %H:%M:%S")

            sql = """
                CALL spCreateWebsiteContactUs(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                );
            """
            cursor.execute(sql, (
                FirstName, LastName, Email, WhatsappNumber,
                Subject, phone_number, Message, Address, LastModifiedBy, utc_datetime_string
            ))
            connection.commit()

            # Set up email parameters
            sender = sender_mail
            app_password = app_passcode
            subject = "Thank You for Your Interest in Our Tap-Time Application"

            # Email content in HTML
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1; color: #333;">
                <p>Dear {FirstName+ " "+ LastName},</p>

            <p>Thank you for reaching out to us via our website’s contact form and expressing interest in our web application. We are excited to learn that you are considering our solution for your business needs.\n\nOur web app is designed to offer Employee management system, and we believe it could greatly support your goals.\n\nWe would love to discuss your requirements in more detail and provide a customized demonstration. Please let us know a convenient time for a meeting, or feel free to share more details on your expectations.\n\nLooking forward to hearing from you!</p>
            <p>Best regards,<br>Tap-Time Team</p>
            </body>
            </html>
            """

            # Initialize Yagmail with the sender's Gmail credentials
            yag = yagmail.SMTP(user=sender, password=app_password)

            # Sending the email
            yag.send(to=[Email], subject=subject, contents=html_content)

            return {"message": "Email sent successfully!"}

    except pymysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()


handler=mangum.Mangum(app)