from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import get_user, get_student_reviews_json, create_review, get_student_by_id
from App.models import User
from App.models import Staff

review_views = Blueprint('review_views', __name__, template_folder='../templates')

@review_views.route('/reviews', methods=['GET'])
@jwt_required()
def get_reviews():
    userID = get_jwt_identity()
    user : User = get_user(userID)
    if user:
        if user.type == "staff":
            data = request.json
            studentID = data['studentID']
            if studentID is None:
                return jsonify({
                    "error":"missing student id"
                }), 404
            else:
                student = get_student_by_id(studentID)
                if not student:
                    return jsonify({"message": "student does not exist"})
                return get_student_reviews_json(studentID=studentID)
        else:
            return jsonify({
                "error":"insufficient permissions"
            }), 401
    return jsonify({
        "error":"must be logged in"
    }), 401

@review_views.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if isinstance(current_user, Staff):  #for ref here: https://www.w3schools.com/python/ref_func_isinstance.asp, if it doesn't work try something else ig
        data = request.get_json()

        if not all(key in data for key in ('studentID', 'type', 'content')):      #if giving problems comment off - not in spec I think
            return jsonify({"error": "Missing required fields"}), 400
            
        studentID = data['studentID']
        student = get_student_by_id(studentID)
        if not student:
            return jsonify({"message": "student does not exist"})

        try:
            new_review = create_review(data['studentID'], current_user_id, data['type'], data['content'])
            return jsonify({
                "message": "Review added",
                "review": new_review.get_json()         #from models
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access, teaching staff only"}), 403