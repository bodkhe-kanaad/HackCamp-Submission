import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import { getRandomQuestion, checkAnswer } from "../services/question";

export default function Solve() {
  const { problemId } = useParams();

  const [question, setQuestion] = useState(null);
  const [selected, setSelected] = useState(null);
  const [result, setResult] = useState(null); // "correct" | "wrong"
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadQ() {
      const q = await getRandomQuestion();
      setQuestion(q);
      setLoading(false);
    }
    loadQ();
  }, []);

  if (loading) return <p>Loading question...</p>;

  return (
    <>
      <Navbar />

      <div style={styles.wrapper}>
        <h2>{question.title}</h2>

        <pre style={styles.code}>{question.code}</pre>

        <div style={styles.options}>
          {Object.entries(question.options).map(([letter, text]) => (
            <button
              key={letter}
              style={{
                ...styles.optionBtn,
                background:
                  selected === letter ? "#3b82f6" : "#f1f1f1",
                color: selected === letter ? "white" : "black",
              }}
              onClick={() => setSelected(letter)}
            >
              {letter}. {text}
            </button>
          ))}
        </div>

        <button
          style={styles.submitBtn}
          onClick={async () => {
            if (!selected) return;
            const correct = await checkAnswer(question.id, selected);
            setResult(correct ? "correct" : "wrong");
          }}
        >
          Submit
        </button>

        {result === "correct" && (
          <p style={{ color: "green", fontWeight: "bold" }}>
            ✅ Correct! Great job.
          </p>
        )}

        {result === "wrong" && (
          <p style={{ color: "red", fontWeight: "bold" }}>
            ❌ Incorrect — try again.
          </p>
        )}
      </div>
    </>
  );
}

const styles = {
  wrapper: {
    maxWidth: "700px",
    margin: "2rem auto",
    padding: "1rem"
  },
  code: {
    background: "#f7f7f7",
    padding: "1rem",
    borderRadius: "8px",
    whiteSpace: "pre-wrap",
  },
  options: {
    marginTop: "1rem",
    display: "flex",
    flexDirection: "column",
    gap: "0.75rem"
  },
  optionBtn: {
    padding: "0.75rem",
    borderRadius: "8px",
    border: "1px solid #ddd",
    textAlign: "left",
    cursor: "pointer",
    fontSize: "1rem",
  },
  submitBtn: {
    marginTop: "1.5rem",
    padding: "0.75rem",
    width: "100%",
    borderRadius: "8px",
    border: "none",
    background: "#3b82f6",
    color: "white",
    fontSize: "1.1rem",
    cursor: "pointer",
  }
};
