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

# ------- Departments add, update, delete and edit ------------------------
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
        return render_template('success.html', action= 'Add department', entity='Departments', active='departments', return_page='departments') # retuns a success message
# -----------End Departments------------------------------------------------------------

# ------- Employees add, update, delete and edit ------------------------
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
        dept_number = request.form['dept']
        # create query from user feedback 
        query = "INSERT INTO Employees (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, start_date, end_date, status, dept_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        # put data in a tuple and execute query
        data = (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, start_date, end_date, status, dept_number)
        execute_query(db_connection, query, data)
        return render_template('success.html', action = 'Add employee', entity='Employees', active='employees', return_page='employees') # returns a success message
# -------------End Employees----------------------------------------------------------

# ------- Certifications add, update, delete and edit ------------------------
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
        return render_template('success.html', action = 'Add certification', entity='Certifications', active='certifications', return_page='certifications') # retuns a success message
# -----------End Certifications------------------------------------------------------------

# ------- Jobs add, update, delete and edit ------------------------
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
        return render_template('success.html', action = 'Add job', entity='Jobs', active='jobs', return_page='jobs') # retuns a success message
# ---------------End Jobs--------------------------------------------------------

# ------- Classes add, update, delete and edit ------------------------
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
        return render_template('success.html', action = 'Add class', entity='Classes', active='classes', return_page='classes') # retuns a success message
# ---------------End Classes--------------------------------------------------------

# ------- Members add, update, delete and edit ------------------------
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
    return render_template('success.html', action ='Add member', entity='Members', active='members', return_page='members')
# ----------------End Members-------------------------------------------------------

# ------- Emp_Certs add, update, delete and edit ------------------------
@app.route('/emp_certs')
def emp_certs():
    db_connection = db.connect_to_database()
    query = "SELECT e.f_name, e.l_name, c.cert_name FROM Employees e LEFT JOIN Emp_Certs ec ON e.emp_id = ec.emp_id LEFT JOIN Certifications c ON ec.cert_id = c.cert_id WHERE c.cert_name is not NULL ORDER by e.emp_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_certs.html', entity=results)

@app.route('/add_emp_certs', methods=['POST','GET'])
def add_emp_certs():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT emp_id, f_name, l_name FROM Employees;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        employees = cursor.fetchall()
        query = "SELECT cert_id, cert_name FROM Certifications;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        certs = cursor.fetchall()
        return render_template('add_emp_certs.html', employees=employees, certs=certs )
    if request.method == 'POST':
        employee = request.form['employee']
        cert = request.form['cert']
        query = "INSERT INTO Emp_Certs (emp_id, cert_id) VALUES (%s,%s);"
        data = (employee, cert)
        execute_query(db_connection, query, data)
        return render_template('success.html', action='Certification added to an employee', entity='Emp_Certs', active='other', return_page='emp_certs')
# ------------------End Emp_Certs-----------------------------------------------------

# ------- Mem_Classes add, update, delete and edit ------------------------
@app.route('/mem_classes')
def mem_classes():
    db_connection = db.connect_to_database()
    query = "SELECT m.f_name, m.l_name, c.class_name FROM Members m LEFT JOIN Mem_Classes mc ON m.member_id = mc.member_id LEFT JOIN Classes c ON mc.class_id = c.class_id WHERE c.class_name is not NULL ORDER by m.member_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('mem_classes.html', entity=results)

@app.route('/add_mem_classes', methods=['POST','GET'])
def add_mem_classes():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT member_id, f_name, l_name FROM Members;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        members = cursor.fetchall()
        query = "SELECT class_id, class_name FROM Classes;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        classes = cursor.fetchall()
        return render_template('add_mem_classes.html', member=members, classes=classes )
    if request.method == 'POST':
        member = request.form['member']
        class_id = request.form['class']
        query = "INSERT INTO Mem_Classes (mem_id, class_id) VALUES (%s,%s);"
        data = (member, class_id)
        execute_query(db_connection, query, data)
        return render_template('success.html', action='Member add to class', entity='Mem_Classes', active='other', return_page='mem_classes')
# -----------------End Mem_Classes------------------------------------------------------

# ------- Emp_Jobs add, update, delete and edit ------------------------
@app.route('/emp_jobs')
def emp_jobs():
    db_connection = db.connect_to_database()
    query = "SELECT e.f_name, e.l_name, j.job_description FROM Employees e LEFT JOIN Emp_Jobs ej ON e.emp_id = ej.emp_id LEFT JOIN Jobs j ON ej.job_id = j.job_id WHERE j.job_description is not NULL ORDER by e.emp_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_jobs.html', entity=results)

@app.route('/add_emp_jobs', methods=['POST','GET'])
def add_emp_jobs():
    db_connection = db.connect_to_database()

    if request.method == 'GET':
        query1 = "SELECT emp_id, f_name, l_name FROM Employees;"
        cursor = db.execute_query(db_connection=db_connection, query=query1)
        employees = cursor.fetchall()
        query2 = "SELECT job_id FROM Jobs;"
        jobs = db.execute_query(db_connection=db_connection, query=query2)
        return render_template('add_emp_jobs.html', employee=employees, job=jobs )

    if request.method == 'POST':
        employee = request.form['employee']
        job = request.form['job']
        query = "INSERT INTO Emp_Jobs (emp_id, job_id) VALUES (%s,%s);"
        data = (employee, job)
        execute_query(db_connection, query, data)
        return render_template('success.html', action='Assignment was', entity='Emp_Jobs', active='other', return_page='emp_jobs')
# -------------------End Emp_Jobs----------------------------------------------------

@app.route('/others')
def others():
    return render_template('others.html')

@app.route('/job_emps')
def job_emps():
    """ this view shows a specific job and the employees associated with the job """

    return render_template('job_emps.html')

@app.route('/enrolled_classes')
def enrolled_classes():
    return render_template('enrolled_classes.html')

@app.route('/emp_details')
def emp_details():
    return render_template('emp_details.html')

@app.route('/emp_dept')
def emp_dept():
    return render_template('emp_dept.html')

@app.route('/class_details')
def class_details():
    db_connection = db.connect_to_database()
    class_name = request.args.get('class_name')
    print(class_name)
    query = "SELECT * from Classes WHERE class_name=%s; "
    data = (class_name)
    cursor = db.execute_query(db_connection, query, data)
    results = cursor.fetchall()
    return render_template('class_details.html', entity=results )


if __name__ == "__main__":
    app.run(host='flip2.engr.oregonstate.edu', port=57455, debug=True)