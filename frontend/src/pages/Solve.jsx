import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Solve() {
  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState(null);
  const [choice, setChoice] = useState(null);
  const [submitResult, setSubmitResult] = useState(null);
  const [error, setError] = useState("");

  async function fetchQuestion() {
    setLoading(true);
    setError("");

    const id = localStorage.getItem("user_id");
    if (!id) {
      setError("You are not logged in.");
      setLoading(false);
      return;
    }

    try {
      const res = await api.get(`/todays-task/${id}`);
      setQuestion(res.data);
    } catch (err) {
      console.error(err);
      setError("No question available or backend offline.");
    }

    setLoading(false);
  }

  async function submitAnswer() {
    setSubmitResult(null);

    const id = localStorage.getItem("user_id");
    if (!id) return;

    try {
      const res = await api.post("/check-answer", {
        user_id: id,
        question_id: question.id,
        choice: choice
      });

      setSubmitResult(res.data.correct);
    } catch (err) {
      console.error(err);
      setError("Failed to submit answer.");
    }
  }

  useEffect(() => {
    fetchQuestion();
  }, []);

  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <h2>Today's Challenge</h2>

        {loading && <p>Loading question...</p>}

        {error && <p style={{ color: "red" }}>{error}</p>}

        {question && (
          <div style={styles.card}>
            <h3>{question.title}</h3>
            <p>{question.description}</p>

            <div style={{ marginTop: "1rem" }}>
              {question.options.map((opt, idx) => (
                <div key={idx} style={styles.option}>
                  <input
                    type="radio"
                    id={`opt-${idx}`}
                    name="mcq"
                    value={opt}
                    onChange={() => setChoice(opt)}
                  />
                  <label htmlFor={`opt-${idx}`}>{opt}</label>
                </div>
              ))}
            </div>

            <button
              style={styles.btn}
              disabled={!choice}
              onClick={submitAnswer}
            >
              Submit Answer
            </button>

            {submitResult !== null && (
              <p style={{ color: submitResult ? "green" : "red" }}>
                {submitResult ? "Correct! 🎉" : "Incorrect ❌"}
              </p>
            )}
          </div>
        )}
      </div>
    </>
  );
}

const styles = {
  container: { width: "70%", margin: "2rem auto", textAlign: "center" },
  card: { background: "#f5f5f5", padding: "1.5rem", borderRadius: "12px", marginBottom: "1.5rem" },
  btn: {
    marginTop: "1rem",
    padding: "0.75rem 1.25rem",
    background: "#3b82f6",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer"
  },
  option: { padding: "0.5rem", textAlign: "left" }
};