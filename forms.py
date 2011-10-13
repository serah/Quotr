from flask import Flask
from flaskext.wtf import Form, TextField, TextAreaField, PasswordField, \
    SubmitField, Required, ValidationError, validators

class EntryForm(Form):
    
    body = TextAreaField("Body")
    tags = TextAreaField("Tags")
    by   = TextField("Posted by:", [validators.Required()])
    submit = SubmitField("Submit")
    

class LoginForm (Form):
    
    email = TextField("Email")
    password = PasswordField("Password")
    login = SubmitField("Login")
    
    forgotpass = TextField("Forgot Password?")
    forgot_submit = SubmitField("Submit")
    
    def validate_email(self,email):
        access_user = Operators.query.filter_by(email = email.data).first()
        if access_user is None:
            raise ValidationError, "Invalid Username"

    def validate_password(self,password):
        access_user = Operators.query.filter_by(email = self.email.data).first()
        if access_user is None:
            raise ValidationError, "Invalid Username"
        else:
            condition = check_password_hash(access_user.password, password.data)
        if not condition:
            raise ValidationError, "Invalid Password"
    
class RegisterationForm (Form):

    email = TextField("Email Address", [validators.Length(min=6)])
    password = PasswordField("New Password", 
                            [
                            validators.Required(),
                            validators.EqualTo('confirm', 
                            message='Passwords must match')
                            ])
    
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Register")   
    
    #querying for known entries for the given email    
    def validate_username(self,email):
        unidentified = User.query.filter_by(email=email.data).first()
        if unidentified is not None:
            raise ValidationError, "Username already exists"
