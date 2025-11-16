import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Dashboard() {
  const nav = useNavigate();
  const [paired, setPaired] = useState(false);

  return (
    <>
      <Navbar />

      <div style={styles.section}>
        {/* Duo card */}
        <div style={styles.card}>
          {!paired ? (
            <>
              <h3>No Study Buddy Yet</h3>
              <button style={styles.btn} onClick={() => nav("/matching")}>
                Pair Me
              </button>
            </>
          ) : (
            <>
              <h3>You & Alex</h3>
              <p>Shared courses: CPSC 121, 210</p>
            </>
          )}
        </div>

        {/* Today's Challenge */}
        <div style={styles.card}>
          <h3>Today's Challenge: Problem 1</h3>
          <button style={styles.btn} onClick={() => nav("/solve/1")}>
            Start Challenge
          </button>
        </div>

        {/* Stats */}
        <div style={styles.card}>
          <h3>Your Stats</h3>
          <p>Points: 120</p>
          <p>Streak: 🔥 5 days</p>
        </div>
      </div>
    </>
  );
}

const styles = {
  section: { padding: "2rem", display: "flex", flexDirection: "column", gap: "1.5rem" },
  card: {
    background: "#f7f7f7",
    padding: "1.5rem",
    borderRadius: "12px"
  },
  btn: {
    padding: "0.75rem",
    background: "#3b82f6",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    marginTop: "0.5rem"
  }
};
