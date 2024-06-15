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
def call_stored_procedure():
   return {"response": "Test get call successfully called"}

@app.get("/company/get")
def call_stored_procedure():
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



handler=mangum.Mangum(app)