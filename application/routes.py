import requests
from application import app
from flask import render_template,request


@app.route('/')
@app.route('/login')
def login():
	return render_template("login.html",login=True)


@app.route('/home',methods=['POST'])
def home():
	username = request.form['username']
	password = request.form['password']
	# calling login api
	url ="https://abchospitalmanagement.herokuapp.com/auth"
	data={"username": username, "password": password}
	response = requests.post(url, json=data,headers={"Content-Type": "application/json"})
	print("hi")
	print(response.text)
	return render_template("home.html",register=True)