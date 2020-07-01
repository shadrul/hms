import requests
patienId = 2
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTM2MjU5NzcsImlhdCI6MTU5MzYyNTY3NywibmJmIjoxNTkzNjI1Njc3LCJpZGVudGl0eSI6MX0.CEiOI6Z1YmWPLhCgX9lGyLZYgf6Z8fIPxtF4vDqDl9s"
url ="https://abchospitalmanagement.herokuapp.com/patient"
data= {"patientId":patienId}
response = requests.get(url, json=data,headers={"Content-Type": "application/json", "Authorization": "JWT " + token})
print(response.json())