from flask import Blueprint, request, jsonify
from App.controllers import create_student

student_views = Blueprint('student_views', __name__)

@student_views.route('/students', methods=['POST'])          #didn't do all the tests, for you all to add - just a start
def add_student():

    data = request.get_json()

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