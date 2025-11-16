import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Solve() {
  const nav = useNavigate();

  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState(null);
  const [choice, setChoice] = useState(null);
  const [submitResult, setSubmitResult] = useState(null);
  const [error, setError] = useState("");

  //  Step 1 — Fetch today's question automatically
  useEffect(() => {
    async function loadQuestion() {
      setError("");
      setSubmitResult(null);

      const user_id = localStorage.getItem("user_id");

      // not logged in
      if (!user_id) {
        nav("/signin");
        return;
      }

      // check paired before fetching question
      try {
        const statusRes = await api.get(`/pair/status/${user_id}`);
        if (statusRes.data.pair_id === null) {
          setError("You do not have a pair yet.");
          return;
        }
      } catch (err) {
        console.error(err);
        setError("Failed to check pair status.");
        return;
      }

      // fetch actual question
      try {
        const res = await api.get(`/todays-task/${user_id}`);
        setQuestion(res.data);
      } catch (err) {
        console.error(err);
        setError("No question assigned yet. Ask your partner to complete pairing.");
      } finally {
        setLoading(false);
      }
    }

    loadQuestion();
  }, [nav]);

  // 🔥 Step 2 — Submit the answer
  async function submitAnswer() {
    const user_id = localStorage.getItem("user_id");

    if (!choice) return;

    try {
      const res = await api.post("/check-answer", {
        user_id,
        question_id: question.id,
        choice
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

        {question && !loading && (
          <div style={styles.card}>
            <h3>{question.title}</h3>
            <p>{question.description}</p>

            {/* Options */}
            <div style={{ marginTop: "1rem" }}>
              {question.options.map((opt, index) => (
                <label key={index} style={styles.option}>
                  <input 
                    type="radio" 
                    name="mcq" 
                    value={opt}
                    onChange={() => setChoice(opt)}
                  />
                  {opt}
                </label>
              ))}
            </div>

            {/* Submit button */}
            <button 
              style={styles.btn} 
              disabled={!choice} 
              onClick={submitAnswer}
            >
              Submit Answer
            </button>

            {/* Result */}
            {submitResult !== null && (
              <p style={{ color: submitResult ? "green" : "red", marginTop: "1rem" }}>
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
    textAlign: "center"
  },
  card: {
    background: "#f5f5f5",
    padding: "1.5rem",
    borderRadius: "12px",
    marginTop: "1rem"
  },
  btn: {
    marginTop: "1.5rem",
    padding: "0.75rem 1.25rem",
    background: "#3b82f6",
    color: "#fff",
    borderRadius: "10px",
    border: "none",
    cursor: "pointer"
  },
  option: {
    display: "block",
    margin: "0.5rem 0",
    textAlign: "left",
    paddingLeft: "1rem"
  }
};