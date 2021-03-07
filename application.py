from flask import Flask, render_template,request,flash,session,url_for,redirect,session,jsonify,g
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm,TeacherRegistrationForm,EditProfileForm,EditTeacherProfile
from flask_mail import Mail
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_mysqldb import MySQL
import MySQLdb.cursors 
from flask_bcrypt import Bcrypt
from datetime import datetime, date	



application = Flask(__name__)
application.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '587',
    MAIL_USE_SSL = True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = 'studentassignmentportal12@gmail.com',
    MAIL_PASSWORD=  '181267174'
)
mail = Mail(application)
application.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://admin:admin123@databasedemo.cbgc16okl3ap.us-east-1.rds.amazonaws.com:3306/student'.format(user='admin', password='admin123', server='databasedemo.cbgc16okl3ap.us-east-1.rds.amazonaws.com', database='student')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['MYSQL_HOST'] = 'databasedemo.cbgc16okl3ap.us-east-1.rds.amazonaws.com'
application.config['MYSQL_USER'] = 'admin'
application.config['MYSQL_PASSWORD'] = 'admin123'
application.config['MYSQL_DB'] = 'student'
application.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(application) 
db = SQLAlchemy(application)
bcrypt=Bcrypt(application)


class Register(db.Model):
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Enrollment = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	Gender = db.Column(db.String(120),	nullable=False)
	birth = db.Column(db.String(12),	nullable=False)
	contact = db.Column(db.String(20),	nullable=False)
	semester = db.Column(db.String(120),	nullable=False)
	city = db.Column(db.String(120),	nullable=False)
	state = db.Column(db.String(120),	nullable=False)
	Address = db.Column(db.String(120),	nullable=False)
	pincode = db.Column(db.String(120),	nullable=False)
	password = db.Column(db.String(120),	nullable=False)
	confirm_password = db.Column(db.String(120),nullable=False)

class Teacherregister(db.Model):
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	Gender = db.Column(db.String(120),	nullable=False)
	birth = db.Column(db.String(12),	nullable=False)
	contact = db.Column(db.String(20),	nullable=False)
	department = db.Column(db.String(120),	nullable=False)
	qualifications = db.Column(db.String(120),	nullable=False)
	designation = db.Column(db.String(120),	nullable=False)
	Address = db.Column(db.String(120),	nullable=False)
	pincode = db.Column(db.String(120),	nullable=False)
	password = db.Column(db.String(120),	nullable=False)
	confirm_password = db.Column(db.String(120),nullable=False)

class Subjectdetail(db.Model):
	sname = db.Column(db.String(80),	unique=False,	nullable=False)
	scode = db.Column(db.String(80),	unique=False,	nullable=False)
	sem = db.Column(db.String(80),	unique=False,	nullable=False)
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)

@application.route("/")
def home():
    return render_template('index.html')

@application.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		name = request.form.get('name')
		email = request.form.get('email')
		Enrollment = request.form.get('Enrollment')
		Gender = request.form.get('Gender')
		birth = request.form.get('birth')
		contact = request.form.get('contact')
		semester = request.form.get('semester')
		city = request.form.get('city')
		state = request.form.get('state')
		Address = request.form.get('Address')
		pincode = request.form.get('pincode')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
		#cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		#cursor.execute('INSERT INTO register (name,email,Enrollment,Gender,birth,contact,semester,city,state,Address,pincode,password,confirm_password) VALUES ( % s, % s, % s, % s, % s, % s, % s, % s, % s,% s, % s, % s, % s)', (name,email,Enrollment,Gender,birth,contact,semester,city,state,Address,pincode,secure_password,secure_password,))
		entry = Register(name=name,email = email,Enrollment = Enrollment,Gender = Gender,birth= birth,contact=contact,semester = semester,city = city,state = state,Address = Address,pincode = pincode,password = secure_password,confirm_password=secure_password)
		db.session.add(entry)
		db.session.commit()
		mail.send_message('New message from Student Assignment Submission Portal' ,
                          sender='studentassignmentportal12@gmail.com',
                          recipients =[email] ,
                           body ="Thanks For Registering Us:" + name + "\n"  +  Enrollment + "\n" + contact
                          )
		flash(f'Account created for {form.email.data}!', 'success')
		return redirect(url_for('register'))
	return render_template('register.html', title='Register', form=form)

@application.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		email=request.form.get('email')
		password1 = request.form.get('password')
		#secure_password = bcrypt.generate_password_hash('password').decode('utf-8')
		#secure_pass = sha256_crypt.verify("password",secure_password)
		#secure_pass=bcrypt.check_password_hash(secure_password,password)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		result=cursor.execute('SELECT * FROM register WHERE email = % s ', [email])    
		if result>0:
			register = cursor.fetchone()
			password=register['password']
			if bcrypt.check_password_hash(password,password1):
				session['loggedin']=True
				session['email']=register['email'] 
				session['name']=register['name']
				session['Enrollment']=register['Enrollment']
				session['Gender']=register['Gender']
				session['birth']=register['birth']
				session['contact']=register['contact']
				session['semester']=register['semester']
				session['city']=register['city']
				session['state']=register['state']
				session['Address']=register['Address']
				session['pincode']=register['pincode']
				flash('You have been logged in!', 'success')
				return redirect(url_for('stsignup'))
				cursor.close() 
			else:
				flash('Password is incorrect','danger')
		else: 
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@application.route("/stsignup")
def stsignup():
	if g.email:
		return render_template('/StudentLogin/index.html',email=session['email'],name=session['name'],Enrollment=session['Enrollment'],Gender=session['Gender'],birth=session['birth'],contact=session['contact'],semester=session['semester'],city=['city'],state=session['state'],Address=session['Address'],pincode=session['pincode'])
	return redirect(url_for('login'))

@application.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
	if g.email:
		form = EditProfileForm(request.form)
		if form.validate_on_submit():
			session['email'] = form.email.data
			session['name'] = form.name.data
			session['Enrollment'] = form.Enrollment.data
			session['Gender'] = form.Gender.data
			session['birth'] = form.birth.data
			session['contact'] = form.contact.data
			session['semester'] = form.semester.data
			session['city'] = form.city.data
			session['state'] = form.state.data
			session['Address'] = form.Address.data
			session['pincode'] = form.pincode.data
		elif request.method == 'GET':
			form.email.data = session['email']
			form.name.data = session['name']
			form.Enrollment.data = session['Enrollment']
			form.Gender.data = session['Gender']
			form.contact.data = session['contact']
			form.semester.data = session['semester']
			form.city.data = session['city']
			form.state.data = session['state']
			form.Address.data = session['Address']
			form.pincode.data = session['pincode']
		return render_template('/StudentLogin/edit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('login'))

@application.route('/teacher_edit_profile', methods=['GET', 'POST'])
def teacher_edit_profile():
	if g.email:
		form = EditTeacherProfile(request.form)
		if form.validate_on_submit():
			g.email = form.email.data
			session['name'] = form.name.data
			session['Tid'] = form.Tid.data
			session['Gender'] = form.Gender.data
			session['birth'] = form.birth.data
			session['contact'] = form.contact.data
			session['department'] = form.department.data
			session['qualifications'] = form.qualifications.data
			session['designation'] = form.designation.data
			session['Address'] = form.Address.data
			session['pincode'] = form.pincode.data
		elif request.method == 'GET':
			form.email.data = g.email
			form.name.data = session['name']
			form.Tid.data = session['Tid']
			form.Gender.data = session['Gender']
			form.contact.data = session['contact']
			form.department.data = session['department']
			form.qualifications.data=session['qualifications']
			form.designation.data=session['designation']
			form.Address.data = session['Address']
			form.pincode.data = session['pincode']
		return render_template('/TeacherAdmin/tedit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('teacherlogin'))


@application.route("/logout3")
def logout3():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@application.route("/teacherlogin", methods=['GET', 'POST'])
def teacherlogin():
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		email=request.form.get('email')
		password1 = request.form.get('password')
		#secure_password = bcrypt.generate_password_hash('password').decode('utf-8')
		#secure_pass = sha256_crypt.verify("password",secure_password)
		#secure_pass=bcrypt.check_password_hash(secure_password,password)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		result=cursor.execute('SELECT * FROM teacherregister WHERE email = % s ', [email])    
		if result>0:
			register = cursor.fetchone()
			password=register['password']
			if bcrypt.check_password_hash(password,password1):
				session['loggedin']=True
				session['email']=register['email'] 
				session['name']=register['name'] 
				session['Tid']=register['Tid']
				session['Gender']=register['Gender']
				session['birth']=register['birth']
				session['contact']=register['contact']
				session['department']=register['department']
				session['qualifications']=register['qualifications']
				session['designation']=register['designation']
				session['Address']=register['Address']
				session['pincode']=register['pincode']
				flash('You have been logged in!', 'success')
				return redirect(url_for('teachersignup'))
				cursor.close() 
			else:
				flash('Password is incorrect','danger')
		else: 
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('teacherlogin.html', title='Login', form=form)
	
@application.route("/teachersignup")
def teachersignup():
	if g.email:
		return render_template('/TeacherAdmin/index.html',email=session['email'],name=session['name'],Tid=session['Tid'],Gender=session['Gender'],birth=session['birth'],contact=session['contact'],department=session['department'],qualifications=session['qualifications'],designation=session['designation'],Address=session['Address'],pincode=session['pincode'])
	return redirect(url_for('teacherlogin'))

@application.route("/logout2")
def logout2():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@application.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('login'))


@application.route("/contact")
def contact():
    return render_template('contact.html')



@application.route("/adminlogin",methods =['GET', 'POST'])
def adminlogin():
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		session.pop('email', None)
		email=request.form.get('email')
		password = request.form.get('password')
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		cursor.execute('SELECT * FROM admin WHERE email = % s AND password = % s', (email, password, )) 
		account = cursor.fetchone() 
		if account: 
			session['loggedin'] = True
			session['id'] = account['id'] 
			session['email'] = account['email'] 
			flash('You have been logged in!', 'success')
			return redirect(url_for('admindash'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('adminlogin.html',title='Login', form=form)

@application.route("/admindash")
def admindash():
	if g.email:
		return render_template('/ADMIN/index.html',email=session['email'])
	return redirect(url_for('adminlogin'))


@application.before_request
def before_request():
	g.email=None
	if 'email' in session:
		g.email=session['email']

@application.route('/logout1')
def logout1():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('adminlogin'))
	
@application.route("/teacheregister",methods =['GET', 'POST'])
def teacheregister():
	form = TeacherRegistrationForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		name = request.form.get('name')
		email = request.form.get('email')
		Tid = request.form.get('Tid')
		Gender = request.form.get('Gender')
		birth = request.form.get('birth')
		contact = request.form.get('contact')
		department = request.form.get('department')
		qualifications = request.form.get('qualifications')
		designation = request.form.get('designation')
		Address = request.form.get('Address')
		pincode = request.form.get('pincode')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
		entry = Teacherregister(name=name,email = email,Tid = Tid,Gender = Gender,birth= birth,contact=contact,department = department,qualifications = qualifications,designation = designation,Address = Address,pincode = pincode,password = secure_password,confirm_password=secure_password)
		db.session.add(entry)
		db.session.commit()
		mail.send_message('New message from Student Assignment Submission Portal' ,
                          sender='studentassignmentportal12@gmail.com',
                          recipients =[email] ,
                           body ="Thanks For Registering Us:" + name + "\n"  +  Tid  + "\n" + contact
                          )
		flash(f'Account created for {form.email.data}!', 'success')
		return redirect(url_for('teacheregister'))
	return render_template('teachergister.html',title='Teacherregister', form=form)



@application.route("/about")
def about():
    return render_template('about.html')


@application.route('/Addsubject',methods=["POST","GET"])
def Addsubject():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result = cur.execute("SELECT * FROM teacherregister ORDER BY Tid")
		carbrands = cur.fetchall()
		if request.method=='POST' :
			sname = request.form.get('sname')
			scode = request.form.get('scode')
			sem = request.form.get('sem')
			Tid = request.form.get('Tid')
			name = request.form.get('name')
			email = request.form.get('email')
			Add = Subjectdetail(sname=sname,scode=scode,sem=sem,Tid=Tid,name=name,email=email)
			db.session.add(Add)
			db.session.commit()
			mail.send_message('New message from Student Assignment Submission Portal' ,
                          sender='studentassignmentportal12@gmail.com',
                          recipients =[email] ,
                           body ="Your Subject Name is:--" + sname +"\t Subjet Code Is:" + scode +"\t for Semester:-- "  +  sem  + "\n And Your Professor Id is \t" + Tid
                          )
			flash(f'Subject Details are Successfully Added !', 'success')
		return render_template('/ADMIN/blank.html',carbrands=carbrands)
	return redirect(url_for('adminlogin'))		
 
@application.route("/carbrand",methods=["POST","GET"])
def carbrand():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM teacherregister WHERE Tid = %s ORDER BY Tid ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
                'name': row['name'],
                'email': row['email']}
            OutputArray.applicationend(outputObj)
    return jsonify(OutputArray)

@application.route("/studentprofile", methods=['GET', 'POST'])
def studentprofile():
	if g.email:
		form = RegistrationForm(request.form)
		return render_template('/StudentLogin/profile.html', title='Register', form=form)
	return redirect(url_for('login'))

@application.route("/teacherprofile", methods=['GET', 'POST'])
def teacherprofile():
	if g.email:
		form = TeacherRegistrationForm(request.form)
		return render_template('/TeacherAdmin/tprofile.html', title='Register', form=form)
	return redirect(url_for('teacherlogin'))

@application.route('/createassignment',methods=["POST","GET"])
def createassignment():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result = cur.execute("SELECT * FROM subjectdetail ORDER BY Tid")
		carbrands = cur.fetchall()
		return render_template('/TeacherAdmin/CreateAssignment.html',carbrands=carbrands)
	return redirect(url_for('teacherlogin'))

@application.route("/crassignment",methods=["POST","GET"])
def crassignment():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM subjectdetail WHERE Tid = %s ORDER BY Tid ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
				'sname': row['sname'],
                'name': row['name'],
                'email': row['email'],
				'sem':row['sem']}
            OutputArray.applicationend(outputObj)
    return jsonify(OutputArray)

@application.route("/crassignment1",methods=["POST","GET"])
def crassignments():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM subjectdetail WHERE sem = %s ORDER BY sem ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
				'sname': row['sname'],
                'name': row['name'],
                'email': row['email'],
				'sem':row['sem']}
            OutputArray.applicationend(outputObj)
    return jsonify(OutputArray)

@application.route('/showstudent')
def showstudent():
	cursor = mysql.connection.cursor()
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM register')
	data = cur.fetchall()
	cur.close()
	return render_template('/ADMIN/showstudent.html', employee = data)

@application.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
	form = EditProfileForm(request.form)
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM register WHERE id = %s', (id,))
	data = cur.fetchall()
	cur.close()
	print(data[0])
	return render_template('/ADMIN/edit_student.html', employee = data[0],form=form)
 
@application.route('/update/<id>', methods=['POST'])
def update_employee(id):
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		Enrollment = request.form['Enrollment']
		Gender = request.form['Gender']
		birth = request.form['birth']
		contact = request.form['contact']
		semester = request.form['semester']
		city = request.form['city']
		state = request.form['state']
		Address = request.form['Address']
		pincode = request.form['pincode']
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("UPDATE register SET name = %s,email = %s,Enrollment=%s,Gender=%s,birth=%s,contact = %s,semester=%s,city=%s,state=%s,Address=%s,pincode=%s,WHERE id = %s", (name, email,Enrollment,Gender,birth,contact,semester,city,state,Address,pincode, id))
		flash('Student Data Updated Successfully')
		
		return redirect(url_for('showstudent'))
 
@application.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM register WHERE id = {0}'.format(id))
    flash('Student Data Removed Successfully')
    return redirect(url_for('showstudent'))

application.secret_key="12345678"


if __name__ == '__main__':
	application.debug = True
	application.run()

