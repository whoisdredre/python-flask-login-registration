from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ThisISSecret"
mysql = MySQLConnector('users1')

@app.route('/')
def index():
	return render_template('index.html')
@app.route('/login', methods=['POST'])
def login():
	email = request.form['my_email']
	user_query = ("SELECT * FROM user WHERE email = :email LIMIT 1")
	query_data = { 'email': email}
	password = request.form['password']
	user = mysql.query_db(user_query, query_data)
	
	if bcrypt.check_password_hash(user[0]['password'], password):
		return render_template('reg.html')
	else:
		flash('invalid email or password')
		session['email'] = email
		return redirect('/')
#login doesnt work. i tried several times to fix it.

@app.route('/register', methods=['POST'])
def register():
	fname= request.form['first_name']
	lname= request.form['last_name']
	email= request.form['email']
	password= request.form['password']

	pw_hash = bcrypt.generate_password_hash(password)

	query = "INSERT INTO user(first_name, last_name, email, password, created_at) VALUES (:first_name, :last_name, :email, :password, NOW())"
	data = {
	'first_name': fname,
	'last_name': lname,
	'email': email,
	'password': pw_hash
	}

	mysql.query_db(query,data)
	session['email'] = request.form['email']
	return render_template('reg.html')

app.run(debug=True)