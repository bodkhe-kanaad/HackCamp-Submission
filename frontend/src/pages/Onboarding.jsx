import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Onboarding() {
  const nav = useNavigate();

  const coursesList = [
    "CPSC 110", "CPSC 121", "CPSC 210",
    "CPSC 213", "CPSC 221", "CPSC 320"
  ];

  const goals = ["Interview Prep", "Pass Classes", "Get Better"];

  // Controlled UI state (ONLY UI — backend untouched)
  const [name, setName] = useState("");
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [selectedGoal, setSelectedGoal] = useState(null);

  // Toggle chip selection
  const toggleCourse = (course) => {
    setSelectedCourses((prev) =>
      prev.includes(course)
        ? prev.filter((c) => c !== course)
        : [...prev, course]
    );
  };

  return (
    <>
      <Navbar />

      {/* Background */}
      <div style={styles.bg}>
        <div style={styles.card}>

          <h2 style={styles.title}>Complete Your Profile</h2>
          <p style={styles.subtitle}>
            We’ll personalize your pairing based on your learning journey.
          </p>

          {/* Name Input */}
          <input
            placeholder="Your Name"
            style={styles.input}
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          {/* COURSE MULTI-SELECT */}
          <h3 style={styles.sectionTitle}>Courses</h3>
          <div style={styles.chipGroup}>
            {coursesList.map((c) => {
              const active = selectedCourses.includes(c);
              return (
                <div
                  key={c}
                  onClick={() => toggleCourse(c)}
                  style={{
                    ...styles.chip,
                    background: active ? "#dbeafe" : "#fff",
                    borderColor: active ? "#3b82f6" : "#cbd5e1",
                    color: active ? "#1e40af" : "#334155",
                  }}
                >
                  {c}
                </div>
              );
            })}
          </div>

          {/* GOAL SELECTION */}
          <h3 style={styles.sectionTitle}>Your Goal</h3>
          <div style={styles.radioGroup}>
            {goals.map((g) => {
              const active = selectedGoal === g;
              return (
                <div
                  key={g}
                  onClick={() => setSelectedGoal(g)}
                  style={{
                    ...styles.radioCard,
                    borderColor: active ? "#3b82f6" : "#d1d5db",
                    background: active ? "#eff6ff" : "#fff",
                    color: active ? "#1e40af" : "#334155",
                  }}
                >
                  <div
                    style={{
                      ...styles.radioCircle,
                      borderColor: active ? "#3b82f6" : "#94a3b8",
                      background: active ? "#3b82f6" : "transparent",
                    }}
                  />
                  {g}
                </div>
              );
            })}
          </div>

          {/* Submit */}
          <button
            style={{
              ...styles.btn,
              opacity: name && selectedGoal ? 1 : 0.5,
              cursor: name && selectedGoal ? "pointer" : "not-allowed",
            }}
            onClick={() => nav("/dashboard")}
            disabled={!name || !selectedGoal}
          >
            Finish Onboarding
          </button>

        </div>
      </div>
    </>
  );
}

const styles = {
  bg: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #eef2ff, #fff7ed, #f0fdf4)",
    padding: "2rem",
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
  },

  card: {
    width: "420px",
    background: "rgba(255,255,255,0.88)",
    backdropFilter: "blur(14px)",
    borderRadius: "18px",
    padding: "2rem",
    boxShadow: "0 6px 26px rgba(0,0,0,0.10)",
    animation: "fadeIn 0.6s ease"
  },

  title: {
    fontSize: "1.8rem",
    fontWeight: 700,
    textAlign: "center",
    marginBottom: "0.4rem"
  },

  subtitle: {
    textAlign: "center",
    color: "#64748b",
    marginBottom: "1.4rem"
  },

  input: {
    width: "100%",
    padding: "0.9rem",
    borderRadius: "12px",
    border: "1px solid #d1d5db",
    marginBottom: "1.5rem",
    fontSize: "1rem"
  },

  sectionTitle: {
    marginTop: "1rem",
    marginBottom: "0.6rem",
    fontSize: "1.15rem",
    fontWeight: 600
  },

  /* CHIPS */
  chipGroup: {
    display: "flex",
    flexWrap: "wrap",
    gap: "0.6rem",
    marginBottom: "1.5rem"
  },

  chip: {
    padding: "0.55rem 1rem",
    borderRadius: "999px",
    border: "2px solid #cbd5e1",
    fontSize: "0.95rem",
    cursor: "pointer",
    transition: "0.2s ease",
    userSelect: "none"
  },

  /* RADIO CARDS */
  radioGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "0.7rem",
    marginBottom: "1.5rem",
  },

  radioCard: {
    display: "flex",
    alignItems: "center",
    gap: "0.8rem",
    padding: "1rem",
    borderRadius: "12px",
    border: "2px solid #d1d5db",
    cursor: "pointer",
    fontWeight: 500,
    transition: "0.25s ease",
  },

  radioCircle: {
    width: "16px",
    height: "16px",
    borderRadius: "50%",
    border: "2px solid #94a3b8",
    transition: "0.25s ease",
  },

  btn: {
    marginTop: "1rem",
    width: "100%",
    padding: "1rem",
    borderRadius: "12px",
    border: "none",
    background: "#3b82f6",
    color: "white",
    fontSize: "1.05rem",
    fontWeight: 600,
    cursor: "pointer",
    transition: "0.2s ease",
  },
};