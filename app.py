from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, session, jsonify
from ai.monitor import start_monitoring
from models import db, User, Exam, Question, Answer, ActivityLog, Violation

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def admin_required():
    if 'user_id' not in session or session.get('role') != 'admin':
        return False
    return True


# ---------------------------
# ROUTES
# ---------------------------

@app.route("/")
def home():
    return "Backend Running Successfully"


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Check if email already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        role=data["role"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})




@app.route('/login', methods=['POST'])
def login():

    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        session['role'] = user.role
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 401
    

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

# ---------------------------
# EXAM MANAGEMENT ROUTES
# ---------------------------


    # CREATE QUESTION
@app.route("/create_question", methods=["POST"])
def create_question():

    data = request.get_json()
    

    question = Question(
        exam_id=data["exam_id"],
        question_text=data["question_text"],
        option1=data["option1"],
        option2=data["option2"],
        option3=data["option3"],
        option4=data["option4"],
        correct_answer=data["correct_answer"]
    )

    db.session.add(question)
    db.session.commit()

    return jsonify({"message": "Question added successfully"})

@app.route("/questions/<int:exam_id>", methods=["GET"])
def get_questions(exam_id):

    questions = Question.query.filter_by(exam_id=exam_id).all()

    question_list = []

    for q in questions:
        question_list.append({
            "id": q.id,
            "question": q.question_text,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4
        })

    return jsonify(question_list)

@app.route('/delete_question/<int:id>', methods=['DELETE'])
def delete_question(id):

    question = Question.query.get(id)

    if not question:
        return jsonify({"message": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Question deleted successfully"})

    # SUBMIT ANSWER
@app.route("/submit_answer", methods=["POST"])
def submit_answer():

    data = request.get_json()

    answer = Answer(
        student_id=data["student_id"],
        exam_id=data["exam_id"],
        question_id=data["question_id"],
        selected_answer=data["selected_answer"]
    )

    db.session.add(answer)
    db.session.commit()

    return jsonify({"message": "Answer submitted successfully"})

    # CALCULATE SCORE
@app.route("/calculate_score/<int:student_id>/<int:exam_id>", methods=["GET"])
def calculate_score(student_id, exam_id):

    answers = Answer.query.filter_by(student_id=student_id, exam_id=exam_id).all()

    score = 0
    total = len(answers)

    for ans in answers:

        question = db.session.get(Question, ans.question_id)

        if question.correct_answer == ans.selected_answer:
            score += 1

    return jsonify({
        "student_id": student_id,
        "exam_id": exam_id,
        "score": score,
        "total": total
    })

    # LOG ACTIVITY
@app.route("/log_activity", methods=["POST"])
def log_activity():

    data = request.get_json()

    log = ActivityLog(
        student_id=data["student_id"],
        exam_id=data["exam_id"],
        activity_type=data["activity_type"],
        description=data["description"]
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Activity logged successfully"})

# GET ACTIVITY LOGS
@app.route("/activity_logs/<int:student_id>/<int:exam_id>", methods=["GET"])
def get_activity_logs(student_id, exam_id):

    logs = ActivityLog.query.filter_by(
        student_id=student_id,
        exam_id=exam_id
    ).all()

    log_list = []

    for log in logs:
        log_list.append({
            "activity_type": log.activity_type,
            "description": log.description,
            "timestamp": str(log.timestamp)
        })

    return jsonify(log_list)

    # START EXAM MONITORING
@app.route("/start_monitoring/<int:user_id>", methods=["GET"])
def start_exam_monitoring(user_id):

    start_monitoring(user_id)
    return jsonify({
        "message": "Monitoring started"
    })

@app.route("/get_score/<int:user_id>", methods=["GET"])
def get_score(user_id):

    violations = Violation.query.filter_by(user_id=user_id).count()

    score = 100 - (violations * 5)

    if score < 0:
        score = 0

    status = "Normal"

    if score < 50:
        status = "Suspicious"

    if score < 30:
        status = "Critical"

    return jsonify({
        "user_id": user_id,
        "total_violations": violations,
        "integrity_score": score,
        "status": status
    })


@app.route('/users', methods=['GET'])
def get_all_users():
    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    users = User.query.all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        })

    return jsonify(result)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)

    db.session.commit()

    return jsonify({"message": "User updated successfully"})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"})

@app.route('/exams', methods=['POST'])
def create_exam_route():
    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    data = request.json

    new_exam = Exam(
        title=data['title'],
        duration=data['duration']
    )

    db.session.add(new_exam)
    db.session.commit()

    return jsonify({"message": "Exam created successfully"})

@app.route('/exams', methods=['GET'])
def fetch_exams():
    exams = Exam.query.all()

    result = []
    for exam in exams:
        result.append({
            "id": exam.id,
            "title": exam.title,
            "duration": exam.duration
        })

    return jsonify(result)
    
if __name__ == "__main__":
        with app.app_context():
            db.create_all()

        app.run(debug=True)
        
        