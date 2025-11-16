import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Solve() {
  const nav = useNavigate();
  const { id: routeUserId } = useParams();

  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState(null);
  const [choice, setChoice] = useState(null);
  const [submitResult, setSubmitResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadQuestion() {
      setError("");
      setSubmitResult(null);
      setChoice(null);

      const user_id = routeUserId || localStorage.getItem("user_id");
      if (!user_id) {
        nav("/signin");
        return;
      }

      try {
        const statusRes = await api.get(`/pair/status/${user_id}`);
        if (statusRes.data.pair_id === null) {
          setError("You do not have a pair yet.");
          setLoading(false);
          return;
        }
      } catch (err) {
        console.error("Pair status error:", err);
        setError("Failed to check pair status.");
        setLoading(false);
        return;
      }

      try {
        const res = await api.get(`/todays-task/${user_id}`);
        const raw = res.data;

        if (!raw || !raw.options || typeof raw.options !== "object") {
          throw new Error("Invalid question format received");
        }

        const formatted = {
          id: raw.id,
          title: "Daily Coding Challenge",
          description: raw.question,
          options: raw.options,
        };

        setQuestion(formatted);
      } catch (err) {
        console.error("Question fetch error:", err);
        setError("No question assigned yet.");
      } finally {
        setLoading(false);
      }
    }

    loadQuestion();
  }, [nav, routeUserId]);

  async function submitAnswer() {
    const user_id = routeUserId || localStorage.getItem("user_id");
    
    if (!choice) {
      alert("Please select an answer first");
      return;
    }

    if (!question || !question.id) {
      setError("Question data is missing");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      const res = await api.post("/check-answer", {
        user_id: user_id,
        question_id: question.id,
        choice: choice,
      });

      const isCorrect = res.data.correct === true;

      setSubmitResult(isCorrect);

    } catch (err) {
      console.error("Submit error:", err);
      setError("Failed to submit answer.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <h2>Today's Challenge</h2>

        {loading && <p>Loading question...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {!loading && !error && question && question.options && typeof question.options === "object" && (
          <div style={styles.card}>
            <h3>{question.title}</h3>
            <p>{question.description}</p>

            <div style={{ marginTop: "1rem" }}>
              {Object.entries(question.options).map(([letter, text]) => (
                <label key={letter} style={styles.option}>
                  <input
                    type="radio"
                    name="mcq"
                    value={letter}
                    checked={choice === letter}
                    onChange={() => setChoice(letter)}
                    disabled={submitResult !== null}
                  />
                  <strong>{letter}.</strong> {text}
                </label>
              ))}
            </div>

            <button
              style={{
                ...styles.btn,
                opacity: (!choice || submitting) ? 0.5 : 1,
                cursor: (!choice || submitting) ? "not-allowed" : "pointer",
              }}
              disabled={!choice || submitting}
              onClick={submitAnswer}
            >
              {submitting ? "Submitting..." : "Submit Answer"}
            </button>

            {submitResult !== null && (
              <div
                style={{
                  marginTop: "1.5rem",
                  padding: "1rem",
                  borderRadius: "8px",
                  backgroundColor: submitResult ? "#d4edda" : "#f8d7da",
                  border: submitResult ? "2px solid #28a745" : "2px solid #dc3545",
                }}
              >
                <p
                  style={{
                    color: submitResult ? "#155724" : "#721c24",
                    fontWeight: "bold",
                    fontSize: "1.2rem",
                    margin: 0,
                  }}
                >
                  {submitResult ? "✓ Correct! 🎉" : "✗ Incorrect ❌"}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}

const styles = {
  container: {
    width: "70%",
    margin: "2rem auto",
    textAlign: "center",
  },
  card: {
    background: "#f5f5f5",
    padding: "1.5rem",
    borderRadius: "12px",
    marginTop: "1rem",
  },
  btn: {
    marginTop: "1.5rem",
    padding: "0.75rem 1.25rem",
    background: "#3b82f6",
    color: "#fff",
    borderRadius: "10px",
    border: "none",
    cursor: "pointer",
    fontSize: "1rem",
    fontWeight: "600",
  },
  option: {
    display: "block",
    margin: "0.5rem 0",
    textAlign: "left",
    paddingLeft: "1rem",
    cursor: "pointer",
  },
};
