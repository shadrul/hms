import requests
from application import app
from flask import render_template, request, redirect, session, url_for, flash
from application.forms import LoginForm,UpdateForm, getData


@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if not session.get('token'):
		if form.validate_on_submit():
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
				return redirect(url_for("home"))

		return render_template("login.html",form=form)
	else:
		token = session.get('token')
		return redirect(url_for("home"))


	# if not session.get('token'):
	# 	if request.method == 'POST':
	# 		username = request.form['username']
	# 		password = request.form['password']
	# 		# calling login api
	# 		url ="https://abchospitalmanagement.herokuapp.com/auth"
	# 		data={"username": username, "password": password}
	# 		response = requests.post(url, json=data,headers={"Content-Type": "application/json"})
	# 		print(response.status_code)
	# 		if(response.status_code==401):
	# 			return redirect(url_for('login'))
	# 			# return render_template("login.html")
	# 		else:
	# 			print(response.json())
	# 			r = response.json()
	# 			token = r['access_token']
	# 			session['token']=token
	# 			return render_template("home.html",access= token)

	# 	return render_template("login.html")
	# else:
	# 	token = session.get('token')
	# 	return render_template("home.html",access= token)



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
	return redirect(url_for("patients"))


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
			response = requests.post(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			if(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))
			elif(response.status_code==201):
				print(response)
				print(response.text)
				flash("Patient Registered Successfully.","success")
			# elif(response.status_code==400):

			# return redirect(url_for('patient_registration'))
		return render_template('patient_registration.html')

	return render_template('patient_registration.html')


# update patient
@app.route('/update_patient',methods=['GET','POST'])
def update_patient():
	form = UpdateForm()
	formx = getData(request.args)
	if not session.get('token'):
		return redirect(url_for('login'))

	else:
		if request.method =='GET':
			patientId = request.args.get('patientID')
			session['pid'] = patientId
			print(patientId)
			token = session.get('token')
			url ="https://abchospitalmanagement.herokuapp.com/patient"
			data= {"patientId":patientId}
			response = requests.get(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			print(response.json())
			r = response.json()
			if(response.status_code==200):
				formx.patientID.data = session.get('pid')
				form.patientSSNID.data = r['patientSSNId']
				form.patientName.data = r['patientName']
				form.patientAge.data = r['patientAge']
				form.doa.data = r['doa']
				form.tob.data = r['tob']
				form.address.data = r['address']
				form.state.data = r['state']
				form.city.data = r['city']
			elif(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))
		if request.method=='POST' and form.submit.data:
			print("hii")
			patientID = session.get('pid')
			patientSSNID = form.patientSSNID.data
			patientName = form.patientName.data
			patientAge = form.patientAge.data
			doa = form.doa.data
			tob = form.tob.data
			address = form.address.data
			state =	form.state.data
			city = form.city.data
			token = session.get('token')
			url = "https://abchospitalmanagement.herokuapp.com/patient"
			data= {"patientId":patientID, "patientSSNId": patientSSNID, "patientName": patientName, "patientAge":patientAge, "doa":doa, "tob":tob, "address":address, "state":state, "city":city}
			response = requests.put(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			formx.patientID.data = session.get('pid')
			if response.status_code == 200:
				print(response.json())
				flash("data updated suucessfully", "success")
				
			elif(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))




	# if request.method == 'GET':
	# 	request.args.get('patientSSNID')= "abcd"
	# 	return render_template('update_patient.html')

	return render_template('update_patient.html',form=form,formx=formx)



# view all patients

@app.route('/patients',methods=['GET','POST'])
def patients():
	if not session.get('token'):
		return redirect(url_for('login'))
	else:
		token = session.get('token')
		url = "https://abchospitalmanagement.herokuapp.com/patients"
		response = requests.get(url, headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
		print(response.json())
		data = response.json()
		if(response.status_code==500):
			session.pop('token',None)
			return redirect(url_for('login'))
		elif(response.status_code==200):
			return render_template('patients.html',data = data['patients'])




# delete a patient
@app.route('/delete_patient',methods=['GET','POST'])
def delete_patient():
	form = UpdateForm()
	formx = getData()
	if not session.get('token'):
		return redirect(url_for('login'))
	else:
		if formx.go.data and formx.validate():
			print("hji")
			patientId = formx.patientID.data
			session['pid'] = patientId
			print(patientId)
			token = session.get('token')
			url ="https://abchospitalmanagement.herokuapp.com/patient"
			data= {"patientId":patientId}
			response = requests.get(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			print(response.json())
			r = response.json()
			if(response.status_code==200):
				formx.patientID.data = r['patientId']
				form.patientID.data = r['patientId']
				form.patientSSNID.data = r['patientSSNId']
				form.patientName.data = r['patientName']
				form.patientAge.data = r['patientAge']
				form.doa.data = r['doa']
				form.tob.data = r['tob']
				form.address.data = r['address']
				form.state.data = r['state']
				form.city.data = r['city']
			elif(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))
		elif form.delete.data:
			print("hiii")
			patientID = form.patientID.data
			print(patientID)
			# patientSSNID = form.patientSSNID.data
			# patientName = form.patientName.data
			# patientAge = form.patientAge.data
			# doa = form.doa.data
			# tob = form.tob.data
			# address = form.address.data
			# state =	form.state.data
			# city = form.city.data
			token = session.get('token')
			url = "https://abchospitalmanagement.herokuapp.com/patient"
			data= {"patientId":patientID}
			# data= {"patientId":patientID, "patientSSNId": patientSSNID, "patientName": patientName, "patientAge":patientAge, "doa":doa, "tob":tob, "address":address, "state":state, "city":city}
			response = requests.delete(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			# formx.patientID.data = session.get('pid')
			print(response)
			if response.status_code == 200:
				print(response.json())
				flash("data deleted suucessfully", "success")
				return redirect(url_for('delete_patient'))
			elif(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))
	return render_template('delete_patient.html',form=form,formx=formx)


# search a patient
@app.route('/search_patient',methods=['GET','POST'])
def search_patient():
	form = UpdateForm()
	formx = getData()
	if not session.get('token'):
		return redirect(url_for('login'))
	else:
		if formx.go.data and formx.validate():
			print("hji")
			patientId = formx.patientID.data
			session['pid'] = patientId
			print(patientId)
			token = session.get('token')
			url ="https://abchospitalmanagement.herokuapp.com/patient"
			data= {"patientId":patientId}
			response = requests.get(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			print(response.json())
			r = response.json()
			if(response.status_code==200):
				formx.patientID.data = r['patientId']
				form.patientID.data = r['patientId']
				form.patientSSNID.data = r['patientSSNId']
				form.patientName.data = r['patientName']
				form.patientAge.data = r['patientAge']
				form.doa.data = r['doa']
				form.tob.data = r['tob']
				form.address.data = r['address']
				form.state.data = r['state']
				form.city.data = r['city']
			elif(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))
	return render_template('search_patient.html',form=form,formx=formx)




