import React, { useState } from "react";
import qaData from "./qaData";

function QnA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  // Simple fuzzy search function
  const fuzzySearch = (q) => {
    const lowerQ = q.trim().toLowerCase();

    // 1. Exact match
    let found = qaData.find(
      (item) => item.question.toLowerCase() === lowerQ
    );
    if (found) return found.answer;

    // 2. Partial match (contains)
    found = qaData.find(
      (item) => item.question.toLowerCase().includes(lowerQ)
    );
    if (found) return found.answer;

    // 3. Word overlap scoring (optional, more advanced)
    const words = lowerQ.split(" ").filter(Boolean);
    let bestScore = 0;
    let bestMatch = null;
    qaData.forEach((item) => {
      const itemWords = item.question.toLowerCase().split(" ");
      const score = words.filter((w) => itemWords.includes(w)).length;
      if (score > bestScore) {
        bestScore = score;
        bestMatch = item;
      }
    });
    if (bestMatch && bestScore > 0) return bestMatch.answer;

    // No match
    return "❌ Sorry, I don't have an answer for that question yet.";
  };

  const handleAsk = async () => {
    if (!question.trim()) {
      setAnswer("⚠️ Please type a question first!");
      return;
    }
    setLoading(true);
    const ans = await fuzzySearch(question);
    setAnswer(ans);
    setLoading(false);
  };

  return (
    <div
      style={{
        marginTop: "30px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "15px",
        backgroundColor: "#f5f5f5",
        padding: "25px",
        borderRadius: "10px",
        boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
        width: "400px",
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask your question..."
        style={{
          padding: "10px",
          width: "100%",
          borderRadius: "5px",
          border: "1px solid #ccc",
          fontSize: "16px",
        }}
      />
      <button
        onClick={handleAsk}
        style={{
          padding: "10px 20px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          fontSize: "16px",
          fontWeight: "bold",
        }}
      >
        Ask
      </button>
      {loading ? (
        <p style={{ marginTop: "15px" }}>⏳ Fetching answer...</p>
      ) : (
        answer && (
          <p
            style={{
              marginTop: "15px",
              backgroundColor: "#e0f7fa",
              padding: "10px",
              borderRadius: "5px",
              width: "100%",
              textAlign: "center",
              fontWeight: "500",
            }}
          >
            {answer}
          </p>
        )
      )}
    </div>
  );
}

export default QnA;

