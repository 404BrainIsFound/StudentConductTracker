import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers.student import *
from App.controllers.review import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

admin = AppGroup("admin", help="Group for managing student records")

@admin.command("create-student", help="Add a new student record. Usage: \"create-student {id} {name}\"")
@click.argument("id")
@click.argument("name")
def create_student_command(id, name):
    if (get_student_by_id(id) is not None):
        print(f'Student with id {id} already exists! Cannot create new student with the same id.')
        return
    create_student(id, name)
    print(f'Student {name} created!')

app.cli.add_command(admin)

'''
Teaching Staff Commands
'''

staff = AppGroup("staff", help="Group for searching and reviewing students")


@staff.command("search-student-id", help="Searches for a student with a specified student ID. Usage \"search-student-id {id}\"", short_help="Usage \"search-student-id {id}\"")
@click.argument("id")
def search_student_id_command(id):
    if (get_student_by_id(id) is None):
        print("Student does not exist.")
        return
    print(f'{get_student_by_id(id)}\nLatest Review: {get_latest_review(id)}')

@staff.command("search-student-name", help="Searches for students that match a specified name. Usage \"search-student-name {name}\"", short_help="Usage \"search-student-name {name}\"")
@click.argument("name")
def search_student_name_command(name):
    students = get_student_by_name(name)
    if (len(students) == 0):
        print("No students match that name.")
        return
    for student in students:
        student: Student
        print(f'\n{student}\nLatest Review: {get_latest_review(student.studentID)}')

@staff.command("add-review", help="Adds a review for a particular student. Usage \"add-review {id}\"", short_help="Usage \"add-review {id}\"")
@click.argument("id")
def add_review_command(id):
    if (get_student_by_id(id) is None):
        print("Invalid student ID!")
    else:
        type = input("Enter review type (positive/negative): ")
        content = input("Enter student review (Max 150 characters). Pressing ENTER will submit your review.\n")
        create_review(id, type, content)
        print(f'Successfully added {type} review for student {id}!')

@staff.command("view-reviews", help="View all reviews from a particular student. Usage \"view-reviews {id}\"", short_help="Usage \"view-reviews {id}\"")
@click.argument("id")
def get_student_reviews_command(id):
    if (get_student_by_id(id) is None):
        print("Invalid student ID!")
    else:
        print(f'Showing reviews for student {id}\n{get_student_by_id(id)}')
        for review in get_student_reviews(id):
            review: Review
            print(f'{review}\n')

app.cli.add_command(staff)