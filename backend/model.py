import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

INDEX_FILE = "faiss_index/index.faiss"
DATA_FILE = "data.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

try:
    with open(DATA_FILE, "r") as f:
        qa_data = json.load(f)
except FileNotFoundError:
    qa_data = []

if len(qa_data) > 0:
    embeddings = model.encode([q["question"] for q in qa_data])
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
else:
    index = faiss.IndexFlatL2(384)

def qa_model(question):
    if len(qa_data) == 0:
        return "I don’t know yet."
    q_emb = model.encode([question])
    D, I = index.search(np.array(q_emb), 1)
    return qa_data[I[0][0]]["answer"]

def add_qa_pair(question, answer):
    qa_data.append({"question": question, "answer": answer})
    with open(DATA_FILE, "w") as f:
        json.dump(qa_data, f, indent=2)
    emb = model.encode([question])
    index.add(np.array(emb))
    faiss.write_index(index, INDEX_FILE)
