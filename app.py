from flask import Flask, render_template, json, redirect
from flask import request
from flask_mysqldb import MySQL
import database.db_connector as db
from database.db_connector import execute_query, connect_to_database
import os


# configuration & database connection
app = Flask(__name__)


""" use this after after debugging
db_connection.ping(True)
cur = db_connection.cursor()
"""

 # Routes
@app.route('/')
def root():
    '''renders home page'''
    return render_template('index.html')

@app.route('/departments')
def departments():
    '''displays all deparments in the database'''
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Departments;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("departments.html", entity=results)

@app.route('/add_department', methods=['POST','GET'])
def add_department():
    ''' adds a department to the database '''
    if request.method =='GET':
        return render_template("add_department.html")
    
    else:
        
        # requests info from the user
        dept_name = request.form['dept_name']
        dept_total = 'Null'
        # create query from user feedback 
        query = "INSERT INTO Departments (dept_name, dept_total) VALUES (%s,%s);"
        # put data in a tuple and execute query
        data = (dept_name, dept_total)
        db_connection = db.connect_to_database()
        execute_query(db_connection, query, data)
        return render_template('success.html', action = 'Add department') # retuns a success message

@app.route('/employees')
def employees():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('employees.html', entity=results)

@app.route('/add_employee', methods=['POST','GET'])
def add_employee():
    db_connection = db.connect_to_database()
    # runs if it needs information from the database
    if request.method == 'GET':
        query = "SELECT dept_id, dept_name FROM Departments;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = execute_query(db_connection, query).fetchall()
        return render_template('add_employee.html', dept=results)

    # runs if it needs to update the database
    elif request.method == 'POST':
        # requests info from the user
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        gender = request.form['gender']
        address_1 = request.form['address_1'] 
        address_2 = request.form['address_2']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        tel = request.form['tel']
        email = request.form['email']
        start_date = request.form['start_date']
        end_date = 'Null'
        status = 'ACTIVE'
        dept_number = ['dept[0]']
        # create query from user feedback 
        query = "INSERT INTO Employees (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, start_date, end_date, status, dept_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        # put data in a tuple and execute query
        data = (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, start_date, end_date, status, dept_name)
        execute_query(db_connection, query, data)
        return render_template('success.html', action = 'Add employee') # retuns a success message

@app.route('/certifications')
def certifications():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Certifications;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('certifications.html', entity=results)

@app.route('/add_certification', methods=['POST', 'GET'])
def add_certification():
    if request.method == 'GET':
        return render_template("add_certification.html")
    else:
        # requests info from the user
        cert_name = request.form['cert_name']
        # create query from user feedback 
        query = "INSERT INTO Certifications (cert_name) VALUES (%s);"
        # put data in a tuple and execute query
        data = (cert_name)
        db_connection = db.connect_to_database()
        execute_query(db_connection, query, data)
        return render_template('success.html', action = 'Add certification') # retuns a success message


@app.route('/jobs')
def jobs():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Jobs;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('jobs.html', entity=results)

@app.route('/add_job')
def add_job():
    """ adds a job to the database"""

    # connect to the database
    db_connection = db.connect_to_database()

    # runs if it needs information from the database
    if request.method == 'GET':
        query = "SELECT dept_id, dept_name FROM Departments;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = execute_query(db_connection, query).fetchall()
        return render_template('add_job.html', dept=results)
    
     # runs if it needs to update the database
    elif request.method == 'POST':
        # requests info from the user
        dept_number = request.form['dept']
        job_description= request.form['job_description']

        # create query from user feedback 
        query = "INSERT INTO Jobs (dept_number, job_description) VALUES (%s,%s);"
        # put data in a tuple and execute query
        data = (dept_number, job_description)
        execute_query(db_connection, query, data)
        return render_template('success.html', action = 'Add job') # retuns a success message

@app.route('/classes')
def classes():
    """ displays all the classes in the database """
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Classes;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('classes.html', entity=results)

@app.route('/add_class', methods=['POST', 'GET'])
def add_class():
    """ adds a class to the database """
    # connect to database
    db_connection = db.connect_to_database()
    # runs if it needs information from the database
    if request.method == 'GET':
        query = "SELECT emp_id, f_name FROM Employees WHERE dept_number = 1 or dept_number = 2;"
        results = db.execute_query(db_connection=db_connection, query=query).fetchall()
        return render_template('add_class.html', instructor=results)

    # runs if it needs to update the database
    elif request.method == 'POST':
        # requests info from the user
        class_name = request.form['class_name']
        instructor = request.form['instructor']
        time = request.form['time']
        length = request.form['length']
        class_total = 'NULL'
        class_max = request.form['class_max']
        # create query from user feedback 
        query = "INSERT INTO Classes (class_name, instructor, time, length, class_total, class_max) VALUES (%s,%s,%s,%s,%s,%s);"
        # put data in a tuple and execute query
        data = (class_name, instructor, time, length, class_total, class_max)
        
        execute_query(db_connection, query, data)
        return render_template('success.html', action = 'Add class') # retuns a success message

@app.route('/members')
def members():
    ''' Displays all members in the database '''
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Members;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('members.html', entity=results)

@app.route("/add_member", methods=['POST', 'GET'])
def add_member():
    ''' adds a member to the database '''
    
    
    if request.method == 'GET':
        return render_template('add_member.html')
    else:
     # requests info from the user
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        gender = request.form['gender']
        address_1 = request.form['address_1'] 
        address_2 = request.form['address_2']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        tel = request.form['tel']
        email = request.form['email']
        status = 'ACTIVE'
    # create query from user feedback
    query = "INSERT INTO Members (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    # put data in a tuple and execute query
    data = (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, status)
    # connect to database
    db_connection = db.connect_to_database()
    execute_query(db_connection, query, data)
    return render_template('success.html', action = 'Add person')

@app.route('/emp_jobs')
def emp_dept():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Empl_Jobs;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_dept.html', entity=results)

@app.route('/emp_certs')
def emp_certs():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Emp_certs;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_certs.html', entity=results)

@app.route('/mem_classes')
def mem_classes():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Mem_Classes;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('mem_classes.html', entity=results)

@app.route('/emp_details')
def emp_jobs():
    db_connection = db.connect_to_database()
    query = "SELECT e.emp_id, e.f_name, e.l_name, ej.job_id, c.class_id FROM Employees e LEFT JOIN Emp_Jobs ej ON e.emp_id = ej.emp_id LEFT JOIN Classes c on e.emp_id = c.instructor  ;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_details.html', entity=results)

@app.route('/others')
def others():
    return render_template('others.html')


if __name__ == "__main__":
    app.run(host='flip2.engr.oregonstate.edu', port=46655, debug=False)