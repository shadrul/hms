import requests
from application import app
from flask import render_template, request, redirect, session, url_for, flash
from application.forms import LoginForm,UpdateForm, getData, SearchForm, IssueForm
import json


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


added = []

# pharmacy
@app.route('/pharmacy',methods=['GET','POST'])
def pharmacy():
	added =[]
	formx = getData()
	if not session.get('token'):
		return redirect(url_for('login'))
	else:
		if formx.go.data and formx.validate():
			print("hji")
			patientId = formx.patientID.data
			# session['pid'] = patientId
			print(patientId)
			token = session.get('token')
			url ="https://abchospitalmanagement.herokuapp.com/patient"
			data= {"patientId":patientId}
			response = requests.get(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			print(response.json())
			if(response.status_code==200):
				data = response.json()
				url1 ="https://abchospitalmanagement.herokuapp.com/medicineissued"
				d= {"patientId":patientId}
				response1 = requests.get(url1, json=d,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
				if(response1.status_code==200):
					med = response1.json()
					print(med)
					return render_template('pharmacy.html', formx=formx, data = data, med = med['medicines'])
			elif(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))
	return render_template('pharmacy.html',formx=formx)


# issue medicines

@app.route('/pharmacy/issue_medicine',methods=['GET','POST'])
def issue_medicine():
	formx = getData(request.values)
	form = SearchForm()
	formi = IssueForm()
	if not session.get('token'):
		return redirect(url_for('login'))
	else:
		token = session.get('token')
		url ="https://abchospitalmanagement.herokuapp.com/medicines"
		response = requests.get(url,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
		medicines = response.json()
		meds = medicines['medicines']
		
		if request.method=='POST' and formx.issue.data:
			print("hiiiiiii	")
			print(medicines)
			patientId = formx.fld1.data
			session['patientId']=patientId
			print(patientId)
		elif request.method=='POST' and form.add.data:
			print(meds)
			print(session.get('patientId'))
			name = form.autocomp.data
			quantity = form.quantity.data
			for med in meds:
				if(med['medicineName']==name):
					if(med['quantity']>=quantity):
						print("aaaa")
						# print(json.dump(med))
						amount = quantity * med['rate']
						added.append({"medicineName": name, "quantity": quantity, "rate": med['rate'], "amount":amount, "medicineId":  med['medicineId']}
							)
						return render_template('issue_medicine.html', form = form, formi = formi, medicines = meds, added= added)
		elif request.method=='POST' and formi.update.data:
			print('updatin')
			# added available here
			patientId = session.get('patientId')
			token = session.get('token')
			url ="https://abchospitalmanagement.herokuapp.com/medicineissued"
			x= []
			for i in added:
				x.append({"patientId":patientId, "medicineId":i['medicineId'], "quantity":i['quantity']})
			data= {"medicines" :x }
			response = requests.post(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
			print(response.json())
			print(response)
			if(response.status_code==200):
				session.pop('patientId',None)
				added.clear()
				return redirect(url_for('pharmacy'))
				
			elif(response.status_code==500):
				session.pop('token',None)
				return redirect(url_for('login'))

	return render_template('issue_medicine.html', form = form, formi = formi, medicines = meds)




