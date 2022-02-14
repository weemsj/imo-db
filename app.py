from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
import database.db_connector as db
import os


# configuration & database connection
app = Flask(__name__)
db_connection = db.connect_to_database()

db_connection.ping(True)
cur = db_connection.cursor()

 # Routes
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/departments')
def departments():
    query = "SELECT * FROM Departments;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("departments.html", entity=results)

@app.route('/employees')
def employees():
    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('employees.html', entity=results)

@app.route('/certifications')
def certifications():
    query = "SELECT * FROM Certifications;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('certifications.html', entity=results)

@app.route('/jobs')
def jobs():
    query = "SELECT * FROM Jobs;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('jobs.html', entity=results)

@app.route('/classes')
def classes():
    query = "SELECT * FROM Classes;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('classes.html', entity=results)

@app.route('/members')
def members():
    query = "SELECT * FROM Members;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('members.html', entity=results)

@app.route('/emp_dept')
def emp_dept():
    query = "SELECT * FROM Emp_Dept;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('relational_tables.j2', entity=results)

@app.route('/emp_certs')
def emp_certs():
    return render_template('relational_tables.j2')

@app.route('/mem_classes')
def mem_classes():
    return render_template('relational_tables.j2')

@app.route('/emp_jobs')
def emp_jobs():
    return render_template('relational_tables.j2')



if __name__ == "__main__":
    app.run(host='flip1.engr.oregonstate.edu', port=45565, debug=False)