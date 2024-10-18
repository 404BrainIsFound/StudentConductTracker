from App.models import Review
from App.database import db

def create_review(studentID, staffID, type, content):
    newreview = Review(studentID=studentID, staffID=staffID, type=type, content=content)
    db.session.add(newreview)
    db.session.commit()
    return newreview

def get_reviews_by_student_id(studentID):
    return Review.query.filter_by(studentID=studentID).all()

def get_reviews_by_staff_id(staffID):
    return Review.query.filter_by(staffID=staffID).all()

def get_latest_review(studentID):
    return Review.query.filter_by(studentID=studentID).order_by(Review.reviewID.desc()).first()

def get_latest_review_json(studentID):
    review = Review.query.filter_by(studentID=studentID).order_by(Review.reviewID.desc()).first()
    return review.get_json()