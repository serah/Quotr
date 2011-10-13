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
from forms import EntryForm, LoginForm, RegisterationForm
#-------------------------------------------------------------------------------

# create our  application :)
app = Flask(__name__)

# take the configuration from the config file
app.config.from_object(appconf)


#use py-bcrypt for hashing password
bcrypt_init(app)
mail = Mail(app)


#-----------------------All forms are defined here------------------------------

     
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
    
@app.route('/quote/<int:quote_id>')
def show_quote(quote_id):
    return render_template('quote.html')

    
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
