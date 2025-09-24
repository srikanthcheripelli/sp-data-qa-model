from flask import Flask, request, jsonify
from flask_cors import CORS
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle

app = Flask(__name__)
CORS(app)

# Load Q&A data
with open("qaData.pkl", "rb") as f:
    qa_list = pickle.load(f)

# Load FAISS index
index = faiss.read_index("qaIndex.faiss")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.json
    question = data.get("question", "")
    if not question.strip():
        return jsonify({"answer": "⚠️ Please type a question first!"})

    # Generate embedding
    q_vec = model.encode([question])
    q_vec = np.array(q_vec).astype("float32")

    # Search FAISS
    D, I = index.search(q_vec, k=1)
    idx = I[0][0]
    answer = qa_list[idx]["answer"]
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(port=5000, debug=True)

