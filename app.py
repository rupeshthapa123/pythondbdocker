import mysql.connector
import json
from flask import Flask

app = Flask(__name__)

"""
This is a Flask route that returns the string "Hello, Docker!" when the root URL is accessed.
:return: the string "Hello, Docker!" when the root URL is accessed.
"""
@app.route('/')
def hello_world():
    return 'Hello, Docker!'

"""
This function retrieves all the data from the "widgets" table in the "inventory" database and
returns it as a JSON object.
:return: A JSON string containing all the rows and columns from the "widgets" table in the
"inventory" database.
"""
@app.route('/widgets')
def get_widgets():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM widgets")
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()
    return json.dumps(json_data)

"""
This function initializes a MySQL database named "inventory" and creates a table named "widgets"
with columns for name and description.
:return: The string 'init database' is being returned.
"""
@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.execute("USE inventory")

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return 'init database'

# This code block is checking if the current script is being run as the main program (as opposed to
# being imported as a module into another program). If it is the main program, it starts the Flask
# application and listens for incoming requests on all available network interfaces (0.0.0.0).
if __name__ == "__main__":
    app.run(host ='0.0.0.0')