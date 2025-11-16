import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function Landing() {
  const nav = useNavigate();

  return (
    <>
      <Navbar />

      <div style={styles.wrapper}>
        <h1>Find Your Coding Study Buddy</h1>
        <p>Pair with real students, solve problems daily, and stay accountable.</p>

        <button style={styles.cta} onClick={() => nav("/signup")}>
          Get Started
        </button>

        <div style={styles.how}>
          <div style={styles.card}>Match with a buddy</div>
          <div style={styles.card}>Solve daily problems</div>
          <div style={styles.card}>Win together</div>
        </div>
      </div>
    </>
  );
}

const styles = {
  wrapper: { textAlign: "center", padding: "4rem 2rem" },
  cta: {
    padding: "0.75rem 1.5rem",
    fontSize: "1.1rem",
    marginTop: "1rem",
    background: "#3b82f6",
    border: "none",
    color: "#fff",
    borderRadius: "8px",
    cursor: "pointer"
  },
  how: {
    marginTop: "3rem",
    display: "flex",
    justifyContent: "center",
    gap: "1.5rem"
  },
  card: {
    padding: "1.5rem",
    background: "#f7f7f7",
    borderRadius: "12px",
    width: "200px"
  }
};

