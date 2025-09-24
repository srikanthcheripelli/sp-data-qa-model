from flask import Flask, request, jsonify
from model import qa_model, add_qa_pair

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = qa_model(question)
    return jsonify({"answer": answer})

@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")
    if question and answer:
        add_qa_pair(question, answer)
        return jsonify({"status": "success"})
    return jsonify({"status": "failed", "reason": "missing question/answer"}), 400

if __name__ == "__main__":
    app.run(debug=True)
