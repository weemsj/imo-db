from flask import Flask, render_template
import os

# configuration 
 
app = Flask(__name__)

# database connection

# app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
# app.config['MYSQL_USER'] = 'cs340_weemsj'
# app.config['MYSQL_PASSWORD'] = '8924' #last 4 of onid
# app.config['MYSQL_DB'] = 'cs340_weemsj'
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"

#mysql = MySQL(app)

 
 # Routes
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/departments')
def departments():
    return render_template('departments.html')

@app.route('/employees')
def employees():
    return render_template('employees.html')

@app.route('/certifications')
def certifications():
    return render_template('certifications.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/classes')
def classes():
    return render_template('classes.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/emp_dept')
def emp_dept():
    return render_template('relational_tables.j2')

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
    port = int(os.environ.get('PORT', 57457))
    app.run(port=port, debug=False)