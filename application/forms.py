from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField, TextField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_bootstrap import Bootstrap

class LoginForm(FlaskForm):
    username   = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=0)])
    submit = SubmitField("Login")

class UpdateForm(FlaskForm):
    # patientID   = IntegerField("patientID", validators=[DataRequired()])
    # go = SubmitField("Go")
    patientID = StringField("patientID", validators=[DataRequired()])
    patientSSNID = StringField("patientSSNID", validators=[DataRequired()])
    patientName = StringField("patientName")
    patientAge = StringField("patientAge")
    doa = StringField("doa")
    tob = StringField("tob")
    address = StringField("address")
    state = StringField("state")
    city = StringField("city")
    submit = SubmitField("submit")
    delete = SubmitField("delete")

class getData(FlaskForm):
	fld1 = HiddenField("Field 1")
	patientID   = IntegerField("patientID", validators=[DataRequired()])
	go = SubmitField("Go")
	issue = SubmitField("Issue Medicines")


class SearchForm(FlaskForm):
	autocomp = StringField('Insert Medicine', id='medicine_autocomplete')
	quantity = IntegerField('Quantity')
	add = SubmitField("ADD")

class IssueForm(FlaskForm):
	update = SubmitField("Update Medicines")