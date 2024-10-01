from .student import create_student
from .review import create_review
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()

def demo():
    db.drop_all()
    db.create_all()
    create_student(1, "John", "Information Technology Major", "DCIT", "FST")
    create_student(2, "Jane", "Computer Science (Special)", "DCIT", "FST")
    create_student(3, "John", "Actuarial Science (Special)", "DMS", "FST")
    create_student(4, "Simon", "Mathematics (Special)", "DMS", "FST")
    create_student(5, "Jennifer", "Agriculture", "DFP", "FFA")

    create_review(1, "Positive", "Very diligent")
    create_review(1, "Positive", "Yes I agree")
    create_review(1, "Negative", "What are they talking about?")

    create_review(2, "Posiitve", "Hello I am positive review")

    create_review(3, "Negative", "Hello I am single negative review")
    
    create_review(5, "Positive", "Haha there is no review for that guy")
    create_review(5, "Positive", "Yeah that guy is really unlucky")
    create_review(5, "Posiitve", "This is the last review")
    create_review(5, "Negative", "...or is it?")
    