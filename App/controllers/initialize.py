from .staff import create_staff
from .student import create_student
from .review import create_review
from .user import get_user_by_username
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()

def demo():
    db.drop_all()
    db.create_all()

    create_staff("jean", "jeanpass")
    create_staff("scott", "scottpass")
    create_staff("xavier", "xavierpass")

    staff1 = get_user_by_username("jean")
    staff2 = get_user_by_username("scott")
    staff3 = get_user_by_username("xavier")

    create_student(1, "John", "Information Technology Major", "DCIT", "FST")
    create_student(2, "Jane", "Computer Science (Special)", "DCIT", "FST")
    create_student(3, "John", "Actuarial Science (Special)", "DMS", "FST")
    create_student(4, "Simon", "Mathematics (Special)", "DMS", "FST")
    create_student(5, "Jennifer", "Agriculture", "DFP", "FFA")

    create_review(1, staff1.id, "Positive", "Very diligent")
    create_review(1, staff2.id, "Positive", "Yes I agree")
    create_review(1, staff1.id, "Negative", "What are they talking about?")

    create_review(2, staff3.id, "Posiitve", "Hello I am positive review")

    create_review(3, staff2.id, "Negative", "Hello I am single negative review")
    
    create_review(5, staff3.id, "Positive", "Haha there is no review for that guy")
    create_review(5, staff3.id, "Positive", "Yeah that guy is really unlucky")
    create_review(5, staff1.id, "Posiitve", "This is the last review")
    create_review(5, staff2.id, "Negative", "...or is it?")
