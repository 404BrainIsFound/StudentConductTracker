import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    create_admin,
    create_staff,
    create_student,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    get_student_by_id,
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
        newadmin = create_admin("newadmin", "newadminpass")
        admin = get_user_by_username("newadmin")
        self.assertEqual(admin.username, "newadmin")
        self.assertEqual(admin.type, "admin")
    
    def test_create_student(self):
        newstudent = create_student(123456789, "John Doe", "BSc. Computer Science", "DCIT", "FST")
        student = get_student_by_id(123456789)
        self.assertEqual(student.studentID, 123456789)
        self.assertEqual(student.studentName, "John Doe")
        self.assertEqual(student.degree, "BSc. Computer Science")
        self.assertEqual(student.department, "DCIT")
        self.assertEqual(student.faculty, "FST")


class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        newstaff = create_staff("newstaff", "newstaffpass")
        staff = get_user_by_username("newstaff")
        self.assertEqual(staff.username, "newstaff")
        self.assertEqual(staff.type, "staff")

