from App.database import db

class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(30), nullable=False)
    reviews = db.relationship('Review', backref='student', lazy=True, cascade="all, delete-orphan")

    def __init__(self, studentID, studentName):
        self.studentID = int(studentID)
        self.studentName = studentName

    def __repr__(self):
        return f'Student Name: {self.studentName} Student ID: {self.studentID}'