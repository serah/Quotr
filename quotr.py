# -*- coding: utf-8 -*-
"""
    Wombat 
    ~~~~~~

    An Asset Managment System written using Flask with SQLAlchemy
    
    Extensions used:
        Flask-SQLAlchemy
        Flask-WTF
        Flask-Uploads
        Flask-Mail    

    :Author : Pronoy Chopra
    :Project: Worldforge
    :program: GSoC 2011
    :Mentor : Kai Blin
            
"""
#-----------------------------imports-------------------------------------------
#bunch of imports
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
#from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from conf import appconf
from flaskext.bcrypt import bcrypt_init, generate_password_hash, \
    check_password_hash
from flaskext.wtf import Form, TextField, TextAreaField, PasswordField, \
    SubmitField, Required, ValidationError, validators
from flaskext.mail import Mail
import os
#-------------------------------------------------------------------------------

# create our  application :)
app = Flask(__name__)

# take the configuration from the config file
app.config.from_object(appconf)


#use py-bcrypt for hashing password
bcrypt_init(app)
mail = Mail(app)

#all functions need to have to be imported from Base class or SVNfunctions() class
func = Base()

#-----------------------All forms are defined here------------------------------

class LoginForm (Form):
    
    username = TextField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Login")
    
    
    def validate_username(self,username):
        access_user = User.query.filter_by(email = username.data).first()
        if access_user is None:
            raise ValidationError, "Invalid Username"


    def validate_password(self,password):
        access_user = User.query.filter_by(email = self.username.data).first()
        if access_user is None:
            raise ValidationError, "Invalid Username"
        else:
            condition = check_password_hash(access_user.password, password.data)
        if not condition:
            raise ValidationError, "Invalid Password"
    
    def validate_user(self,username):
        access_user = User.query.filter_by(email = username.data).first()
        if not access_user.active:
            raise ValidationError, "User not Active"


#this is the registeration form
class RegisterationForm (Form):

    #email field: Mandatory
    email = TextField("Email Address", [validators.Length(min=6)])
    
    #password field: Mandatory
    password = PasswordField("New Password", [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    
    #confirm password field: Mandatory
    confirm = PasswordField('Repeat Password')
        
    #name of the user: Non Mandatory
    Name = TextField("Your full name")
    
    #nick name of the user: Non Mandatory
    Nickname = TextField("Your nick name")
    
    #vcs_username of the user: Non Mandatory
    VCS_Username = TextField("Your VCS Username")
    
    #vcs_password of the user: Non mandatory
    VCS_Password = PasswordField("Your VCS Password")

    submit = SubmitField("Register")   
    
    #querying for known entries for the given email    
    def validate_username(self,email):
        unidentified = User.query.filter_by(email=email.data).first()
        if unidentified is not None:
            raise ValidationError, "Username already exists"
     
     
     
    class UpdateForm (Form):
        
        #username = TextField("Your new email")
        password = PasswordField("New Password", [
                                validators.Required(),
                                validators.EqualTo('confirm', 
                                message='Passwords must match')
                                ])
        confirm = PasswordField("Your new password again")
        Name = TextField("Your name")
        Nickname = TextField("Your nickname")    
        VCS_Username = TextField("Your VCS Username")
        VCS_Password = PasswordField("Your VCS Password")
        Update = SubmitField("Update Information")
     
     
     class ForgotPassword (Form):
         username = TextField("Your Email/Username ")
         submit = SubmitField("Check for Username")
         
         def validate_email(self,username):
             forgetful_user = User.query.filter_by(email=username.data).first()
             if forgetful_user is None:
                 raise ValidationError, "Username doesn't exist"
         
            
#-----------------------------database related actions--------------------------


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    g.db.close()
    return response

#----------------------------decorators start here------------------------------

if __name__ == '__main__':
    app.run()
