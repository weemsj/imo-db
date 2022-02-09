from flask import Flask, render_template
import os

# configuration 
 
app = Flask(__name__)
 
 # Routes
 
@app.route('/')
def root():
    return render_template('main.j2')

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
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)