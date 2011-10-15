#some functions
import glob
import os


#returns true if field is empty
def check_if_field_empty(field):
    if field == '':
        return True
    else:
        return False
        
#returns true if user is present        
def check_if_user_present(user):
    if not Operators.query.filter_by(email=user).first() is None:
        return True
    else:
        return False

#keeps the whitespaces in field
def preserve_whitespace(field):
    new_field_data = '<pre>'+field+'</pre>'
    return new_field_data
    
def separate_tags(field):
    pass
    
def check_if_database_up():
    q = glob.glob("*.db")
    if not q.__sizeof__() == 20:
        return True
    else:
        return False,
    
