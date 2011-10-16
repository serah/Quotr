from quotrdb import Operators, db, init_db
import os
from conf import appconf
import sys
from flaskext.bcrypt import generate_password_hash, check_password_hash

print "\nHello and welcome to Quotr. This will help setup Quotr very quickly and easily."
print "-------------------------------------------------------------------------------"
print "Step 1. Setting up the database\n"
print "Please note that the database will be setup with the default name as given in the configuration file. ./conf/appconf.py"
print "You can check it and or edit it as per the rules given in the comments. Please be careful."
print "If you don't want to go about messing with the configuration file you can proceed by entering yes."
print "If not you can abort by typing anything other than yes."


choice = raw_input("Go ahead?: " )
if choice == 'yes':
    if os.path.isfile(appconf.DATABASE):
        print "Removed the old database first ................................."
        os.remove(appconf.DATABASE)
    init_db()
    #quick check if database was created
    if not os.path.isfile(appconf.DATABASE):
        print "Looks like there was some problem in creating the Database. You may want to try again"
        sys.exit()
    print "Congratulations Database was setup\n"
    print "Step 2. Setup the admin, checking the one time config file"
    print "...................................................................."
    if not os.path.isfile("conf/onetimeconf.py"):
        print "Couldn't find onetimeconf.py in the conf folder. Please create that file as per the README"
    else:
        print "Found the file, now attempting to add the admin"
        from conf.onetimeconf import admin_nick, admin_email, admin_password
        usable_password = generate_password_hash(admin_password)
        admin = Operators(nick=admin_nick,email=admin_email,password=usable_password)
        db.session.add(admin)
        db.session.commit()
        
        print "Attempting to check if admin was added..."
        check = Operators.query.filter_by(email=admin_email).first()
        if check:
            print "Congratulations the admin was setup with the email: "+ admin_email
            print "Now attempting to REMOVE the onetimeconf.py file. It is dangerous to keep it around"
            os.remove('conf/onetimeconf.py')
            if not os.path.isfile('conf/onetimeconf.py'):
                print "Successful! Perfect. Now you're good to go. Start quotr by doing python quotr.py"
            else:
                print "uh oh. Looks like the file wasn't removed. Kindly remove it manually. It is unsafe to keep that file"
                
        else:
            print "Something went wrong, the admin wasn't setup"
    
    
else:
    print "Abort"
    

