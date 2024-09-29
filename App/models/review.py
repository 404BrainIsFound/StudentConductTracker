from App.database import db

class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(150), nullable=False)

    def __init__(self, studentID, type, content):
        self.studentID = studentID
        self.type = type
        self.content = content