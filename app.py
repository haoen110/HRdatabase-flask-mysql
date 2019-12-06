import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, request, redirect, url_for, logging, session
from wtforms import Form, StringField, TextAreaField, PasswordField, IntegerField, validators
from passlib.hash import sha256_crypt
from functools import wraps

# Config Application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/sdsc5003'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db = SQLAlchemy(app)
connection = db.engine.raw_connection()


# Create registration form
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords do not match.')])
    confirm = PasswordField('Confirm password')


# Registration Page
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.hash(str(form.password.data))
        # Execute MySQL
        cur = db.engine.raw_connection().cursor()
        cur.execute("SELECT * FROM users WHERE username = %s;", username)
        result = cur.fetchone()
        if result is not None:
            flash('Username Existed.', 'danger')
            return render_template('register.html', form=form)
        db.engine.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s);",
                          (username, email, password))
        flash('Registered Successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    session['logged_in'] = False
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = db.engine.raw_connection().cursor()
        cur.execute("SELECT * FROM users WHERE username = %s;", username)
        result = cur.fetchone()
        print(result)
        if result is not None:
            # Get stored has
            password = result[3]
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Wrong Password.', 'danger')
        else:
            flash('Wrong Username.', 'danger')
    return render_template('login.html')


# Forget Password Page
@app.route('/forgot-password.html')
def forgot_password():
    return render_template('forgot-password.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['logged_in']:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login!', 'danger')
            return redirect(url_for('login'))

    return wrap


# Index
@app.route('/index.html')
@is_logged_in
def index():
    cur = db.engine.raw_connection().cursor()
    cur.execute('''select * from departments,
                (select emp.department, count(emp.eid) as Total
                from employees emp
                group by emp.department
                order by emp.department) as tp
                where departments.dname = tp.department;''')
    departments = cur.fetchall()
    # Enrolled Line Plot
    df = pd.read_sql("""
            select start_date
            from contracts""", connection)
    df['start_date'] = pd.to_datetime(df['start_date'])
    l1 = pd.date_range(start=df['start_date'].min(), end=df['start_date'].max(), freq='M').strftime('%m/%d/%Y')
    l2 = list(df['start_date'].groupby(df.start_date.dt.to_period("M")).agg('count').values.astype(int))
    return render_template('index.html', departments=departments, l1=l1, l2=l2)


# hrForm Class, Please add more attributes here! including dept's attr and contract's attr
class HRForm(Form):
    eid = IntegerField('Eid', [validators.DataRequired()])
    cid = IntegerField('Cid', [validators.DataRequired()])
    ename = StringField('Name', [validators.Length(min=1)])
    gender = StringField('Gender', [validators.Length(min=1)])
    age = IntegerField('Age', [validators.DataRequired()])
    salary = IntegerField('Salary', [validators.DataRequired()])
    department = StringField('Department', [validators.Length(min=1)])
    address = StringField('Address', [validators.Length(min=1)])
    start = StringField('Start Date', [validators.DataRequired()])
    end = StringField('End Date', [validators.DataRequired()])


# Recruitment Page (for addition and deletion of employees)
@app.route('/recruitment.html', methods=['GET', 'POST'])
@is_logged_in
def recruitment():
    cur = db.engine.raw_connection().cursor()
    cur.execute('''select employees.eid, cid, ename, gender, age, salary, department
                   from employees, contracts
                   where employees.eid=contracts.eid''')
    employees = cur.fetchall()
    cur = db.engine.raw_connection().cursor()
    cur.execute("SELECT dname FROM departments;")
    departments = cur.fetchall()
    l = []
    for i in departments:
        l.append(i[0])
    departments = l
    return render_template('recruitment.html', employees=employees, departments=departments)


# Emp Addition
@app.route('/add_employee', methods=['POST', 'GET'])
@is_logged_in
def add_employee():
    form = HRForm(request.form)
    eid = form.eid.data
    cid = form.cid.data
    ename = form.ename.data
    gender = form.gender.data
    age = form.age.data
    salary = form.salary.data
    department = request.form['departments']
    address = form.address.data
    start = form.start.data
    end = form.start.data
    dd = {'Security Department': '1',
          'Financial Department': '2',
          'Official Department': '3',
          'Peace Hotel': '4',
          'Exhibition Center': '5',
          'Support Department': '6',
          'Property Department': '7'}
    print("**************", eid, cid, ename, gender, age, salary, department, address, start, end)
    # Exist or Not
    cur = db.engine.raw_connection().cursor()
    cur.execute("SELECT * FROM employees WHERE eid = %s;", eid)
    result = cur.fetchone()
    if result is not None:
        flash('Eid Existed.', 'danger')
        # return render_template('recruitment.html', form=form, employees=employees, departments=departments)
        return redirect(url_for('recruitment'))
    # Integer format or Not
    if type(eid) and type(cid) and type(age) and type(salary) != type(1):
        flash('Eid and Cid must be integer, Please Check Again!', 'danger')
        return redirect(url_for('recruitment'))
    try:
        db.engine.execute('''
                insert into employees(eid, ename, gender, age, salary, department, address)
                values(%s, %s, %s, %s, %s, %s, %s);
                ''', (eid, ename, gender, age, salary, department, address))
        db.engine.execute('''
                        insert into contracts(cid, eid, did, start_date, finish_date)
                        values(%s, %s, %s, %s, %s);
                        ''', (cid, eid, dd[department], start, end))
        print("**************", eid, cid, ename, gender, age, salary, department, address, start, end)
    except:
        flash('Insert Unsuccessfully, Please Check Again!', 'danger')
        return redirect(url_for('recruitment'))
    flash('Insert Successfully!', 'success')
    return redirect(url_for('recruitment'))


# Emp Deletion
@app.route('/recruitment.html/<string:eid>', methods=['GET', 'POST'])
@is_logged_in
def delete_employee(eid):
    if request.method == 'POST':
        db.engine.execute("DELETE FROM contracts WHERE eid = %s", [eid])
        db.engine.execute("DELETE FROM employees WHERE eid = %s", [eid])
        flash('Delete Successfully!', 'success')
        return redirect(url_for('recruitment'))


# Employee Page (Blue One)
@app.route('/employee.html', methods=['GET', 'POST'])
@is_logged_in
def employee():
    cur = db.engine.raw_connection().cursor()
    cur.execute("SELECT * FROM employees;")
    employees = cur.fetchall()
    cur = db.engine.raw_connection().cursor()
    cur.execute("SELECT dname FROM departments;")
    departments = cur.fetchall()
    l = []
    for i in departments:
        l.append(i[0])
    # print(l)
    departments = l
    return render_template('employee.html', employees=employees, departments=departments)


# Selection of Employee
@app.route('/search_employee', methods=['POST', 'GET'])
@is_logged_in
def search_employee():
    form = HRForm(request.form)
    eid = form.eid.data
    ename = form.ename.data
    gender = form.gender.data
    department = request.form['departments']
    address = form.address.data
    # list of dept.
    cur = db.engine.raw_connection().cursor()
    cur.execute("SELECT dname FROM departments;")
    departments = cur.fetchall()
    l = []
    for i in departments:
        l.append(i[0])
    # print(l)
    departments = l
    # search
    cur = db.engine.raw_connection().cursor()
    if eid is not None:
        # print(eid)
        cur.execute("select * from employees where eid =%d;" % eid)
    elif gender == 'flag':
        cur.execute("select * from employees \
                     where ename like '%%%s%%'\
                     and department like '%%%s%%'\
                     and address like '%%%s%%';"
                    % (ename, department, address))
    else:
        cur.execute("select * from employees \
                     where ename like '%%%s%%'\
                     and gender = '%s'\
                     and department like '%%%s%%'\
                     and address like '%%%s%%';"
                    % (ename, gender, department, address))
    employees = cur.fetchall()
    flash('Search Successfully!', 'success')
    return render_template('employee.html', employees=employees, departments=departments)


# Department Page (Yellow One)
@app.route('/department.html', methods=['GET', 'POST'])
@is_logged_in
def department():
    cur = db.engine.raw_connection().cursor()
    cur.execute('''select * from departments,
            (select emp.department, count(emp.eid) as Total
            from employees emp
            group by emp.department
            order by emp.department) as tp
            where departments.dname = tp.department;''')
    departments = cur.fetchall()
    return render_template('department.html', departments=departments)


# Contract Page (Green One)
@app.route('/contract.html', methods=['GET', 'POST'])
@is_logged_in
def contract():
    cur = db.engine.raw_connection().cursor()
    cur.execute('''
        select cid, contracts.eid, ename, employees.department, contracts.start_date, contracts.finish_date
        from employees, contracts
        where employees.eid = contracts.eid;''')
    contracts = cur.fetchall()
    df = pd.read_sql("""
        select start_date
        from contracts""", connection)
    df['start_date'] = pd.to_datetime(df['start_date'])
    l1 = pd.date_range(start=df['start_date'].min(), end=df['start_date'].max(), freq='M').strftime('%m/%d/%Y')
    l2 = list(df['start_date'].groupby(df.start_date.dt.to_period("M")).agg('count').values.astype(int))
    return render_template('contract.html', contracts=contracts, l1=l1, l2=l2)


# Attendance Page (Red One)
@app.route('/attendance.html', methods=['GET', 'POST'])
@is_logged_in
def attendance():
    cur = db.engine.raw_connection().cursor()
    cur.execute('''select aid, ename, on_work, off_work
                   from employees, attendance_owned
                   where employees.eid=attendance_owned.eid;''')
    attendances = cur.fetchall()
    return render_template('attendance.html', attendances=attendances)


if __name__ == "__main__":
    app.secret_key = '123'
    app.run(debug=True)
    print("Server is running...")
