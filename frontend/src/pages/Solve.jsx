import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Solve() {
  const nav = useNavigate();
  const { id: routeUserId } = useParams(); // /solve/:id

  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState(null);
  const [choice, setChoice] = useState(null);
  const [submitResult, setSubmitResult] = useState(null);
  const [error, setError] = useState("");

  // Step 1 — Fetch today's question
  useEffect(() => {
    async function loadQuestion() {
      setError("");
      setSubmitResult(null);

      const user_id = routeUserId || localStorage.getItem("user_id");
      if (!user_id) {
        nav("/signin");
        return;
      }

      // confirm paired
      try {
        const statusRes = await api.get(`/pair/status/${user_id}`);
        if (statusRes.data.pair_id === null) {
          setError("You do not have a pair yet.");
          setLoading(false);
          return;
        }
      } catch (err) {
        console.error(err);
        setError("Failed to check pair status.");
        setLoading(false);
        return;
      }

      // fetch question
      try {
        const res = await api.get(`/todays-task/${user_id}`);
        const raw = res.data;

        // Transform unified backend response
        const formatted = {
          id: raw.id,
          title: "Daily Coding Challenge",
          description: raw.question,
          options: raw.options, // <-- dictionary {A: "...", B: "..."}
        };

        setQuestion(formatted);
      } catch (err) {
        console.error(err);
        setError("No question assigned yet.");
      } finally {
        setLoading(false);
      }
    }

    loadQuestion();
  }, [nav, routeUserId]);

  // Step 2 — Submit answer
  async function submitAnswer() {
    const user_id = routeUserId || localStorage.getItem("user_id");
    if (!choice) return;

    try {
      const res = await api.post("/check-answer", {
        user_id: user_id,
        question_id: question.id,
        choice: choice, // MUST match backend
      });

      setSubmitResult(res.data.correct);
    } catch (err) {
      console.error(err);
      setError("Failed to submit answer.");
    }
  }

  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <h2>Today's Challenge</h2>

        {loading && <p>Loading question...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {/* Prevent render crashes with strong guards */}
        {!loading && question && question.options && (
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
                    onChange={() => setChoice(letter)}
                  />
                  <strong>{letter}.</strong> {text}
                </label>
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
              <p
                style={{
                  color: submitResult ? "green" : "red",
                  marginTop: "1rem",
                }}
              >
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
  },
  option: {
    display: "block",
    margin: "0.5rem 0",
    textAlign: "left",
    paddingLeft: "1rem",
  },
};
