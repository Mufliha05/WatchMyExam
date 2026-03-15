from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# USER
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))

# EXAM
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    duration = db.Column(db.Integer)

# QUESTION
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer)
    question_text = db.Column(db.String(500))
    option1 = db.Column(db.String(200))
    option2 = db.Column(db.String(200))
    option3 = db.Column(db.String(200))
    option4 = db.Column(db.String(200))
    correct_answer = db.Column(db.String(200))

# ANSWER
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    exam_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    selected_answer = db.Column(db.String(200))

# ACTIVITY LOG
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    exam_id = db.Column(db.Integer)
    activity_type = db.Column(db.String(100))
    description = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# VIOLATION
class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    violation_type = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    image_path = db.Column(db.String(300))   # NEW FIELD

class ExamAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    exam_id = db.Column(db.Integer)
    status = db.Column(db.String(50), default="assigned")
    