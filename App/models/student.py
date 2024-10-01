from App.database import db

class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(30), nullable=False)
    degree = db.Column(db.String(30), nullable=False)
    department = db.Column(db.String(30), nullable=False)
    faculty = db.Column(db.String(30), nullable=False)
    reviews = db.relationship('Review', backref='student', lazy=True, cascade="all, delete-orphan")

    def __init__(self, studentID, studentName, degree, department, faculty):
        self.studentID = int(studentID)
        self.studentName = studentName
        self.degree =  degree
        self.department = department
        self.faculty = faculty

    def __repr__(self):
        return f'Student Name: {self.studentName}, Student ID: {self.studentID}, Degree: {self.degree}, Department: {self.department}, Faculty: {self.faculty}'