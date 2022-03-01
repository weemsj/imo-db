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
    ''' renders home page '''
    return render_template('index.html')


# ------- Departments add, update, delete and edit ------------------------
@app.route('/departments')
def departments():
    '''displays all deparments in the database'''
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Departments;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    print(results)
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
        return render_template('success.html', action= 'Add department', entity='Departments', active='departments', return_page='/departments') # retuns a success message


@app.route('/update_department', methods=['POST', 'GET'])
def update_department():
    db_connection = db.connect_to_database()
    dept_id = request.args.get('dept_id')
    if request.method == 'GET':
        dept_query = 'SELECT * FROM Departments WHERE dept_id = %s;' % (dept_id)
        dept_result = execute_query(db_connection, dept_query).fetchone()
        return render_template("update_department.html", dept_id=dept_id, department=dept_result, entity='Departments', return_page='/departments')

    elif request.method == 'POST':
        dept_id = request.form['dept_id']
        dept_name = request.form['dept_name']
        query = "UPDATE Departments SET dept_name = %s WHERE dept_id = %s ;"
        data = (dept_name, dept_id)
        execute_query(db_connection, query, data)
        return redirect('/departments')


@app.route('/delete_department')
def delete_department():
    dept_id = request.args.get('dept_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Departments WHERE dept_id = %s ;"
    data = (dept_id,)
    execute_query(db_connection, query, data)
    return redirect('/departments')


# -----------End Departments------------------------------------------------------------

# ------- Employees add, update, delete and edit ------------------------

@app.route('/employees')
def employees():
    db_connection = db.connect_to_database()
    query = "SELECT emp_id, f_name, l_name, status, dept_number FROM Employees;"
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


@app.route('/update_employee', methods=['POST','GET'])
def update_employee():
    emp_id = request.args.get('emp_id')
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        emp_query = 'SELECT * FROM Employees WHERE emp_id = %s;' % (emp_id)
        emp_result = execute_query(db_connection, emp_query).fetchone()
        dept_query = "SELECT dept_id, dept_name FROM Departments;"
        dept_result = execute_query(db_connection, dept_query).fetchall()
        return render_template("update_employee.html", emp_id=emp_id, employee=emp_result, dept=dept_result, entity='Employees', return_page='/employees')
    else:
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
        end_date = request.form['end_date']
        if end_date is Null:
            status = 'ACTIVE'
        else:
            status = 'NOT ACTIVE'
        dept_number = request.form['dept']
        query = "UPDATE Employees SET f_name = %s, l_name = %s, gender = %s, address_1 = %s, address_2 = %s, city = %s, state = %s, zip = %s, tel = %s, email = %s, start_date = %s , end_date = %s, status = %s, dept_number = %s WHERE emp_id = %s;"
        data = (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, start_date, end_date, status, dept_number)
        execute_query(db_connection, query, data)
        return redirect('/employees')


@app.route('/delete_employee')
def delete_employee():
    emp_id = request.args.get('emp_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Employees WHERE emp_id = %s ;"
    data = (emp_id,)
    execute_query(db_connection, query, data)
    return redirect('/employees')

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


@app.route('/update_certification', methods=['POST', 'GET'])
def update_certification():
    db_connection = db.connect_to_database()
    cert_id = request.args.get('cert_id')
    if request.method == 'GET':
        cert_query = 'SELECT * FROM Certifications WHERE cert_id = %s;' % (cert_id)
        cert_result = execute_query(db_connection, cert_query).fetchone()
        print(cert_result)
        return render_template("update_certification.html", cert_id=cert_id, cert=cert_result, return_page='/certifications', entity='Certification')

    elif request.method == 'POST':
        cert_id = request.form['cert_id']
        cert_name = request.form['cert_name']
        query = "UPDATE Certifications SET cert_name = %s WHERE cert_id = %s ;"
        data = (cert_name, cert_id)
        execute_query(db_connection, query, data)
        return redirect('/certifications')


@app.route('/delete_certification')
def delete_certification():
    cert_id = request.args.get('cert_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Certifications WHERE cert_id = %s ;"
    data = (cert_id,)
    execute_query(db_connection, query, data)
    return redirect('/certifications')

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
        return render_template('success.html', action = 'Add job', entity='Jobs', active='jobs', return_page='jobs')
        # returns a success message


@app.route('/update_job', methods=['POST', 'GET'])
def update_job():
    db_connection = db.connect_to_database()
    job_id = request.args.get('job_id')
    print(job_id)
    if request.method == 'GET':
        job_query = 'SELECT * FROM Jobs WHERE job_id = %s;' % (job_id)
        dept_query = 'SELECT dept_id, dept_name FROM Departments;'
        dept_result = execute_query(db_connection, dept_query).fetchall()
        job_result = execute_query(db_connection, job_query).fetchone()
        print(job_result)
        return render_template("update_job.html", job_id=job_id, dept=dept_result, job=job_result, return_page='/jobs', entity='Jobs')

    elif request.method == 'POST':
        job_id = request.form['job_id']
        job_description = request.form['job_description']
        query = "UPDATE Jobs SET job_descriptions = %s WHERE job_id = %s ;"
        data = (job_description, job_id)
        execute_query(db_connection, query, data)
        return redirect('/certifications')

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
    query = "SELECT member_id, f_name, l_name, status FROM Members;"
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


@app.route('/update_member', methods=['POST','GET'])
def update_member():
    member_id = request.args.get('member_id')
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        member_query = 'SELECT * FROM Members WHERE member_id = %s;' % (member_id)
        member_result = execute_query(db_connection, member_query).fetchone()
        return render_template("update_member.html", member_id=member_id, member=member_result, return_page='/members', entity='Members')
    else:
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
        status = request.form['status']
        query = "UPDATE Members SET f_name = %s, l_name = %s, gender = %s, address_1 = %s, address_2 = %s, city = %s, state = %s, zip = %s, tel = %s, email = %s, status = %s;"
        data = (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, status) 
        execute_query(db_connection, query, data)
        return redirect('/members')


@app.route('/delete_member')
def delete_member():
    member_id = request.args.get('member_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Members WHERE member_id = %s ;"
    data = (member_id,)
    execute_query(db_connection, query, data)
    return redirect('/members')

# ----------------End Members-------------------------------------------------------

# ------- Emp_Certs add, update, delete and edit ----------------------------------


@app.route('/emp_certs')
def emp_certs():
    cert_id = request.args.get('cert_id')
    db_connection = db.connect_to_database()
    if cert_id is None:
        query = "SELECT e.emp_id, e.f_name, e.l_name, c.cert_name FROM Employees e LEFT JOIN Emp_Certs ec ON e.emp_id = ec.emp_id LEFT JOIN Certifications c ON ec.cert_id = c.cert_id WHERE c.cert_name is not NULL ORDER by e.emp_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('emp_certs.html', entity=results)
    else:
        query = "SELECT e.emp_id, e.f_name, e.l_name, c.cert_name FROM Certifications c LEFT JOIN Emp_Certs ec ON c.cert_id = ec.cert_id LEFT JOIN Employees e ON ec.emp_id = e.emp_id WHERE c.cert_id = %s;"
        data = (cert_id,)
        cursor = db.execute_query(db_connection, query, data)
        results = cursor.fetchall()
        page = results[0]['cert_name'] # value is {'f_name': 'Eberto', 'l_name': 'Cashman', 'cert_name': 'NASM-CPT'}
        print(page)  # trying to find the index for cert_name in the dictionary 
        return render_template('emp_certs.html', entity=results, page=page) 


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


@app.route('/update_emp_certs', methods=['POST', 'GET'])
def update_emp_certs():
    db_connection = db.connect_to_database()
    emp_id = request.args.get('emp_id')
    cert_name = request.args.get('cert_name')
    if request.method == 'GET':
        query = "SELECT emp_id, f_name, l_name FROM Employees WHERE emp_id = %s ;" % (emp_id)
        cursor = db.execute_query(db_connection, query)
        employee = cursor.fetchall()
        query = "SELECT cert_id, cert_name FROM Certifications;"
        cursor = db.execute_query(db_connection, query)
        certs = cursor.fetchall()
        query = "SELECT cert_id FROM Certifications WHERE cert_name = '%s';" % (cert_name)
        cursor = db.execute_query(db_connection, query)
        cert_id = cursor.fetchall()
        cert_id = cert_id[0]['cert_id']
        return render_template('update_emp_cert.html', employee = employee, certs=certs, curr_cert_id=cert_id)

    else:
        emp_id = request.form['emp_id']
        cert_id = request.form['cert_id']
        query = "UPDATE Emp_Certs SET emp_id = %s, cert_id = %s;"
        data = (emp_id, cert_id)
        execute_query(db_connection, query, data)
        return redirect('emp_certs')


@app.route('/delete_emp_certs')
def delete_emp_certs():
    cert_name = request.args.get('cert_name')
    emp_id = request.args.get('emp_id')
    db_connection = db.connect_to_database()
    certquery = "SELECT cert_id FROM Certifications WHERE cert_name = '%s';" % (cert_name)
    cursor = db.execute_query(db_connection, certquery)
    result = cursor.fetchone()
    cert_id = result[0]['cert_id']
    query = "DELETE from Emp_Certs WHERE emp_id = %s and cert_id = %s ;"
    data = (emp_id, cert_id)
    execute_query(db_connection, query, data)
    return redirect('/emp_certs')

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
    query = 'SELECT d.dept_name, e.f_name, e.l_name, j.job_description FROM Employees e LEFT JOIN Emp_Jobs ej ON ej.emp_id = e.emp_id LEFT JOIN Jobs j ON ej.job_id = j.job_id LEFT JOIN Departments d ON d.dept_id = j.dept_number WHERE j.job_description is NOT NULL;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_jobs.html', entity=results, page='Jobs', return_page='/jobs')


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
    job_id = request.args.get('job_id')
    db_connection = db.connect_to_database()
    query = 'SELECT d.dept_name, e.f_name, e.l_name, j.job_description FROM Employees e LEFT JOIN Emp_Jobs ej ON ej.emp_id = e.emp_id LEFT JOIN Jobs j ON ej.job_id = j.job_id LEFT JOIN Departments d ON d.dept_id = j.dept_number WHERE j.job_description is NOT NULL and j.job_id= %s;' % (job_id)
    cursor = db.execute_query(db_connection, query)
    result = cursor.fetchall()
    print(result)
    return render_template('job_emps.html', entity = result, job_id = job_id, page='Jobs', return_page='/jobs')


@app.route('/emp_details')
def emp_details():
    emp_id = request.args.get('emp_id')
    db_connection = db.connect_to_database()
    query = 'SELECT * FROM Employees WHERE emp_id = %s;' % (emp_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    print(results)
    return render_template('emp_details.html', entity = results, emp_id=emp_id, page='All Employees', return_page='/employees')


@app.route('/enrolled_classes')
def enrolled_classes():
    member_id = request.args.get('member_id')
    print(member_id)
    db_connection = db.connect_to_database()
    query = 'SELECT c.class_name, c.time, c.length FROM Members m LEFT JOIN Mem_Classes mc ON m.member_id = mc.member_id LEFT JOIN Classes c ON mc.class_id = c.class_id WHERE m.member_id = %s;' % (member_id)
    member = 'SELECT f_name, l_name FROM Members WHERE member_id = %s;' % (member_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor = db.execute_query(db_connection=db_connection, query=member)
    member = cursor.fetchall()
    print(results)
    print(member)
    return render_template('enrolled_classes.html', entity = results, member = member)


@app.route('/member_details')
def member_details():
    member_id = request.args.get('member_id')
    db_connection = db.connect_to_database()
    query = 'SELECT * FROM Members WHERE member_id = %s;' % (member_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    print(results)
    return render_template('emp_details.html', entity=results)


@app.route('/emp_dept')
def emp_dept():
    dept_id = request.args.get('dept_id')
    dept_name = request.args.get('dept_name')
    print(dept_name)
    db_connection = db.connect_to_database()
    query = 'SELECT f_name, l_name FROM Employees WHERE dept_number = %s;' % (dept_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_dept.html', entity = results, dept_name=dept_name)


@app.route('/class_details')
def class_details():
    '''
    db_connection = db.connect_to_database()
    class_name = request.args.get('class_name')
    print(class_name)
    query = "SELECT * from Classes WHERE class_name = %s ;"
    data = (class_name,)
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=data)
    results = cursor.fetchall()
    return render_template('class_details.html', entity=results )
    '''
    return render_template('class_details.html')


if __name__ == "__main__":
    app.run(host='flip2.engr.oregonstate.edu', port=4024, debug=True)