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

admin = AppGroup("admin")

@admin.command("create-student")
@click.argument("id")
@click.argument("name")
def create_student_command(id, name):
    create_student(id, name)
    print(f'Student {name} created!')

app.cli.add_command(admin)

'''
Teaching Staff Commands
'''

staff = AppGroup("staff")


@staff.command("search-student")
@click.argument("type")
def search_students_command(type):
    if (type == "id"):
        id = input("Enter student id: ")
        print(get_student_by_id(id))
    elif (type == "name"):
        name = input("Enter student name")
        print(get_student_by_name(name))
    else:
        print("Invalid search type! Try search-student id or search-student name")

@staff.command("add-review")
@click.argument("id")
def add_review_command(id):
    if (get_student_by_id(id) is None):
        print("Invalid student ID!")
    else:
        type = input("Enter review type (positive/negative): ")
        content = input("Enter student review (Max 150 characters). Pressing ENTER will submit your review.\n")
        create_review(id, type, content)

@staff.command("view-reviews")
@click.argument("id")
def get_student_reviews_command(id):
    print(get_student_reviews(id))

app.cli.add_command(staff)