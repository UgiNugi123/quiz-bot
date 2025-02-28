from flask import Flask, request, jsonify
from datetime import datetime
import streamlit as st
import requests

app = Flask(__name__)

db = {
    "categories": ["Science", "History", "Math"],
    "questions": [],
    "quizzes": [],
    "results": []
}

# 1. Fetch Categories
@app.route("/categories", methods=["GET"])
def get_categories():
    return jsonify(db["categories"])

# 2. Add Questions
@app.route("/questions", methods=["POST"])
def add_question():
    data = request.json
    db["questions"].append(data)
    return jsonify({"message": "Question added", "question": data})

# 3. Get Questions by Category
@app.route("/questions", methods=["GET"])
def get_questions():
    category = request.args.get("category")
    questions = [q for q in db["questions"] if q["category"] == category]
    return jsonify(questions)

# 4. Create Quiz
@app.route("/quiz/create", methods=["POST"])
def create_quiz():
    data = request.json
    category = data["category"]
    questions = [q for q in db["questions"] if q["category"] == category]
    quiz = {"id": len(db["quizzes"])+1, "category": category, "questions": questions, "approved": False}
    db["quizzes"].append(quiz)
    return jsonify({"message": "Quiz created", "quiz_id": quiz["id"]})

# 5. Approve Quiz
@app.route("/quiz/approve/<int:quiz_id>", methods=["POST"])
def approve_quiz(quiz_id):
    for quiz in db["quizzes"]:
        if quiz["id"] == quiz_id:
            quiz["approved"] = True
            return jsonify({"message": "Quiz approved"})
    return jsonify({"error": "Quiz not found"}), 404

# 6. Start Quiz
@app.route("/quiz/start/<int:quiz_id>", methods=["POST"])
def start_quiz(quiz_id):
    for quiz in db["quizzes"]:
        if quiz["id"] == quiz_id and quiz["approved"]:
            return jsonify({"message": "Quiz started", "quiz": quiz})
    return jsonify({"error": "Quiz not approved or found"}), 404

# 7. Submit Quiz
@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.json
    db["results"].append(data)
    return jsonify({"message": "Quiz submitted", "result": data})

# 8. Get Quiz Results
@app.route("/quiz/results/<int:quiz_id>", methods=["GET"])
def get_results(quiz_id):
    results = [r for r in db["results"] if r["quiz_id"] == quiz_id]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

# Streamlit Frontend
st.title("Quiz Bot UI")

st.sidebar.header("Quiz Options")
category = st.sidebar.selectbox("Select Category", db["categories"])

if st.sidebar.button("Create Quiz"):
    response = requests.post("http://127.0.0.1:5000/quiz/create", json={"category": category})
    st.success(response.json()["message"])

quiz_id = st.sidebar.number_input("Enter Quiz ID to Approve", min_value=1)
if st.sidebar.button("Approve Quiz"):
    response = requests.post(f"http://127.0.0.1:5000/quiz/approve/{quiz_id}")
    st.success(response.json()["message"])

if st.sidebar.button("Start Quiz"):
    response = requests.post(f"http://127.0.0.1:5000/quiz/start/{quiz_id}")
    if "quiz" in response.json():
        st.write(response.json()["quiz"])
    else:
        st.error(response.json()["error"])