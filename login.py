import pymysql
from fastapi import FastAPI, Body
import mangum

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


handler = mangum.Mangum(app)