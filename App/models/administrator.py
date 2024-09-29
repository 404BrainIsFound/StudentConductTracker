from App.database import db
from App.models import User

class Administrator(User):
    def __init__(self, username, password):
        super(self, username, password)