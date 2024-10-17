from App.database import db
from App.models import User

class Administrator(User):
    __mapper_args__ = {'polymorphic_identity' : 'admin'}
    def __init__(self, username, password):
        super().__init__(username, password)