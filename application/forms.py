from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username   = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), Length(min=0)])
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
    patientID   = IntegerField("patientID", validators=[DataRequired()])
    go = SubmitField("Go")
    