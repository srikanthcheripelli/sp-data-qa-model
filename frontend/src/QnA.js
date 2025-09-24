const fetchAnswer = async (q) => {
  try {
    const res = await fetch("http://localhost:5000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q }),
    });
    const data = await res.json();
    return data.answer;
  } catch (err) {
    return "❌ Error fetching answer. Please try again.";
  }
};

