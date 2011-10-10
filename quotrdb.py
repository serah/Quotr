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
    active = db.Column(db.Boolean)
    by = db.Column(db.Text)

    def __init__(self,body,tags,active,by):
        self.body = body
        self.tags = tags
        self.active = active
        self.by = by
        
        
class Operators (db.Model):
    
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.Text)
    email = db.Column(db.Text)
    

    def __init__(self,username,email):
        self.username = username
        self.email = email


#create the database by db.create_all()
#if database is present, it won't be overwritten
def init_db():
    db.create_all()
