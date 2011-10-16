#-------------------------------imports-----------------------------------------

from flask import Flask

from flaskext.wtf import Form, TextField, TextAreaField, PasswordField, \
    SubmitField, Required, ValidationError, validators

from flaskext.bcrypt import bcrypt_init, generate_password_hash, \
    check_password_hash

from quotrdb import Operators, Quotes

#-------------------------------------------------------------------------------


class EntryForm(Form):
    
    body = TextAreaField("Body")
    tags = TextAreaField("Tags")
    by   = TextField("Posted by:")
    submit = SubmitField("Submit")
    

class LoginForm (Form):
    
    email = TextField("Email")
    password = PasswordField("Password")
    login = SubmitField("login")

    """
    def validate_password(self,password):
        access_user = Operators.query.filter_by(email = self.email.data).first()
        if access_user is None:
            raise ValidationError, "Invalid Username"
        else:
            condition = check_password_hash(access_user.password, password.data)
        if not condition:
            raise ValidationError, "Invalid Password"
    """
      
            
class RegisterationForm(Form):
    
    email = TextField("Email")
    password = PasswordField("Password",[
                            validators.Required(), 
                            validators.EqualTo('confirm', 
                            message="Passwords must match")]
                            )
                            
    confirm = PasswordField("Confirm Password")
    nick = TextField("Nickname")
    submit = SubmitField("Register")
    
    """
    def validate_email(self,email):
        unidentified = Operators.query.filter_by(email=email.data).first()
        if not unidentified is None:
            raise ValidationError, "Username already exists"
    
    """         
