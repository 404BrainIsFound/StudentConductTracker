from App.database import db
from App.models import User

class Staff(User):
    __mapper_args__ = {'polymorphic_identity' : 'staff'}
    def __init__(self, username, password):
        super().__init__(username, password)