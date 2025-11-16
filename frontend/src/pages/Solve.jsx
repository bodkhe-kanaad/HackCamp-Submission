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
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

<<<<<<< HEAD
  // Step 1 — Fetch today's question
=======
  // ---------------------------------------------
  // Load today's question
  // ---------------------------------------------
>>>>>>> 3ac752b (Frontend experiment)
  useEffect(() => {
    async function loadQuestion() {
      setError("");
      setSubmitResult(null);
      setChoice(null);

      const user_id = routeUserId || localStorage.getItem("user_id");
      if (!user_id) return nav("/signin");

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

        console.log("Raw question from backend:", raw);

        // Validate response structure
        if (!raw || !raw.options) {
          throw new Error("Invalid question format received");
        }

        setQuestion({
          id: raw.id,
          title: "Daily Coding Challenge",
          description: raw.question,
          options: raw.options,
<<<<<<< HEAD
        };

        console.log("Formatted question:", formatted);
        setQuestion(formatted);
=======
        });
>>>>>>> 3ac752b (Frontend experiment)
      } catch (err) {
        console.error("Question fetch error:", err);
        setError("No question assigned yet.");
      } finally {
        setLoading(false);
      }
    }

    loadQuestion();
  }, [nav, routeUserId]);

<<<<<<< HEAD
  // Step 2 — Submit answer
  async function submitAnswer() {
    const user_id = routeUserId || localStorage.getItem("user_id");
    if (!choice) return;

    if (!question || !question.id) {
      setError("Question data is missing");
      return;
    }
=======
  // ---------------------------------------------
  // Submit answer
  // ---------------------------------------------
  async function submitAnswer() {
    const user_id = routeUserId || localStorage.getItem("user_id");
    if (!choice) return alert("Please select an answer first");
    if (!question?.id) return setError("Question data is missing");
>>>>>>> 3ac752b (Frontend experiment)

    setSubmitting(true);
    setError("");

    try {
      const res = await api.post("/check-answer", {
        user_id,
        question_id: question.id,
        choice,
      });

<<<<<<< HEAD
      console.log("Backend response:", res.data);

      const isCorrect = res.data.correct === true;
      setSubmitResult(isCorrect);

=======
      setSubmitResult(res.data.correct === true);
>>>>>>> 3ac752b (Frontend experiment)
    } catch (err) {
      console.error("Submit error:", err);
      setError("Failed to submit answer. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  // ---------------------------------------------
  // Render
  // ---------------------------------------------
  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <h2>Today's Challenge</h2>

        {/* NEW AI loading text */}
        {loading && (
          <p style={{ fontSize: "1.1rem", opacity: 0.85 }}>
            🤖 AI at work — thinking really hard…
          </p>
        )}

        {error && <p style={{ color: "red" }}>{error}</p>}

<<<<<<< HEAD
        {!loading && !error && question && question.options && (
          <div style={styles.card}>
            <h3>{question.title}</h3>
            <p>{question.description}</p>
=======
        {!loading &&
          !error &&
          question &&
          question.options &&
          typeof question.options === "object" && (
            <>
              <div style={styles.card}>
                <h3>{question.title}</h3>
                <p>{question.description}</p>
>>>>>>> 3ac752b (Frontend experiment)

                <div style={styles.optionsContainer}>
                  {Object.entries(question.options).map(([letter, text]) => {
                    const isSelected = choice === letter;
                    return (
                      <div
                        key={letter}
                        onClick={() => !submitResult && setChoice(letter)}
                        style={{
                          ...styles.optionCard,
                          borderColor: isSelected ? "#3b82f6" : "#ccc",
                          background: isSelected ? "#e8f0fe" : "white",
                          opacity:
                            submitResult && !isSelected ? 0.6 : 1,
                        }}
                      >
                        <strong>{letter}.</strong>
                        <span style={{ marginLeft: "0.5rem" }}>
                          {text}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>

<<<<<<< HEAD
            <button
              style={{
                ...styles.btn,
                opacity: !choice || submitting ? 0.5 : 1,
                cursor: !choice || submitting ? "not-allowed" : "pointer",
              }}
              disabled={!choice || submitting}
              onClick={submitAnswer}
            >
              {submitting ? "Submitting..." : "Submit Answer"}
            </button>

            {/* RESULT DISPLAY */}
            {submitResult !== null && (
              <div
                style={{
                  marginTop: "1.5rem",
                  padding: "1rem",
                  borderRadius: "8px",
                  backgroundColor: submitResult ? "#d4edda" : "#f8d7da",
                  border: submitResult
                    ? "2px solid #28a745"
                    : "2px solid #dc3545",
=======
              <button
                style={{
                  ...styles.btn,
                  opacity: !choice || submitting ? 0.5 : 1,
                  cursor:
                    !choice || submitting ? "not-allowed" : "pointer",
>>>>>>> 3ac752b (Frontend experiment)
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
                    backgroundColor: submitResult
                      ? "#d4edda"
                      : "#f8d7da",
                    border: submitResult
                      ? "2px solid #28a745"
                      : "2px solid #dc3545",
                  }}
                >
<<<<<<< HEAD
                  {submitResult ? "✓ Correct! 🎉" : "✗ Incorrect ❌"}
                </p>
              </div>
            )}

            {/* Debug info */}
            <div style={{ marginTop: "1rem", fontSize: "0.8rem", color: "#666" }}>
              <p>Debug: choice = {choice || "none"}</p>
              <p>Debug: submitResult = {String(submitResult)}</p>
            </div>
          </div>
        )}
=======
                  <p
                    style={{
                      color: submitResult ? "#155724" : "#721c24",
                      fontWeight: "bold",
                      fontSize: "1.2rem",
                      margin: 0,
                    }}
                  >
                    {submitResult
                      ? "✓ Correct! 🎉"
                      : "✗ Incorrect ❌"}
                  </p>
                </div>
              )}
            </>
          )}
>>>>>>> 3ac752b (Frontend experiment)
      </div>
    </>
  );
}

// ---------------------------------------------
// Styles
// ---------------------------------------------
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
  optionsContainer: {
    marginTop: "1rem",
    display: "flex",
    flexDirection: "column",
    gap: "0.75rem",
  },
  optionCard: {
    padding: "1rem",
    borderRadius: "10px",
    border: "2px solid #ccc",
    cursor: "pointer",
    transition: "0.2s ease",
    textAlign: "left",
    display: "flex",
    alignItems: "center",
    fontSize: "1rem",
    background: "white",
    boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
  },
};
