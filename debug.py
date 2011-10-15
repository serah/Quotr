from quotrdb import db, Operators

q = Operators.query.filter_by(email = 'pronoyc@gmail.com').first()
print q
