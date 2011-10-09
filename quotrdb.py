from flask import Flask
from conf import appconf
from flaskext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = appconf.DB_URI

db = SQLAlchemy(app)



    
    
#create the database by db.create_all()
#if database is present, it won't be overwritten
def init_db():
    db.create_all()
