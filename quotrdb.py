from flask import Flask
from conf import appconf
from flaskext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = appconf.DB_URI

db = SQLAlchemy(app)

class Quotes (db.Model):
    
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    tags = db.Column(db.Text)
    by = db.Column(db.Text)
    active = db.Column(db.Boolean)

    def __init__(self,body,tags,by,active):
        self.body = body
        self.tags = tags
        self.by = by
        self.active = active
"""
class Queue (db.Model):
    
    __tablename__ = 'queue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    tags = db.Column(db.Text)
    active = db.Column(db.Boolean)
    by = db.Column(db.Text)

    def __init__(self,body,tags,by,active):
        self.body = body
        self.tags = tags
        self.by = by
        self.active = active
"""
        
class Operators (db.Model):
    
    __tablename__ = 'operators'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nick = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self,email,password,nick):
        self.nick = nick
        self.email = email
        self.password = password


#create the database by db.create_all()
#if database is present, it will be overwritten
def init_db():
    db.create_all()
