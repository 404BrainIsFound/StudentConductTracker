from App.models import Review
from App.database import db

def create_review(studentID, type, content):
    newreview = Review(studentID=studentID, type=type, content=content)
    db.session.add(newreview)
    db.session.commit()
    return newreview

def get_reviews_by_id(studentID):
    return Review.query.filter_by(studentID=studentID)