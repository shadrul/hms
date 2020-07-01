import requests
from application import app
from flask import render_template, request, redirect, session, url_for, flash


@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	if not session.get('token'):
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']
			# calling login api
			url ="https://abchospitalmanagement.herokuapp.com/auth"
			data={"username": username, "password": password}
			response = requests.post(url, json=data,headers={"Content-Type": "application/json"})
			print(response.status_code)
			if(response.status_code==401):
				return redirect(url_for('login'))
				# return render_template("login.html")
			else:
				print(response.json())
				r = response.json()
				token = r['access_token']
				session['token']=token
				return render_template("home.html",access= token)

		return render_template("login.html")
	else:
		token = session.get('token')
		return render_template("home.html",access= token)



@app.route('/home')
def home():
	# username = request.form['username']
	# password = request.form['password']
	# # calling login api
	# url ="https://abchospitalmanagement.herokuapp.com/auth"
	# data={"username": username, "password": password}
	# response = requests.post(url, json=data,headers={"Content-Type": "application/json"})
	# print(response.status_code)
	# if(response.status_code==401):
	# 	return redirect(url_for('login'))
	# 	# return render_template("login.html")
	# else:
	# 	print(response.json())
	# 	r = response.json()
	# 	token = r['access_token']
	return render_template("home.html")


# registration page
@app.route('/patient_registration',methods=['GET','POST'])
def patient_registration():
	if not session.get('token'):
		return redirect(url_for('login'))
	else:
		if request.method == 'POST':
			patientSSNID = request.form['patientSSNID']
			patientName = request.form['patientName']
			patientAge = request.form['patientAge']
			doa = request.form['doa']
			tob = request.form['tob']
			address = request.form['address']
			state = request.form['state']
			city = request.form['city']
			token = session.get('token')
			url ="https://abchospitalmanagement.herokuapp.com/patient"
			data={"patientSSNId": patientSSNID, "patientName": patientName,"patientAge": patientAge, "doa": doa, "tob": tob, "address": address, "state": state, "city": city}
			print("JWT "+token)
			response = requests.post(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			if(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))
			else:
				print(response)
				print(response.text)
				flash("Patient Registered Successfully.","success")
			# return redirect(url_for('patient_registration'))
		return render_template('patient_registration.html')

	return render_template('patient_registration.html')