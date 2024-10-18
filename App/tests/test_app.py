import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.models import Student
from App.models import Review
from App.controllers import (
    create_user,
    create_admin,
    create_staff,
    create_student,
    create_review,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    get_student_by_id,
    get_all_students_json,
    get_latest_review_json,
    get_reviews_by_student_id_json,
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)
    

class AdminUnitTests(unittest.TestCase):

    def test_addStudent(self):
        student = Student(101, "Mike Ross", "BSc. Computer Science", "DCIT", "FST")
        assert student.studentID == 101
        assert student.studentName == "Mike Ross"
        assert student.degree == "BSc. Computer Science"
        assert student.department == "DCIT"
        assert student.faculty == "FST"


class StaffUnitTests(unittest.TestCase):

    def test_addStudentReview(self):
        review = Review(101, 107, "Positive", "Has an amazing ability to remember details")
        assert review.studentID == 101
        assert review.staffID == 107
        assert review.type == "Positive"
        assert review.content == "Has an amazing ability to remember details"



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None


class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

class AdminIntegrationTests(unittest.TestCase):

    def test_create_admin(self):
        newadmin = create_admin("ben", "benpass")
        admin = get_user_by_username("ben")
        self.assertEqual(admin.username, "ben")
        self.assertEqual(admin.type, "admin")
    
    def test_create_student(self):
        newstudent = create_student(101, "Mike Ross", "BSc. Computer Science", "DCIT", "FST")
        student = get_student_by_id(101)
        self.assertEqual(student.studentID, 101)
        self.assertEqual(student.studentName, "Mike Ross")
        self.assertEqual(student.degree, "BSc. Computer Science")
        self.assertEqual(student.department, "DCIT")
        self.assertEqual(student.faculty, "FST")
    
    def test_get_all_students(self):
        student = create_student(102, "Rachel Zane", "BSc. Information Technology", "DCIT", "FST")
        students = get_all_students_json()
        expected_students = [
            {
                "studentID":101, 
                "studentName":"Mike Ross", 
                "degree":"BSc. Computer Science", 
                "department":"DCIT", 
                "faculty":"FST"
            },
            {
                "studentID":102, 
                "studentName":"Rachel Zane", 
                "degree":"BSc. Information Technology", 
                "department":"DCIT", 
                "faculty":"FST"
            }
        ]
        self.assertListEqual(expected_students, students)


class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        newstaff = create_staff("newstaff", "newstaffpass")
        staff = get_user_by_username("newstaff")
        self.assertEqual(staff.username, "newstaff")
        self.assertEqual(staff.type, "staff")

    def test_create_review(self):
        staff = create_staff("gwen", "gwenpass")
        staff = get_user_by_username("gwen")
        student = create_student(103, "Harvey Spectre", "BSc. Computer Science (Special)", "DCIT", "FST")
        review = create_review(103, staff.id, "Positive", "The best closer this city has ever seen")
        expected_review = {
            "reviewID": review.reviewID,
            "studentID": 103,
            "staffID": staff.id,
            "type": "Positive",
            "content": "The best closer this city has ever seen"
        }
        review = get_latest_review_json(103)
        self.assertEqual(expected_review, review)
    
    def test_get_latest_review(self):
        staff1 = create_staff("kevin", "kevinpass")
        staff1 = get_user_by_username("kevin")
        staff2 = create_staff("max", "maxpass")
        staff2 = get_user_by_username("max")
        student = create_student(104, "Jessica Pearson", "BSc. Information Technology (Special)", "DCIT", "FST")
        review1 = create_review(104, staff1.id, "Positive", "She is very hardworking.")
        review2 = create_review(104, staff2.id, "Negative", "She does not repond well to threats.")
        expected_review = {
            "reviewID": review2.reviewID,
            "studentID": 104,
            "staffID": staff2.id,
            "type": "Negative",
            "content": "She does not repond well to threats."
        }
        review = get_latest_review_json(104)
        self.assertEqual(expected_review, review)
    
    def test_get_reviews_by_student_id(self):
        staff = create_staff("cooper", "cooperpass")
        staff = get_user_by_username("cooper")
        student = student = create_student(105, "Louis Litt", "BSc. Computer Science and Management", "DCIT", "FST")
        review1 = create_review(105, staff.id, "Negative", "Mean")
        review2 = create_review(105, staff.id, "Negative", "Short-tempered")
        expected_reviews = [
            {
                "reviewID": review1.reviewID,
                "studentID": 105,
                "staffID": staff.id,
                "type": "Negative",
                "content": "Mean"
            },
            {
                "reviewID": review2.reviewID,
                "studentID": 105,
                "staffID": staff.id,
                "type": "Negative",
                "content": "Short-tempered"
            }
        ]
        reviews = get_reviews_by_student_id_json(105)
        self.assertEqual(expected_reviews, reviews)

