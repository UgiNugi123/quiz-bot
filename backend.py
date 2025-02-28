from flask import Flask, request, jsonify

app = Flask(__name__)

db = {
    "categories": ["Science", "History", "Math"],
    "questions": [],
    "quizzes": [],
    "results": []
}

@app.route("/categories", methods=["GET"])
def get_categories():
    return jsonify(db["categories"])

@app.route("/questions", methods=["POST"])
def add_question():
    data = request.json
    db["questions"].append(data)
    return jsonify({"message": "Question added", "question": data})

@app.route("/quiz/create", methods=["POST"])
def create_quiz():
    data = request.json
    category = data["category"]
    questions = [q for q in db["questions"] if q["category"] == category]
    quiz = {"id": len(db["quizzes"])+1, "category": category, "questions": questions, "approved": False}
    db["quizzes"].append(quiz)
    return jsonify({"message": "Quiz created", "quiz_id": quiz["id"]})

@app.route("/quiz/approve/<int:quiz_id>", methods=["POST"])
def approve_quiz(quiz_id):
    for quiz in db["quizzes"]:
        if quiz["id"] == quiz_id:
            quiz["approved"] = True
            return jsonify({"message": "Quiz approved"})
    return jsonify({"error": "Quiz not found"}), 404

@app.route("/quiz/start/<int:quiz_id>", methods=["POST"])
def start_quiz(quiz_id):
    for quiz in db["quizzes"]:
        if quiz["id"] == quiz_id and quiz["approved"]:
            return jsonify({"message": "Quiz started", "quiz": quiz})
    return jsonify({"error": "Quiz not approved or found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
