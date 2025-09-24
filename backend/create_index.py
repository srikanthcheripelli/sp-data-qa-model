import faiss
from sentence_transformers import SentenceTransformer
import pickle
import numpy as np

# Your Q&A list
qa_list = [
    {"question": "What are the key metrics in supply planning?",
     "answer": "Key metrics include forecast accuracy, inventory levels, on-time delivery, production efficiency, capacity utilization, and order fulfillment rate."},
    {"question": "How do you calculate inventory turnover?",
     "answer": "Inventory turnover = Cost of Goods Sold (COGS) / Average Inventory."},
    {"question": "What is safety stock?",
     "answer": "Safety stock is extra inventory kept to avoid stockouts due to demand variability or supply delays."},
    # Add more Q&A here
]

# Save QA list
with open("qaData.pkl", "wb") as f:
    pickle.dump(qa_list, f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute embeddings
embeddings = model.encode([qa["question"] for qa in qa_list])
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, "qaIndex.faiss")

print("FAISS index and QA data created successfully!")

