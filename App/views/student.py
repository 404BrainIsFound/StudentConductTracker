from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import create_student, get_user, get_student_by_name_json, get_student_by_id
from App.models import Student
from App.models import User

student_views = Blueprint('student_views', __name__)

@student_views.route('/students', methods=['POST'])          #didn't do all the tests, for you all to add - just a start
@jwt_required()
def add_student():

    data = request.get_json()
    userID = get_jwt_identity()
    user: User = get_user(userID)
    if user and user.type == "admin":
        if not all(key in data for key in ('studentID', 'studentName', 'degree', 'department', 'faculty')):
            return jsonify({"error": "Missing required fields"}), 400        #check to make sure all passed

        studentID = data['studentID']
        studentName = data['studentName']
        degree = data['degree']                        #get the fields needed
        department = data['department']
        faculty = data['faculty']

        student = get_student_by_id(studentID)
        if student:
            return jsonify({"message": "student already exists"})
    
        try:
            new_student = create_student(studentID, studentName, degree, department, faculty)  #from controllers
            return jsonify({
                "message": f"added student {new_student.studentName}"
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500     #processing error - return e so we would get more insight
    else:
        return jsonify({
            "error":"must be logged in"
        })
    

@student_views.route('/students', methods=['GET']) 
@jwt_required()
def search_student():
    userID = get_jwt_identity()
    user : User = get_user(userID)
    if user and user.type == "staff":
        data = request.json
        studentName = data['studentName']
        if studentName is None:
            return jsonify({
                "error":"must provide student name"
            })
        students: Student = get_student_by_name_json(studentName=studentName)
        if students is None:
            return jsonify({
                "error":"student not found"
            }), 404
        return students