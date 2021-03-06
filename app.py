from flask import Flask, render_template, json, redirect, flash
from flask import request
from flask_mysqldb import MySQL
import database.db_connector as db
from database.db_connector import execute_query, connect_to_database
import os


# configuration & database connection
app = Flask(__name__)
app.secret_key = 'secret'


""" use this after after debugging
db_connection.ping(True)
cur = db_connection.cursor()
"""


# Routes
@app.route('/')
def root():
    """ renders home page """
    return render_template('index.html')


# ------- Departments add, update, delete and edit ------------------------
@app.route('/departments')
def departments():
    """displays all departments in the database"""
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Departments;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("departments.html", entity=results)


@app.route('/add_department', methods=['POST','GET'])
def add_department():
    """ adds a department to the database """
    if request.method =='GET':
        return render_template("add_department.html")
    
    else:
        # requests info from the user
        dept_name = request.form['dept_name']
        dept_name = dept_name.title()
        dept_total = 'Null'
        # create query from user feedback 
        query = "INSERT INTO Departments (dept_name, dept_total) VALUES (%s,%s);"
        # put data in a tuple and execute query
        data = (dept_name, dept_total)
        db_connection = db.connect_to_database()
        execute_query(db_connection, query, data)
        flash('Department add was successful', 'success')
        return redirect('/departments')


@app.route('/update_department', methods=['POST', 'GET'])
def update_department():
    """ updates department using the department pk dept_id sent as an argument. This function expects an integer argument named 'dept_id' """
    db_connection = db.connect_to_database()
    dept_id = request.args.get('dept_id')
    if request.method == 'GET':
        dept_query = 'SELECT * FROM Departments WHERE dept_id = %s;' % (dept_id)
        dept_result = execute_query(db_connection, dept_query).fetchone()
        return render_template("update_department.html", dept_id=dept_id, department=dept_result, entity='Departments', return_page='/departments')

    elif request.method == 'POST':
        dept_id = request.form['dept_id']
        dept_name = request.form['dept_name']
        dept_name = dept_name.title()
        query = "UPDATE Departments SET dept_name = %s WHERE dept_id = %s ;"
        data = (dept_name, dept_id)
        execute_query(db_connection, query, data)
        flash('Update department was successful', 'success')
        return redirect('/departments')


@app.route('/delete_department')
def delete_department():
    """ Deletes a department from the database. This function expects an integer argument named 'dept_id' """
    dept_id = request.args.get('dept_id')
    db_connection = db.connect_to_database()
    query = "SELECT dept_total FROM Departments WHERE dept_id = %s;" % (dept_id)
    cursor = execute_query(db_connection, query)
    dept = cursor.fetchone()
    if dept['dept_total'] > 0:
        flash("Can't delete a department with employees in it, please reassign employees", "error")
        return redirect('/departments')

    query = "DELETE from Departments WHERE dept_id = %s ;"
    data = (dept_id,)
    execute_query(db_connection, query, data)
    # add flash message here if delete was successful
    flash('Department delete was successful', 'success')
    return redirect('/departments')  # after delete redirect to page to show results


# -----------End Departments------------------------------------------------------------

# ------- Employees add, update, delete and edit ------------------------

@app.route('/employees')
def employees():
    """ Displays employee id, first name, last name, status and department number of an employee """
    db_connection = db.connect_to_database()
    query = "SELECT emp_id, f_name, l_name, status, dept_number FROM Employees;"  # should department name also be added or in Leu of dept number
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()  # returns a tuple so need to access first value in the tuple first
    return render_template('employees.html', entity=results)


@app.route('/employee_search', methods=['POST'])
def employee_search():
    """ Displays employee id, first name, last name, status and department number for a provided last name, using SQL LIKE functionality """
    db_connection = db.connect_to_database()
    last_name = request.form['emp_search']
    last_name = last_name.title()
    query = "SELECT emp_id, f_name, l_name, status, dept_number FROM Employees WHERE l_name LIKE %s;"
    data = (last_name,)
    cursor = db.execute_query(db_connection, query, data)
    results = cursor.fetchall()  # returns a tuple so need to access first value in the tuple first
    # Only display results if one is found:
    if results:
        return render_template('employee_search.html', entity=results)
    else:
        flash('No results found for entry', 'warning')
        return redirect('/employees')


@app.route('/add_employee', methods=['POST','GET'])
def add_employee():
    """
    adds an employee to the employee table 'end_date' is automatically 'Null' on add can be modified on update. Status is also defaulted to 'ACTIVE'.
    On get request a query for all departments is done to provide the user with a dropdown of preset departments in the database to choose from when adding an employee.
    """
    db_connection = db.connect_to_database()
    # runs if it needs information from the database
    if request.method == 'GET':
        query = "SELECT dept_id, dept_name FROM Departments;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('add_employee.html', dept=results)

    # runs if it needs to update the database
    elif request.method == 'POST':
        # requests info from the user
        f_name = request.form['f_name']
        f_name = f_name.title()
        l_name = request.form['l_name']
        l_name = l_name.title()
        gender = request.form['gender']
        address_1 = request.form['address_1'] 
        address_2 = request.form['address_2']
        city = request.form['city']
        state = request.form['state']
        state = state.upper()  # converts state to uppercase to keep with database formate
        zip = request.form['zip']
        tel = request.form['tel']
        email = request.form['email']
        start_date = request.form['start_date']
        end_date = None  # default is null. Can't add a terminated employee to the database
        status = 'ACTIVE'  # employee is only added to the database when active
        dept_number = request.form['dept']
        # create query from user feedback 
        query = "INSERT INTO Employees (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, start_date, end_date, status, dept_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        # put data in a tuple and execute query
        data = (
        f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, start_date, end_date, status,
        dept_number)
        execute_query(db_connection, query, data)
        # need to return to redirected 'employees' page and add flash message here
        flash('Employee added successfully', 'success')
        return redirect('/employees')


@app.route('/update_employee', methods=['POST','GET'])
def update_employee():
    """ updates employee expects an integer argument passed called 'emp_id' """
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
        f_name = f_name.title()
        l_name = request.form['l_name']
        l_name = l_name.title()
        gender = request.form['gender']
        address_1 = request.form['address_1']
        address_2 = request.form['address_2']
        if address_2 == '':
            address_2 = None
        city = request.form['city'].title()
        state = request.form['state']
        state = state.upper()
        zip = request.form['zip']
        tel = request.form['tel']
        email = request.form['email']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        if end_date == '':
            status = 'ACTIVE'
            end_date = None
        else:
            status = 'NOT ACTIVE'
        if status == 'NOT ACTIVE':
            dept_number = None
        else:
            dept_number = request.form['dept']
        query = "UPDATE Employees SET f_name = %s, l_name = %s, gender = %s, address_1 = %s, address_2 = %s, city = %s, state = %s, zip = %s, tel = %s, email = %s, start_date = %s , end_date = %s, status = %s, dept_number = %s WHERE emp_id = %s;"
        data = (
            f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, start_date, end_date, status,
            dept_number, emp_id)
        execute_query(db_connection, query, data)
        # add flash message here
        flash('Employee update successful', 'success')
        return redirect('/employees')


@app.route('/delete_employee', methods=['POST', 'GET'])
def delete_employee():
    """ deletes an employee from the table, expects an integer argument passed as 'emp_id' """
    db_connection = db.connect_to_database()
    emp_id = request.args.get('emp_id')
    if request.method == 'POST':
        confirm = request.form.get('user_input')
        print(confirm)
        if confirm and confirm == 'True':
            # find all the classes an instructor teaches
            query1 = "SELECT class_id FROM Classes WHERE instructor = %s;" % (emp_id)
            cursor = db.execute_query(db_connection, query1)
            classes = cursor.fetchall()
            # iterate through all classes and delete the classes
            for c in classes[0].values():
                print(c)
                mini_query = "DELETE FROM Classes WHERE class_id = %s;" % (c)
                execute_query(db_connection, mini_query)
            # after all classes are deleted, delete employee
            query = "DELETE from Employees WHERE emp_id = %s ;"
            data = (emp_id,)
            execute_query(db_connection, query, data)
            # flash message here
            flash('Employee and all classes associated with employee have been deleted successfully', 'success')
            return redirect('/employees')

        elif confirm and confirm == 'False':
            print('wont delete anything')
            return redirect('/employees')

# -------------End Employees----------------------------------------------------------

# ------- Certifications add, update, delete and edit ------------------------


@app.route('/certifications')
def certifications():
    """ shows all certifications at IMO """
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Certifications;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('certifications.html', entity=results)


@app.route('/add_certification', methods=['POST', 'GET'])
def add_certification():
    """ add new certification to database """
    if request.method == 'GET':
        return render_template("add_certification.html")
    else:
        # requests info from the user
        cert_name = request.form['cert_name']
        cert_name = cert_name.title()
        # create query from user feedback 
        query = "INSERT INTO Certifications (cert_name) VALUES (%s);"
        # put data in a tuple and execute query
        data = (cert_name)
        db_connection = db.connect_to_database()
        execute_query(db_connection, query, data)
        flash('Certification add was successful', 'success')
        return redirect('/certifications')


@app.route('/update_certification', methods=['POST', 'GET'])
def update_certification():
    """ updates an existing certification, needs a certification id """
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
        cert_name = cert_name.title()
        query = "UPDATE Certifications SET cert_name = %s WHERE cert_id = %s ;"
        data = (cert_name, cert_id)
        execute_query(db_connection, query, data)
        flash('Update certification was successful', 'success')
        return redirect('/certifications')


@app.route('/delete_certification')
def delete_certification():
    """ deletes a certification from the database, needs a certification id"""
    cert_id = request.args.get('cert_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Certifications WHERE cert_id = %s ;"
    data = (cert_id,)
    execute_query(db_connection, query, data)
    flash('Certification was successfully deleted', 'success')
    return redirect('/certifications')

# -----------End Certifications------------------------------------------------------------

# ------- Jobs add, update, delete and edit ------------------------


@app.route('/jobs')
def jobs():
    """ shows all jobs and descriptions in database """
    db_connection = db.connect_to_database()
    query = "SELECT j.job_id, d.dept_name, j.job_description FROM Jobs j LEFT JOIN Departments d ON j.dept_number = d.dept_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('jobs.html', entity=results)


@app.route('/add_job', methods=['POST', 'GET'])
def add_job():
    """ adds a job to the database"""

    # connect to the database
    db_connection = db.connect_to_database()

    # runs if it needs information from the database
    if request.method == 'GET':
        query = "SELECT dept_id, dept_name FROM Departments;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('add_job.html', dept=results)
    
    # runs if it needs to update the database
    elif request.method == 'POST':
        # requests info from the user
        dept_number = request.form['dept']
        job_description = request.form['job_description']

        # create query from user feedback 
        query = "INSERT INTO Jobs (dept_number, job_description) VALUES (%s,%s);"
        # put data in a tuple and execute query
        data = (dept_number, job_description)
        execute_query(db_connection, query, data)
        flash('Job add was successful', 'success')
        # returns a success message
        return redirect('/jobs')


@app.route('/update_job', methods=['POST', 'GET'])
def update_job():
    """ updates a job in the database, needs job_id """
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
        dept_id = request.form['dept']
        job_description = request.form['job_description']
        query = "UPDATE Jobs SET job_description = %s, dept_number = %s WHERE job_id = %s ;"
        data = (job_description, dept_id, job_id)
        execute_query(db_connection, query, data)
        flash('Job updated successfully', 'successful')
        return redirect('/jobs')


@app.route('/delete_job')
def delete_job():
    """ deletes a job from the database, needs job_id """
    job_id = request.args.get('job_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Jobs WHERE job_id = %s ;"
    data = (job_id,)
    execute_query(db_connection, query, data)
    flash('Job was deleted successfully', 'success')
    return redirect('/jobs')

# ---------------End Jobs--------------------------------------------------------

# ------- Classes add, update, delete and edit ------------------------


@app.route('/classes')
def classes():
    """ displays all the classes in the database """
    db_connection = db.connect_to_database()
    query = "SELECT c.class_id, c.class_name, c.instructor, e.f_name, e.l_name, c.time, c.length, c.class_total, c.class_max FROM Classes c LEFT JOIN Employees e ON c.instructor = e.emp_id ;"
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
        query = "SELECT emp_id, f_name, l_name FROM Employees WHERE dept_number = 1 or dept_number = 2;"
        results = db.execute_query(db_connection=db_connection, query=query).fetchall()
        flash('Class add was successful', 'success')
        return render_template('add_class.html', instructor=results)

    # runs if it needs to update the database
    elif request.method == 'POST':
        # requests info from the user
        class_name = request.form['class_name']
        class_name = class_name.title()
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
        flash('Class add was successful', 'success')
        return redirect('/classes')


@app.route('/update_class', methods=['POST', 'GET'])
def update_class():
    """ updates a class in the database, needs class_id """
    db_connection = db.connect_to_database()
    class_id = request.args.get('class_id')
    print(class_id)
    if request.method == 'GET':
        class_query = 'SELECT * FROM Classes WHERE class_id = %s;' % (class_id)
        instructor_query = 'SELECT emp_id, f_name, l_name FROM Employees WHERE dept_number = 1 or dept_number = 2;'
        instructor_result = execute_query(db_connection, instructor_query).fetchall()
        class_result = execute_query(db_connection, class_query).fetchone()
        print(class_result)
        return render_template("update_class.html", class_id=class_id, instructor=instructor_result, classes=class_result, return_page='/classes', entity='Classes')

    elif request.method == 'POST':
        class_id = request.form['class_id']
        print(class_id)
        class_name = request.form['class_name']
        class_name = class_name.title()
        instructor = request.form['instructor']
        time = request.form['time']
        length = request.form['length']
        class_total = request.form['class_total']
        class_max = request.form['class_max']
        query = "UPDATE Classes SET class_name = %s, instructor = %s, time = %s, length = %s, class_total = %s, class_max = %s WHERE class_id = %s ;"
        data = (class_name, instructor, time, length, class_total, class_max, class_id)
        execute_query(db_connection, query, data)
        flash('Class update was successful', 'success')
        return redirect('/classes')


@app.route('/delete_class')
def delete_class():
    """ deletes class from database, needs class_id """
    class_id = request.args.get('class_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Classes WHERE class_id = %s ;"
    data = (class_id,)
    execute_query(db_connection, query, data)
    flash('Class was successfully deleted', 'success')
    return redirect('/classes')
# ---------------End Classes--------------------------------------------------------

# ------- Members add, update, delete and edit ------------------------


@app.route('/members')
def members():
    """ Displays all members in the database """
    db_connection = db.connect_to_database()
    query = "SELECT member_id, f_name, l_name, status FROM Members;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('members.html', entity=results, view="current and past")


@app.route('/members_search', methods=['POST'])
def members_search():
    """ Displays member id, first name, last name, and status for a provided last name, using SQL LIKE functionality """
    db_connection = db.connect_to_database()
    last_name = request.form['lname']
    last_name = last_name.title()
    query = "SELECT member_id, f_name, l_name, status FROM Members WHERE l_name LIKE %s;"
    data = (last_name,)
    cursor = db.execute_query(db_connection, query, data)
    results = cursor.fetchall()  # returns a tuple so need to access first value in the tuple first
    #Only display results if one is found:
    if results:
        return render_template('members_search.html', entity=results)
    else:
        flash('No results found for entry', 'warning')
        return redirect('/members')


@app.route("/add_member", methods=['POST', 'GET'])
def add_member():
    """ adds a member to the database """

    if request.method == 'GET':
        return render_template('add_member.html')
    else:
        # requests info from the user
        f_name = request.form['f_name']
        f_name = f_name.title()
        l_name = request.form['l_name']
        l_name = l_name.title()
        gender = request.form['gender']
        address_1 = request.form['address_1'] 
        address_2 = request.form['address_2']
        city = request.form['city']
        state = request.form['state']
        state = state.upper()
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
    flash('Member add was successful', 'success')
    return redirect('/members')


@app.route('/update_member', methods=['POST','GET'])
def update_member():
    """ updates member in database, takes member_id """
    member_id = request.args.get('member_id')
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        member_query = 'SELECT * FROM Members WHERE member_id = %s;' % (member_id)
        member_result = execute_query(db_connection, member_query).fetchone()
        return render_template("update_member.html", member_id=member_id, member=member_result, return_page='/members', entity='Members')
    else:
        member_id = request.form['member_id']
        f_name = request.form['f_name']
        f_name = f_name.title()
        l_name = request.form['l_name']
        l_name = l_name.title()
        gender = request.form['gender']
        address_1 = request.form['address_1']
        address_2 = request.form['address_2']
        city = request.form['city']
        state = request.form['state']
        state = state.upper()
        zip = request.form['zip']
        tel = request.form['tel']
        email = request.form['email']
        status = request.form['status']
        query = "UPDATE Members SET f_name = %s, l_name = %s, gender = %s, address_1 = %s, address_2 = %s, city = %s, state = %s, zip = %s, tel = %s, email = %s, status = %s WHERE member_id = %s;"
        data = (f_name, l_name, gender, address_1, address_2, city, state, zip, tel, email, status, member_id)
        execute_query(db_connection, query, data)
        flash('Member update was successful', 'success')
        return redirect('/members')


@app.route('/delete_member')
def delete_member():
    """ delete member from database, takes member_id """
    member_id = request.args.get('member_id')
    db_connection = db.connect_to_database()
    query1 = "SELECT class_id FROM Mem_Classes WHERE member_id = %s;" % (member_id)
    cursor = execute_query(db_connection, query1)
    classes = cursor.fetchall()
    if classes:
        for c in classes[0].values():
            mini_query = "UPDATE Classes SET class_total = class_total - 1 WHERE class_id = %s;" % (c)
            execute_query(db_connection, mini_query)
    query = "DELETE from Members WHERE member_id = %s ;"
    data = (member_id,)
    execute_query(db_connection, query, data)
    flash('Member delete was successful', 'success')
    return redirect('/members')

# ----------------End Members-------------------------------------------------------

# ------- Emp_Certs add, update, delete and edit ----------------------------------


@app.route('/emp_certs')
def emp_certs():
    """ displays all employee certifications can take a cert_id """
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
        page = results[0]['cert_name']
        return render_template('emp_certs.html', entity=results, page=page) 


@app.route('/add_emp_certs', methods=['POST','GET'])
def add_emp_certs():
    """ adds employee certification relationship """
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT emp_id, f_name, l_name FROM Employees;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        employees = cursor.fetchall()
        query = "SELECT cert_id, cert_name FROM Certifications;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        certs = cursor.fetchall()
        return render_template('add_emp_certs.html', employees=employees, certs=certs)

    if request.method == 'POST':
        employee = request.form['employee']
        cert = request.form['cert']
        query = "INSERT INTO Emp_Certs (emp_id, cert_id) VALUES (%s,%s);"
        data = (employee, cert)
        execute_query(db_connection, query, data)
        flash('Employee certification add was successful', 'success')
        return redirect('/emp_certs')
        # return render_template('success.html', action='Certification added to an employee', entity='Emp_Certs', active='other', return_page='emp_certs')


@app.route('/update_emp_certs', methods=['POST', 'GET'])
def update_emp_certs():
    """ updates an employee certification relationship , takes an emp_id and cert_name """
    db_connection = db.connect_to_database()
    emp_id = request.args.get('emp_id')
    cert_name = request.args.get('cert_name')
    if request.method == 'GET':
        query = "SELECT emp_id, f_name, l_name FROM Employees WHERE emp_id = %s ;" % (emp_id)
        cursor = db.execute_query(db_connection, query)
        employee = cursor.fetchone()
        query = "SELECT cert_id, cert_name FROM Certifications;"
        cursor = db.execute_query(db_connection, query)
        certs = cursor.fetchall()
        query = "SELECT cert_id FROM Certifications WHERE cert_name = '%s';" % (cert_name)
        cursor = db.execute_query(db_connection, query)
        cert_id = cursor.fetchall()
        cert_id = cert_id[0]['cert_id']
        print(employee)
        return render_template('update_emp_cert.html', employee=employee, certs=certs, curr_cert_id=cert_id, return_page='emp_certs', entity='Emp_Certs')

    else:
        emp_id = request.form['emp_id']
        cert_id = request.form['cert_id']
        query = "UPDATE Emp_Certs SET emp_id = %s, cert_id = %s WHERE emp_id = %s;"
        data = (emp_id, cert_id, emp_id)
        execute_query(db_connection, query, data)
        flash('Employee certification update was successful', 'success')
        return redirect('emp_certs')


@app.route('/delete_emp_certs')
def delete_emp_certs():
    """ deletes employee certification relationship, takes certification name and emp_id"""
    cert_name = request.args.get('cert_name')
    emp_id = request.args.get('emp_id')
    db_connection = db.connect_to_database()
    certquery = "SELECT cert_id FROM Certifications WHERE cert_name = '%s';" % (cert_name)
    cursor = db.execute_query(db_connection, certquery)
    result = cursor.fetchone()
    cert_id = result['cert_id']
    query = "DELETE from Emp_Certs WHERE emp_id = %s and cert_id = %s ;"
    data = (emp_id, cert_id)
    execute_query(db_connection, query, data)
    flash('Employee certification was successfully deleted', 'success')
    return redirect('/emp_certs')

# ------------------End Emp_Certs-----------------------------------------------------


# ------- Mem_Classes add, update, delete and edit ------------------------
@app.route('/mem_classes')
def mem_classes():
    """ shows members and class relationship """
    db_connection = db.connect_to_database()
    query = "SELECT c.class_id, c.class_name, c.time, m.member_id, m.f_name, m.l_name FROM Members m LEFT JOIN Mem_Classes mc ON m.member_id = mc.member_id LEFT JOIN Classes c ON mc.class_id = c.class_id WHERE c.class_name is not NULL ORDER by m.member_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('mem_classes.html', entity=results)


@app.route('/add_mem_classes', methods=['POST','GET'])
def add_mem_classes():
    """ adds a member/class relationship to the database """
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT member_id, f_name, l_name FROM Members WHERE status = 'ACTIVE';"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        members = cursor.fetchall()
        query = "SELECT class_id, class_name FROM Classes;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        classes = cursor.fetchall()
        return render_template('add_mem_classes.html', member=members, classes=classes, entity='Member Classes',
                               return_page='mem_classes')

    if request.method == 'POST':
        member = request.form['member']
        class_id = request.form['class']
        query = "SELECT class_total, class_max FROM Classes WHERE  class_id = %s;" % (class_id)
        cursor = db.execute_query(db_connection, query)
        check_cap = cursor.fetchone()
        if check_cap['class_total'] == check_cap['class_max']:  # make sure class isn't full
            # insert flash message here (class is at capacity)
            flash('class is full', 'error')  # implement category for filters
            print('class is full')
            return redirect('/mem_classes')
        query = "INSERT INTO Mem_Classes (member_id, class_id) VALUES (%s,%s);"
        data = (member, class_id)
        execute_query(db_connection, query, data)
        flash("Member's class was successfully added ", 'success')
        return redirect('/mem_classes')


@app.route('/enroll_into_class', methods=['POST', 'GET'])
def enroll_into_class():
    """ enrolls a member into a class, takes a class_id """
    db_connection = db.connect_to_database()
    class_id = request.args.get('class_id')
    if request.method == 'GET':
        query = "SELECT member_id, f_name, l_name FROM Members WHERE status = 'ACTIVE';"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        members = cursor.fetchall()
        query = "SELECT class_id, class_name FROM Classes WHERE class_id = %s;" % (class_id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        classes = cursor.fetchone()
        return render_template('enroll_into_class.html', member=members, classes=classes, entity='Member Classes',
                               return_page='mem_classes')

    if request.method == 'POST':
        member = request.form['member']
        class_id = request.form['class']
        query = "SELECT class_total, class_max FROM Classes WHERE  class_id = %s;" % (class_id)
        cursor = db.execute_query(db_connection, query)
        check_cap = cursor.fetchone()
        if check_cap['class_total'] == check_cap['class_max']:  # make sure class isn't full
            # insert flash message here (class is at capacity)
            flash('sorry, this class is full', 'warning')
            print('class is full')
            return redirect('/mem_classes')
        query = "INSERT INTO Mem_Classes (member_id, class_id) VALUES (%s,%s);"
        data = (member, class_id)
        execute_query(db_connection, query, data)
        flash("Member's class was successfully added ", 'success')
        return redirect('/mem_classes')


@app.route('/update_mem_class', methods=['POST', 'GET'])
def update_mem_class():
    """ updates a member and class relationship, needs member_id and class_id """
    db_connection = db.connect_to_database()
    member_id = request.args.get('member_id')
    class_id = request.args.get('class_id')
    if request.method == 'GET':
        query = "SELECT f_name, l_name FROM Members WHERE member_id = %s ;" % (member_id)
        cursor = db.execute_query(db_connection, query)
        member = cursor.fetchone()
        query = "SELECT class_id, class_name FROM Classes;"
        cursor = db.execute_query(db_connection, query)
        classes = cursor.fetchall()
        print(member)
        return render_template('update_mem_class.html', member_id=member_id, member=member, classes=classes, curr_class_id=class_id, return_page='mem_classes', entity="Member's Classes")
    else:
        member_id = request.form['member_id']
        class_id = request.form['class_id']
        curr_class_id = request.form['curr_class_id']
        query = "UPDATE Mem_Classes SET member_id = %s, class_id = %s WHERE member_id = %s and class_id = %s;"
        data = (member_id, class_id, member_id, curr_class_id)
        execute_query(db_connection, query, data)
        flash("Member's class was successfully updated ", 'success')
        return redirect('mem_classes')


@app.route('/delete_mem_class')
def delete_mem_class():
    """ deletes member class relationship, expects class_id and member_id """
    class_id = request.args.get('class_id')
    member_id = request.args.get('member_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Mem_Classes WHERE member_id = %s and class_id = %s ;"
    data = (member_id, class_id)
    execute_query(db_connection, query, data)
    flash("Member's class was successfully deleted", 'success')
    return redirect('/mem_classes')

# -----------------End Mem_Classes------------------------------------------------------


# ------- Emp_Jobs add, update, delete and edit ------------------------
@app.route('/emp_jobs')
def emp_jobs():
    """ shows employee job relationship """
    db_connection = db.connect_to_database()
    query = 'SELECT d.dept_name, e.emp_id, e.f_name, e.l_name, j.job_description, j.job_id FROM Employees e LEFT JOIN Emp_Jobs ej ON ej.emp_id = e.emp_id LEFT JOIN Jobs j ON ej.job_id = j.job_id LEFT JOIN Departments d ON d.dept_id = j.dept_number WHERE j.job_description is NOT NULL;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_jobs.html', entity=results, page='Jobs', return_page='/jobs')


@app.route('/add_emp_jobs', methods=['POST','GET'])
def add_emp_jobs():
    """ adds an employee job relationship """
    db_connection = db.connect_to_database()

    if request.method == 'GET':
        dept_name = request.args.get('dept_name')
        job_id = request.args.get('job_id')
        query1 = "SELECT dept_id FROM Departments WHERE dept_name = '%s';" % (dept_name)
        cursor = db.execute_query(db_connection, query1)
        results = cursor.fetchone()
        dept_id = results['dept_id']
        query2 = "SELECT emp_id, f_name, l_name FROM Employees WHERE dept_number = %s;" % (dept_id)
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        employees = cursor.fetchall()
        query3 = "SELECT * FROM Jobs WHERE job_id = %s;" % (job_id)
        jobs = db.execute_query(db_connection=db_connection, query=query3)
        return render_template('add_emp_jobs.html', employee=employees, job=jobs)

    if request.method == 'POST':
        employee = request.form['employee']
        job = request.form['job']
        query = "INSERT INTO Emp_Jobs (emp_id, job_id) VALUES (%s,%s);"
        data = (employee, job)
        execute_query(db_connection, query, data)
        flash('employee was successfully assigned to a job', 'success')
        return redirect('/emp_jobs')
        # return render_template('success.html', action='Assignment was', entity='Emp_Jobs', active='other', return_page='emp_jobs')


@app.route('/update_emp_job', methods=['POST', 'GET'])
def update_emp_job():
    """ updates an employee job relationship, expects emp_id and job_id """
    db_connection = db.connect_to_database()
    emp_id = request.args.get('emp_id')
    job_id = request.args.get('job_id')
    if request.method == 'GET':
        query = "SELECT emp_id, f_name, l_name FROM Employees WHERE emp_id = %s ;" % (emp_id)
        cursor = db.execute_query(db_connection, query)
        employee = cursor.fetchone()
        query = "SELECT dept_number FROM Employees WHERE emp_id = %s;" % (emp_id)
        cursor = db.execute_query(db_connection, query)
        emp_dept = cursor.fetchone()
        emp_dept = emp_dept['dept_number']
        query = "SELECT job_id, job_description FROM Jobs WHERE dept_number = %s;" % (emp_dept)
        cursor = db.execute_query(db_connection, query)
        jobs = cursor.fetchall()
        return render_template('update_emp_job.html', employee=employee, jobs=jobs, curr_job_id=job_id,
                               return_page='emp_jobs', entity="Employee's Jobs")

    else:
        emp_id = request.form['emp_id']
        job_id = request.form['job_id']
        old_job_id = request.form['curr_job_id']
        query = "UPDATE Emp_Jobs SET emp_id = %s, job_id = %s WHERE emp_id = %s and job_id = %s;"
        data = (emp_id, job_id, emp_id, old_job_id)
        execute_query(db_connection, query, data)
        flash("employee's job was successfully updated", 'success')
        return redirect('emp_jobs')


@app.route('/delete_emp_job')
def delete_emp_job():
    """ deletes an employee job relationship expects a job_id and emp_id """
    job_id = request.args.get('job_id')
    emp_id = request.args.get('emp_id')
    db_connection = db.connect_to_database()
    query = "DELETE from Emp_Jobs WHERE emp_id = %s and job_id = %s ;"
    data = (emp_id, job_id)
    execute_query(db_connection, query, data)
    flash("Employee's job was successfully deleted", 'success')
    return redirect('/emp_jobs')


# -------------------End Emp_Jobs----------------------------------------------------


@app.route('/others')
def others():
    """ renders a page that links to the relational tables """
    return render_template('others.html')

# --------------- Additional views------------------------------------------------------------

@app.route('/job_emps')
def job_emps():
    """ this view shows a specific job and the employees associated with the job """
    job_id = request.args.get('job_id')
    db_connection = db.connect_to_database()
    query = 'SELECT e.emp_id, d.dept_name, e.f_name, e.l_name, j.job_description FROM Employees e LEFT JOIN Emp_Jobs ej ON ej.emp_id = e.emp_id LEFT JOIN Jobs j ON ej.job_id = j.job_id LEFT JOIN Departments d ON d.dept_id = j.dept_number WHERE j.job_description is NOT NULL and j.job_id = %s;' % (
        job_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    result = cursor.fetchall()
    if result is None:
        flash("No employees are assigned to this job", 'warning')
        return redirect('/jobs')
    else:
        return render_template('job_emps.html', entity=result, job_id=job_id, page='Jobs', return_page='/jobs')


@app.route('/emp_details')
def emp_details():
    """ shows an employee details expects an emp_id """
    emp_id = request.args.get('emp_id')
    db_connection = db.connect_to_database()
    query = 'SELECT * FROM Employees WHERE emp_id = %s;' % (emp_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('emp_details.html', entity = results, emp_id=emp_id, page='All Employees', return_page='/employees')


@app.route('/enrolled_classes')
def enrolled_classes():
    """ shows classes a member is enrolled in expects a member_id"""
    member_id = request.args.get('member_id')
    print(member_id)
    db_connection = db.connect_to_database()
    query = 'SELECT c.class_name, c.time, c.length FROM Members m LEFT JOIN Mem_Classes mc ON m.member_id = mc.member_id LEFT JOIN Classes c ON mc.class_id = c.class_id WHERE m.member_id = %s;' % (member_id)
    member = 'SELECT f_name, l_name FROM Members WHERE member_id = %s;' % (member_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor = db.execute_query(db_connection=db_connection, query=member)
    member = cursor.fetchall()
    return render_template('enrolled_classes.html', entity=results, member=member, return_page='/members', page='Members')


@app.route('/member_details')
def member_details():
    """ shows all a members details expects a member_id """
    member_id = request.args.get('member_id')
    db_connection = db.connect_to_database()
    query = 'SELECT * FROM Members WHERE member_id = %s;' % (member_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    print(results)
    return render_template('member_details.html', entity=results)


@app.route('/emp_dept')
def emp_dept():
    """ shows employees in a department, expects a dept_id and dept_name"""
    dept_id = request.args.get('dept_id')
    dept_name = request.args.get('dept_name')
    db_connection = db.connect_to_database()
    query = 'SELECT f_name, l_name FROM Employees WHERE dept_number = %s;' % (dept_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    if results == ():
        print(results)  # add flash message here
        flash("This department doesn't have any employees", 'warning')
        return redirect('/departments')
    else:
        return render_template('emp_dept.html', entity=results, dept_name=dept_name)


@app.route('/class_details')
def class_details():
    """ shows class details expects a class_id """
    db_connection = db.connect_to_database()
    class_id = request.args.get('class_id')
    query = "SELECT m.member_id, m.f_name, m.l_name from Members m LEFT JOIN Mem_Classes mc ON m.member_id = mc.member_id LEFT JOIN Classes c ON mc.class_id = c.class_id WHERE c.class_id = %s ;" % (
        class_id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('class_details.html', entity=results, class_id=class_id)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


if __name__ == "__main__":
    app.run(host='flip3.engr.oregonstate.edu', port=57455, debug=True)
