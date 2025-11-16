import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Solve() {
  const { userId } = useParams();
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get(`/get_question/${userId}`);
        setQuestion(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [userId]);

  if (loading) return <div>Loading question…</div>;
  if (!question) return <div>No question found.</div>;

  const options = [
    { key: "option_a", text: question.option_a },
    { key: "option_b", text: question.option_b },
    { key: "option_c", text: question.option_c },
    { key: "option_d", text: question.option_d },
  ];

  return (
    <div>
      <Navbar center="Solve Challenge" />

      <div style={styles.container}>
        <h2>{question.question_text}</h2>

        <div style={{ marginTop: 20 }}>
          {options.map((opt) => (
            <div
              key={opt.key}
              onClick={() => setSelected(opt.key)}
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #ccc",
                marginBottom: "10px",
                cursor: "pointer",
                background: selected === opt.key ? "#dbeafe" : "white"
              }}
            >
              {opt.text}
            </div>
          ))}
        </div>

        <button
          style={styles.btn}
          onClick={() => alert(`You selected: ${selected}`)}
        >
          Submit (demo only)
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    width: "90%",
    maxWidth: "600px",
    margin: "2rem auto",
  },
  btn: {
    marginTop: "20px",
    padding: "12px",
    width: "100%",
    background: "#3b82f6",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  }
};
