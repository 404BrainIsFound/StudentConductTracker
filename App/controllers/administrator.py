from App.models import Administrator
from App.database import db

def create_admin(username, password):
    newadmin = Administrator(username=username, password=password)
    newadmin.type = "admin"
    db.session.add(newadmin)
    db.session.commit()