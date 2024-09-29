from App.models import Administrator
from App.database import db

def create_admin(username, password):
    newadmin = Administrator(username=username, password=password)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin