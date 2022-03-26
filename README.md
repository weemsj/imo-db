# imo-db
This website is created to be used by administration of a fictional fitness company. The administration will be able to CRUD all employees, members, classes, jobs, certifications and departments. 
Web app is avalible to view [here]
(http://imofitness.link:5000/).

Full Executive Summary, Project outline, ERD, and Database Schema avalible at [via Google Doc]
(https://docs.google.com/document/d/1G2f5M1lUuk-ZJ2exV9qsRDDLrh7t_7ckrPgzn6TWXds/edit?usp=sharing/).


Executive Summary
	Over the course of this quarter we kept the core project idea and structure consistent, making improvements at each step inspired by our peers and our own explorations. Some of those improvements include changes to data types, user interfaces, relationships, constraints, and business rules:
	Early in our project we were using varchar (1) for the gender, expecting “M” or “F” for male or female. A peer reviewer (James Bush) recommended considering an input for those employees and members who don’t identify as male or female, so we adjusted the data type to ENUM(‘MALE’, ‘FEMALE’, ‘NONBINARY’) for a more inclusive gender field. Using ENUM also helps keep the database normalized to the preselected options. 
On the user interface side we have made several iterative changes. One peer reviewer recommended that our tables show more meaningful data, so that users don’t need to have two windows open to cross reference primary keys (IDs) with names and other details. To improve this we decided to use generalized queries on the entity pages, with links to more detailed queries or customized views that could be helpful for users looking for specific information. For example, if a user navigates to the Employees page they will see a list of all employees at IMO-Fitness, including both ‘ACTIVE’ and ‘NOT ACTIVE’ employees. There are links on this page to view “details” for a given employee id (emp_id), utilizing a SELECT statement. There is also a link to view the jobs that a specific employee is assigned to, for additional user convenience. To keep the navigation bar neat, we moved links to composite tables to the ‘Others’ page. 
The relationships haven’t changed much from the beginning, with the exception of combing through the outline to see which would benefit from being NULLable. One such relationship is the link between Departments and Employees - we updated the site so that when a user edits an employee, they can make the relationship with a Department NULL by simply adding an end date, thereby also making the employee ‘NOT ACTIVE’. We have also added some constraints and triggers to the database. Many of these triggers deal with the department and class total count fields - to be updated when an employee or member is deleted, added, or updated. These were changes that were identified as needed by us and our peer reviewers. 
The main business rule change that was implemented relates to the Employees and Departments. Initially, an employee could be related to zero or more Departments, the zero pertaining to when an employee status is ‘NOT ACTIVE’. Departments were required to have at least one Employee. We found that if a department was deleted it would potentially leave many employees without a relationship to a Department - getting around this would require removing all Employees from a Department before deleting the Department required. As this was against our initial scheme, we changed the relationship to allow Departments to have zero or more employees. 
Project and Database Outline								
	IMO Fitness (IMO) is a St. Louis based fitness facility that is strategically positioned on the state line of Illinois and Missouri. IMO first opened its doors in 2001 as a small fitness studio. The fitness center has since expanded from 5 employees and 15 members operating out of a 3,200 sq ft store front to currently employing 62 staff members and over 1500 members in a 32,000 sq ft stand alone fitness facility. At any time IMO can expect to have 10% of its members in attendance, either participating in classes, group training, individual training or working out on their own. With the increased staffing IMO has divided its employees into 6 departments, including training, wellness, maintenance, member experience, operations and director. The training staff have combined expertise and certifications in NASM-CPT, sports specific training (FMS), Pilates, Yoga, CROSSFIT, Swimming, ISSA, and nutrition. The maintenance employees have combined certifications in electrictrical, plumbing, hvac and RRP. IMO training and wellness Employees can instruct group or individual Classes for Members to attend. Each department manager is responsible for assigning Employees to Jobs. 

Currently IMO is still using the same system to keep track of its Customers, Employees and operations as it did when it first opened its doors in 2001. The inefficiencies of their current system have resulted in overbooked classes, trainers instructing the wrong classes, idle employees, and members double booking themselves for classes To prevent these issues from occurring in the future, IMO is in need of a database system that can effectively keep track of its Members and the Classes they attend, Classes and is members and instructors, Employees and the Jobs they are assigned to, Employees and their Certifications, and the Departments its Employees. The database needs to be growth and future proof with the hopes that the company continues to grow. 


Project Outline 
Departments: represents the different departments at IMO Gym
dept_id: int, auto_increment, unique, not NULL, PK
dept_name: varChar(25), not NULL, one of the following, corresponds 1:1 with dept_id:
training
wellness
maintenance
member_experience
operations
director
dept_total: <<derived from Employees>> int, not NULL
Relationships:
1:M relationship between the Jobs entity and the Departments entity, where a job must belong to one department but a department can have zero or more jobs. Department → dept_id is a  FK in Jobs. (Nullable relationship)
1:M relationship between Departments and Employees entities, where an employee can belong to zero or one department but a department can have zero or more employees, a dept_id is a FK inside of the Employees entity. (Nullable relationship)

Employees: records employee details
emp_id: int, auto_increment, unique, not NULL, PK
f_name: varChar(50), not NULL
l_name: varChar(50), not NULL
gender: varChar(9), not NULL
address_1: varChar(46), not NULL
address_2: varChar(46)
city: varChar(50), not NULL
state: Char(2), not NULL
zip:  Char(5), not NULL
tel: Char(12), not NULL
emall: varChar(50), not NULL
start_day: date, not NULL
end_day: date
If NULL employee is active employee
status: ENUM(‘ACTIVE’,’NOT ACTIVE’)
dept_number: int, not NULL, FK (Departments - dept_id)
Relationships: 
1:M relationship between Employees and Departments, where an employee must work in zero or one department and a department must have zero or more employee(s). A department is a FK inside of the Employees entity. (Nullable Relationship)
M:M relationship between the Employees entity and the Certifications entity, where an employee can have zero to many certifications and a certification can be held by zero to many employees, this relationship is demonstrated in composite entity Emp_Certs, if Employees → cert attribute is NULL the relationship is NULL.
1:M relationship between the Employees entity and the Classes entity where an employee (see constraints) can instruct zero to many classes but a class must  be taught by only one employee, Employees → emp_id attribute is a FK in Classes entity.
M:M relationship between the Jobs entity and the Employees entity, where a job can be assigned to zero or many employees and an employee can be assigned to many jobs. This relationship will be demonstrated within a composite entity Emp_Jobs if no employees are assigned to a job then the relationship is NULL.

Certifications: represents the different certifications IMO employees have
cert_id: int, auto_increment, unique, not NULL, PK
cert_name: varChar(50), not NULL, one of the following:


NASM-CPT
FMS
Pilates
Yoga
CrossFit
Swimming
ISSA
Electrical
Plumbing
Hvac
RRP
Nutrition


Relationships:
M:M relationship between the Certifications entity and the Employees entity, where zero to many employees can be certified in any discipline and a certification can be held by zero to many employees. This relationship will be demonstrated within a composite entity Emp_Certs if no employee is certified then the relationship is NULL. 

Emp_Certs: represents the relationship between Employees and Certifications if no employees are certified, the relationship is NULL.
emp_id:int, FK(Employees-emp_id),PK
cert_id:int, FK(Certifications-cert_id),PK

Jobs: represents jobs employees can be assigned to
job_id: int, auto_increment, unique, not NULL, PK
dept_number: int, not NULL (FK Departments - dept_id)
job_description: mediumtext 
Relationships:
1:M relationship between the Jobs entity and the Departments entity, where a job must belong to one department but a department can have zero or many jobs. Department → dept_id is  a FK in Jobs.
M:M relationship between the Jobs entity and the Employees entity, where a job can be assigned to zero or many employees and an employee can be assigned to many jobs. This relationship will be demonstrated within a composite entity Emp_Jobs if no employees are assigned to a job then the relationship is NULL.

Emp_Jobs: represents the relationship between Employees entity and Jobs entity. If no employees are assigned to jobs, the relationship is NULL.
emp_id: int, not NULL, FK(Employees - emp_id),PK
job_id: int, not NULL, FK(Jobs- job_id),PK

Classes: represents the classes that are offered by the gym
class_id: int, auto_increment, unique, not NULL
class_name: varChar(50), not NULL
instructor: int, not NULL, FK( Employees - emp_id)
Constraints- employee must be apart of the training or wellness department
time: TIME, not NULL
Stores class start time in 24H time, local time assumed (US-CST)
length: int, not NULL
Stores class length in minutes
class_total:<<derived from Members>> int
If total is NULL class is empty
Derived from number of members, if = 1 then the class is an individual training session
class_max: int, not Null
Relationships:
1:M relationship between the Classes entity and the Employees entity, where an employee(see constraints) can instruct zero to many classes and a class must be led by one instructor, Employees → emp_id attribute is a FK inside of classes.
M:M relationship between the Classes entity and the Members entity, where a member can take zero to many classes, and a class can have zero to many members. This relationship will be demonstrated within a composite entity where Members → member_id and Classes → class_id attributes are FKs in Mem_Classes if there are zero members in a class the relationship between a class and members is NULL. 

Members: represents all current and past members of IMO fitness
member_id: int, auto_increment, unique, not NULL
f_name: varChar(50), not NULL
l_name: varChar(50), not NULL
gender:  ENUM(‘MALE’, ‘FEMALE’,NONBINARY’), not NULL
address_1: varChar(46), not NULL
address_2: varChar(46)
city: varChar(50), not NULL
state: Char(2), not NULL
zip:  char(5)
tel: Char(12), not NULL
email: varChar(50), not NuLL
status: ENUM(‘ACTIVE’,NOT ACTIVE’) not NULL
Relationships
M:M relationship between the Members entity and the Classes entity, where a member can take zero to many classes and a class can have zero to many members. This relationship is demonstrated within the composite entity Mem_Classes where Members →  member_id and Classes → class_id attributes are FKs. This relationship can be NULL. 

Mem_Classes: shows the relationship between all Classes and Members enrolled in them if there are zero members enrolled in classes the relationship is NULL.
member_id: int,FK(Members-member_id),PK
class_id: int,FK(Classes-class_id),PK
