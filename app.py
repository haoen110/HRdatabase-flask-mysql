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
cur = connection.cursor()


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
    return render_template('index.html')


# hrForm Class, Please add more attributes here! including dept's attr and contract's attr
class HRForm(Form):
    eid = IntegerField('Eid', [validators.DataRequired()])
    ename = StringField('Name', [validators.Length(min=1)])
    gender = StringField('Gender', [validators.Length(min=1)])
    age = IntegerField('Age', [validators.DataRequired()])
    salary = IntegerField('Salary', [validators.DataRequired()])
    department = StringField('Department', [validators.Length(min=1)])
    address = StringField('Address', [validators.Length(min=1)])

# Recruitment Page (for addition and deletion of employees)
@app.route('/recruitment.html', methods=['GET', 'POST'])
@is_logged_in
def recruitment():
    cur = db.engine.raw_connection().cursor()
    cur.execute("SELECT * FROM employees;")
    employees = cur.fetchall()
    return render_template('recruitment.html', employees=employees)

# Emp Addition
@app.route('/add_employee', methods=['POST'])
@is_logged_in
def add_employee():
    form = HRForm(request.form)
    if request.method == 'POST' and form.validate():
        eid = form.eid.data
        ename = form.ename.data
        gender = form.gender.data
        age = form.age.data
        salary = form.salary.data
        department = form.department.data
        try:
            db.engine.execute("INSERT INTO employees(eid, ename, gender, age, salary, department) VALUES (%s, %s, %s, %s, %s, %s)",
                        (eid, ename, gender, age, salary, department))
        except:
            flash('Insert Unsuccessfully, Please Check Again!', 'danger')
            return redirect(url_for('recruitment'))
        flash('Insert Successfully!', 'success')
        return redirect(url_for('recruitment'))
    return render_template('recruitment.html', form=form)

# Emp Deletion
@app.route('/recruitment.html/<string:eid>', methods=['GET', 'POST'])
@is_logged_in
def delete_employee(eid):
    if request.method == 'POST':
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
    return render_template('employee.html', employees=employees)

# Selection of Employee
@app.route('/search_employee', methods=['POST', 'GET'])
@is_logged_in
def search_employee():
    form = HRForm(request.form)
    eid = form.eid.data
    ename = form.ename.data
    gender = form.gender.data
    department = form.department.data
    address = form.address.data
    cur = db.engine.raw_connection().cursor()
    if eid is not None:
        cur.execute("select * from employees where eid =%d;" % eid)
    else:
        cur.execute("select * from employees \
                     where ename like '%%%s%%'\
                     and gender like '%%%s%%'\
                     and department like '%%%s%%'\
                     and address like '%%%s%%';"
                    % (ename, gender, department, address))
    employees = cur.fetchall()
    flash('Search Successfully!', 'success')
    return render_template('employee.html', employees=employees)

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
    cur.execute("SELECT * FROM contracts;")
    contracts = cur.fetchall()
    return render_template('contract.html', contracts=contracts)


# Attendance Page (Red One)
@app.route('/attendance.html', methods=['GET', 'POST'])
@is_logged_in
def attendance():
    cur = db.engine.raw_connection().cursor()
    cur.execute("SELECT * FROM attendance_owned;")
    attendances = cur.fetchall()
    return render_template('attendance.html', attendances=attendances)


if __name__ == "__main__":
    app.secret_key = '123'
    app.run(debug=True)
    print("Server is running...")









# @app.route('/charts.html')
# @is_logged_in
# def charts():
#     return render_template('charts.html')

# @app.route('/tables.html')
# @is_logged_in
# def tables():
#     return render_template('tables.html')

# # Article Form Class
# class ArticleForm(Form):
#     title = StringField('Title', [validators.Length(min=1)])
#     body = TextAreaField('Body', [validators.Length(min=1)])
#
#
# @app.route('/table1.html', methods=['GET', 'POST'])
# @is_logged_in
# def table1():
#     cur = db.engine.raw_connection().cursor()
#     cur.execute("SELECT * FROM articles;")
#     articles = cur.fetchall()
#     return render_template('table1.html', articles=articles)
#
#
# @app.route('/add_article', methods=['POST'])
# @is_logged_in
# def add_article():
#     form = ArticleForm(request.form)
#     if request.method == 'POST' and form.validate():
#         title = form.title.data
#         body = form.body.data
#         db.engine.execute("INSERT INTO articles(title, body, transactor) VALUES (%s, %s, %s)",
#                     (title, body, session['username']))
#         flash('Insert Successfully!', 'success')
#         return redirect(url_for('table1'))
#     return render_template('table1.html', form=form)