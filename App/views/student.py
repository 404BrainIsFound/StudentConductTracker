from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import create_student, get_user_by_username
from App.models import User


student_views = Blueprint('student_views', __name__)

@student_views.route('/students/<int:studentID>', methods=['PUT'])          #didn't do all the tests, for you all to add - just a start
@jwt_required()
def add_student():

    data = request.get_json()
    username = get_jwt_identity()
    user: User = get_user_by_username(username=username)
    if user and user.type == "admin":
        if not all(key in data for key in ('studentID', 'studentName', 'degree', 'department', 'faculty')):
            return jsonify({"error": "Missing required fields"}), 400        #check to make sure all passed

        studentID = data['studentID']
        studentName = data['studentName']
        degree = data['degree']                        #get the fields needed
        department = data['department']
        faculty = data['faculty']

    
        try:
            new_student = create_student(studentID, studentName, degree, department, faculty)  #from controllers
            return jsonify({
                "message": f"added student {new_student.studentName}"
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500     #processing error - return e so we would get more insight