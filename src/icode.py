from fastapi import FastAPI, Body
import mangum
import pymysql

app = FastAPI()

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



handler=mangum.Mangum(app)