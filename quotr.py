# -*- coding: utf-8 -*-
"""
    Quotr 
    ~~~~~~

    A Quote Managment System written using Flask and SQLAlchemy
    
    Extensions used:
        Flask-SQLAlchemy
        Flask-WTF
        Flask-Bcrypt
        Flask-Mail

    :Author : Pronoy Chopra
    :Project: Quotr
            
"""
#-------------------------------imports-----------------------------------------
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
from quotrdb import Operators, Quotes
#-------------------------------------------------------------------------------

# create our  application :)
app = Flask(__name__)

# take the configuration from the config file
app.config.from_object(appconf)


#use py-bcrypt for hashing password
bcrypt_init(app)
mail = Mail(app)


#-----------------------All forms are defined here------------------------------


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
     
#---------------------------database related actions----------------------------

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

#---------------------------decorators start here-------------------------------

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm(request.form)
    if form.validate_on_submit():
        session['logged_in'] = True
        session['username'] = form.username.data
        if session['logged_in']:
            flash('You were logged in as '+ session['username'])
        else:
            flash('oops you were not logged in')
        return redirect(url_for('server_status'))
    return render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('logged out')
    return redirect(url_for('index')) 
    
@app.route('/submit', methods=['GET','POST'])
def submit_quote():
    form = EntryForm(request.form)
        
    return render_template('submit.html',form=form)
    
@app.route('/q')
def queue():
    return render_template('queue.html')

@app.route('/tags')
def tags():
    return render_template('tags.html')

@app.route('/wiki')
def wiki():
    return render_template('wiki.html')
   
if __name__ == '__main__':
    app.run()
