from App.models import Staff
from App.database import db

def create_staff(username, password):
    newadmin = Staff(username=username, password=password)
    newadmin.type = "staff"
    db.session.add(newadmin)
    db.session.commit()