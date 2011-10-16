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
from quotrdb import Operators, Quotes, db
from forms import RegisterationForm, LoginForm, EntryForm
from backend import preserve_whitespace, separate_tags, check_if_database_up, \
    check_size
#-------------------------------------------------------------------------------

# create our  application :)
app = Flask(__name__)

# take the configuration from the config file
app.config.from_object(appconf)


#use py-bcrypt for hashing password
bcrypt_init(app)
mail = Mail(app)


#-----------------------All forms are defined here------------------------------
#forms.py
#---------------------------database related actions----------------------------

def connect_db():
    #Returns a new connection to the database.
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    #Make sure we are connected to the database each request.
    g.db = connect_db()

@app.after_request
def after_request(response):
    #Closes the database again at the end of the request.
    g.db.close()
    return response

#---------------------------decorators start here-------------------------------

@app.route('/')
def index():
    if check_if_database_up():
        if check_size() == 0:
            return render_template('oops.html')
        else:
            quotes = Quotes.query.order_by(Quotes.id.desc()).all()
            if not quotes:
                error = 'Nothing to see here. Move along'
            else:
                error = ''
            return render_template('index.html',quotes=quotes,error=error)

#debug
"""
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterationForm(request.form)
    if request.method == 'POST' and form.validate():
        
        password_hash = generate_password_hash(form.password.data)
        
        new_user = Operators(form.email.data, password_hash,form.nick.data)
        db.session.add(new_user)
        db.session.commit()
        
        #check if user was registered 
    return render_template('register.html', form=form)
"""
#debug ends
    
@app.route('/submit', methods=['GET','POST'])
def submit_quote():
    if check_if_database_up():
        if check_size() == 0:
            return render_template('oops.html')
        else:
            form = EntryForm(request.form)
            if request.method=='POST':
                new_body = preserve_whitespace(form.body.data)
                new_quote = Quotes(new_body,form.tags.data,form.by.data,False)
                db.session.add(new_quote)
                db.session.commit()
                return redirect(url_for('index'))
            return render_template('submit.html',form=form)
    
    
@app.route('/quote/<quote_id>')
def show_quote(quote_id):
    if check_if_database_up():
        if check_size() == 0:
            return render_template('oops.html')
        else:
            specific = Quotes.query.get_or_404(quote_id)
            return render_template('quote.html',specific=specific)
    
@app.route('/q')
def queue():
    if check_if_database_up():
        if check_size() == 0:
            return render_template('oops.html')
        else:
            quotes = Quotes.query.order_by(Quotes.id.desc()).all()
            if not quotes:
                error = 'Nothing to see here. Move along'
            else:
                error = ''
            return render_template('queue.html',quotes=quotes,error=error)
            
            
            
@app.route('/tags')
def tags():
    if check_if_database_up():
        if check_size() == 0:
            return render_template('oops.html')
        else:
            return render_template('tags.html')

@app.route('/wiki')
def wiki():
    return render_template('wiki.html')

@app.route('/wiki/tutorials')
def tutorials():
    return render_template('tutorials.html')
    
@app.route('/wiki/scripts')
def scripts():
    return render_template('scripts.html')    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if check_if_database_up():
        if check_size() == 0:
            return render_template('oops.html')
        else:
            form = LoginForm(request.form)
            if form.validate_on_submit():
                session['logged_in'] = True
                return redirect(url_for('index'))
            return render_template('login.html', form=form)
        
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('logged out')
    return redirect(url_for('index')) 
   
if __name__ == '__main__':
    app.run()
