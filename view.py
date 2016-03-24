#-*- coding: utf-8 -*-
#encoding=utf-8
from flask import Flask,render_template,url_for,request,flash,redirect,session
from flask_sqlalchemy import SQLAlchemy
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.secret_key = 'my is  some_secret'

# app.config['SESSION_TYPE'] = 'filesystem'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/dutylist'
db = SQLAlchemy(app)


class Category(db.Model):
	__tablename__ = "du_category"
	category_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Category %r>' % self.name

class User(db.Model):
	__tablename__ = "du_user"
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	phone = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(64), unique=True)
	create_time = db.Column(db.Integer, unique=True)
	
	def __init__(self, username,phone,password,create_time):
		self.username = username
		self.phone = phone
		self.password = password
		self.create_time = create_time

	def __repr__(self):
		return self.username

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():

    return render_template('login.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
	error = None
	if request.method == "POST":
		username = request.form['username']
		phone = request.form['phone']
		password = request.form['password']
		repassword = request.form['repassword']

		if username or phone or password or repassword:
			if password != repassword:
				flash('Password and Confirm Password not same')
				return redirect(url_for('register'))
			res = User.query.filter_by(phone=phone).first()
			if res:
				flash('phone is be register')
				return redirect(url_for('register'))
			data = User(username,phone,password,time.time())
			res = db.session.add(data)
			db.session.commit()
			if data.user_id:
				flash('register successfully! please login')
				return redirect(url_for('login'))
			else:
				flash('register error!')
				return redirect(url_for('register'))
		else:
			flash('字段不能为空')
			return redirect(url_for('register'))
	else:
		return render_template('register.html')

@app.route('/add_duty')
def add_duty():
    return render_template('add_duty.html')
@app.route('/my_duty')
def my_duty():
    return render_template('my_duty.html')

@app.route('/add_category',methods=['GET', 'POST'])
def add_category():
    category = Category.query.all()
    print category
    error = None
    if request.method == 'POST':
        name = request.form['category[name]']
        print name
        if name is None:
        	error = 'name not None!'
        	return render_template('add_category.html',error=error)
        else:
        	flash('You were successfully logged in')
        	return redirect(url_for('my_duty'))
    return render_template('add_category.html')
@app.errorhandler(404) 
def page_not_found(e): 
    return render_template('404.html'), 404 
@app.errorhandler(500) 
def internal_server_error(e): 
    return render_template('500.html'), 500

if __name__ == '__main__':
	app.debug = True
	app.run()