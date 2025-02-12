from App.database import db

class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(150), nullable=False)

    def __init__(self, studentID, staffID, type, content):
        self.studentID = studentID
        self.staffID = staffID
        self.type = type
        self.content = content


        

    def __repr__(self):
        return f'Review Type: {self.type}\nReview: {self.content}'
    
    def get_json(self):
        return {
            'reviewID' : self.reviewID,
            'studentID' : self.studentID,
            'staffID' : self.staffID,
            'type' : self.type,
            'content' : self.content
        }