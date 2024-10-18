from App.models import Student
from App.models import Review
from App.database import db

def create_student(studentID, studentName, degree, department, faculty):
    newstudent = Student(studentID=studentID, studentName=studentName, degree=degree, department=department, faculty=faculty)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def get_student_by_name(studentName):
    return Student.query.filter(Student.studentName.like(f'{studentName}%')).all()

def get_student_by_name_json(studentName):
    students = get_student_by_name(studentName=studentName)
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students

def get_student_by_id(studentID):
    return Student.query.get(studentID)

def get_student_reviews(studentID):
    return Review.query.filter_by(studentID=studentID).all()

def get_student_reviews_json(studentID):
    reviews = get_student_reviews(studentID=studentID)
    if not reviews:
        return []
    reviews = [review.get_json() for review in reviews]
    return reviews

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students