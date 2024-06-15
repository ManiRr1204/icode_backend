import mysql.connector as mysql
from fastapi import FastAPI, Body
import mangum

app = FastAPI()

# Improved database connection handling with context manager
def connect_to_database():
    try:
        connection = mysql.connect(
            host="mydb.cxms2oikutcu.us-west-2.rds.amazonaws.com",
            user="admin",
            password="databasepass",
            database="icodeTest"
        
        )
        return connection
    except mysql.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.get("/test")
def call_stored_procedure():
   return {"response": "Test get call successfully called"}

@app.get("/get_all_companies")
def call_stored_procedure():
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            sql = "select * from company"
            # sql = "CALL get_all_companies"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            companies = []
            column_names = [i[0] for i in mycursor.description] 
            for row in myresult:
                company = dict(zip(column_names, row))
                companies.append(company)

            return companies 

    except mysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

@app.get("/get_company/{company_id}")
async def get_company(company_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            # Execute SELECT query with parameter
            sql = "SELECT * FROM company WHERE cid = %s"
            mycursor.execute(sql, (company_id,))

            # Fetch results (assuming only one company for the ID)
            myresult = mycursor.fetchall()
            column_names = [i[0] for i in mycursor.description] 
            for row in myresult:
                company = dict(zip(column_names, row))

            return company 

    except mysql.Error as err:
        print(f"Error retrieving company: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# POST request to create a company
@app.post("/create_company")
async def create_company(company: dict = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            # Extract data from request body
            cid = company.get("cid")
            cname = company.get("cname")
            clogo = company.get("clogo")  # Assuming clogo is a byte stream
            caddress = company.get("caddress")
            username = company.get("username")
            password = company.get("password")

            # Call the stored procedure
            # sql = "CALL CreateCompany(%s, %s, %s, %s, %s, %s)"
            sql = """
                INSERT INTO company (cid, cname, clogo, caddress, username, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            mycursor.execute(sql, (cid, cname, clogo, caddress, username, password))
            connection.commit()  # Commit changes

            return {"message": "Company created successfully"}

    except mysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# DELETE request to delete a company
@app.delete("/delete_company/{company_id}")
async def delete_company(company_id: str):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as mycursor:
            # sql = "CALL delete_company(%s)"
            sql = "DELETE FROM company WHERE cid = %s"
            mycursor.execute(sql, (company_id,))
            connection.commit()

            return {"message": f"Company with ID '{company_id}' deleted successfully"}

    except mysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

# PUT request to update a company
@app.put("/update_company/{company_id}")
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

            # sql = "CALL update_company(%s, %s, %s, %s, %s, %s)"
            sql="UPDATE company SET cname = %s,  clogo = %s,   caddress = %s,  username = %s,  password = %s  WHERE cid = %s"
            mycursor.execute(sql, ( cname, clogo, caddress, username, password, cid))

            connection.commit()

            return {"message": f"Company with ID '{company_id}' updated successfully"}

    except mysql.Error as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

handler=mangum.Mangum(app)