import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Dashboard() {
  const nav = useNavigate();

  const [user, setUser] = useState(null);
  const [pairBasic, setPairBasic] = useState(null);
  const [pairFull, setPairFull] = useState(null);

  const [loadingUser, setLoadingUser] = useState(true);
  const [loadingPair, setLoadingPair] = useState(false);
  const [error, setError] = useState("");
  const [pairError, setPairError] = useState("");

  // --------------------------
  // LOAD DATA
  // --------------------------
  useEffect(() => {
    async function load() {
      const id = localStorage.getItem("user_id");
      if (!id) {
        setError("No session found — please log in again.");
        return;
      }

      try {
        const userRes = await api.get(`/user/${id}`);
        setUser(userRes.data);
      } catch {
        setError("Failed to load profile.");
      }

      try {
        const pairRes = await api.get(`/pair/status/${id}`);
        if (pairRes.data.pair_id !== null) {
          setPairBasic(pairRes.data);

          const mate = await api.get(`/pair/mate/${id}`);
          setPairFull(mate.data);
        }
      } catch (err) {
        console.error("Pair error:", err);
      }

      setLoadingUser(false);
    }

    load();
  }, []);

  // --------------------------
  // PAIR USER
  // --------------------------
  async function handlePair() {
    setPairError("");
    setLoadingPair(true);
    const id = localStorage.getItem("user_id");

    try {
      const res = await api.post("/pair", { user_id: id });
      setPairBasic(res.data);

      const mate = await api.get(`/pair/mate/${id}`);
      setPairFull(mate.data);
    } catch {
      setError("Pairing failed. Try again.");
    }

    setLoadingPair(false);
  }

  return (
    <>
      <Navbar />

      <div style={styles.page}>
        <div style={styles.container}>

          <h1 style={styles.title}>Your Dashboard</h1>

          {/* ERROR */}
          {error && <p style={styles.error}>{error}</p>}

          {/* LOADING SKELETON */}
          {loadingUser && <div style={styles.skeleton}></div>}

          {/* --------------------- */}
          {/* USER PROFILE CARD     */}
          {/* --------------------- */}
          {user && !loadingUser && (
            <div style={styles.card}>
              <h2 style={styles.cardTitle}>👋 Welcome, {user.username}</h2>

              <div style={styles.row}>
                <span style={styles.label}>Courses</span>
                <span>{user.courses.join(", ") || "None"}</span>
              </div>

              <div style={styles.row}>
                <span style={styles.label}>Interests</span>
                <span>{user.interests.join(", ") || "None"}</span>
              </div>

              {!pairBasic && (
                <button
                  style={styles.primaryButton}
                  onClick={handlePair}
                  disabled={loadingPair}
                >
                  {loadingPair ? "Finding your best match..." : "Find Study Partner"}
                </button>
              )}
            </div>
          )}

          {/* --------------------- */}
          {/* PARTNER CARD          */}
          {/* --------------------- */}
          {pairFull && (
            <div style={styles.card}>
              <h2 style={styles.cardTitle}>🤝 You’re Paired!</h2>

              <div style={styles.partnerBox}>
                <div style={styles.avatar}>
                  {pairFull.partner.username[0].toUpperCase()}
                </div>

                <div>
                  <h3 style={styles.partnerName}>
                    {pairFull.partner.username}
                  </h3>
                  <p style={styles.partnerLine}>
                    <strong>Courses:</strong> {pairFull.partner.courses.join(", ")}
                  </p>
                  <p style={styles.partnerLine}>
                    <strong>Interests:</strong> {pairFull.partner.interests.join(", ")}
                  </p>

                  <p style={styles.streakLine}>
                    🔥 Streak: <strong>{pairFull.streak || 0}</strong> days
                  </p>
                </div>
              </div>

              {/* AI MODE TOGGLE */}
              <div style={styles.toggleRow}>
                <span style={styles.label}>AI Mode</span>
                <Toggle
                  value={pairFull.ai_mode}
                  onChange={async (newState) => {
                    try {
                      await api.post("/pair/toggle-mode", {
                        user_id: user.user_id,
                        ai_mode: newState,
                      });
                      setPairFull({ ...pairFull, ai_mode: newState });
                    } catch {
                      alert("Could not toggle AI mode.");
                    }
                  }}
                />
              </div>
            </div>
          )}

          {/* --------------------- */}
          {/* TASK CTA              */}
          {/* --------------------- */}
          {pairBasic && (
            <div style={styles.taskCard}>
              <h3 style={styles.taskTitle}>📘 Today’s Challenge</h3>
              <p style={styles.taskText}>
                Complete today’s question with your partner or with AI mode.
              </p>

              <button
                style={styles.taskButton}
                onClick={() => nav(`/solve/${user.user_id}`)}
              >
                Start Task →
              </button>
            </div>
          )}

        </div>
      </div>
    </>
  );
}

/* -------------------------------------------
   MODERN iOS-STYLE TOGGLE
-------------------------------------------- */
function Toggle({ value, onChange }) {
  return (
    <div
      onClick={() => onChange(!value)}
      style={{
        width: 46,
        height: 26,
        borderRadius: 20,
        background: value ? "#34d399" : "#cbd5e1",
        position: "relative",
        cursor: "pointer",
        transition: "0.2s",
      }}
    >
      <div
        style={{
          width: 20,
          height: 20,
          borderRadius: "50%",
          background: "#fff",
          position: "absolute",
          top: 3,
          left: value ? 22 : 3,
          transition: "0.2s",
          boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
        }}
      />
    </div>
  );
}

/* -------------------------------------------
   STYLES
-------------------------------------------- */
const styles = {
  page: {
    minHeight: "100vh",
    width: "100%",
    background: "linear-gradient(135deg, #eef2ff, #fdf2f8, #ecfdf5)",
    padding: "2rem 0",
    display: "block",
  },

  container: {
    width: "95%",
    maxWidth: "680px",
    margin: "0 auto",
    padding: "0 1rem",
    boxSizing: "border-box",
  },

  title: {
    textAlign: "center",
    fontSize: "2rem",
    fontWeight: 800,
    marginBottom: "1.5rem",
  },

  error: {
    color: "red",
    textAlign: "center",
    fontSize: "0.95rem",
  },

  skeleton: {
    height: "180px",
    background: "#e5e7eb",
    borderRadius: "14px",
    animation: "pulse 1.5s infinite",
    marginBottom: "1.5rem",
  },

  card: {
    background: "#fff",
    padding: "1.8rem",
    borderRadius: "16px",
    boxShadow: "0 4px 15px rgba(0,0,0,0.05)",
    marginBottom: "1.5rem",
  },

  cardTitle: {
    fontSize: "1.4rem",
    fontWeight: 700,
    marginBottom: "1rem",
  },

  row: {
    display: "flex",
    marginBottom: "0.6rem",
    gap: "0.5rem",
  },

  label: {
    fontWeight: 600,
    opacity: 0.75,
  },

  primaryButton: {
    width: "100%",
    padding: "0.9rem",
    background: "#3b82f6",
    borderRadius: "12px",
    color: "#fff",
    border: "none",
    fontWeight: 600,
    cursor: "pointer",
    marginTop: "1rem",
  },

  partnerBox: {
    display: "flex",
    gap: "1rem",
  },

  avatar: {
    width: "55px",
    height: "55px",
    borderRadius: "50%",
    background: "#3b82f6",
    color: "#fff",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontSize: "1.4rem",
    fontWeight: 700,
  },

  partnerName: {
    margin: 0,
    fontSize: "1.3rem",
    fontWeight: 700,
  },

  partnerLine: {
    marginTop: "4px",
    opacity: 0.75,
  },

  streakLine: {
    marginTop: "0.5rem",
    fontSize: "1rem",
    fontWeight: 600,
  },

  toggleRow: {
    marginTop: "1.2rem",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },

  taskCard: {
    background: "#f0f9ff",
    padding: "1.6rem",
    borderRadius: "16px",
    textAlign: "center",
    boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
  },

  taskTitle: {
    fontSize: "1.25rem",
    fontWeight: 700,
  },

  taskText: {
    marginTop: "0.5rem",
    opacity: 0.8,
  },

  taskButton: {
    marginTop: "1rem",
    padding: "0.8rem 1.4rem",
    background: "#10b981",
    borderRadius: "10px",
    border: "none",
    color: "#fff",
    fontWeight: 600,
    cursor: "pointer",
  },

  accentButton: {
    marginTop: "1rem",
    padding: "0.8rem",
    width: "100%",
    background: "#10b981",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: 600,
  },

  partnerCard: {
    marginTop: "2rem",
    background: "#effdf5",
    padding: "1.5rem",
    borderRadius: "14px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
    textAlign: "left",
  },

  partnerTitle: {
    fontSize: "1.4rem",
    fontWeight: 700,
    marginBottom: "1rem",
  },

  switch: {
    position: "relative",
    display: "inline-block",
    width: "48px",
    height: "24px",
  },

  slider: {
    position: "absolute",
    cursor: "pointer",
    top: "0",
    left: "0",
    right: "0",
    bottom: "0",
    backgroundColor: "#ccc",
    transition: ".4s",
    borderRadius: "24px",
  },

  streakBox: {
    marginTop: "1rem",
    padding: "0.7rem",
    background: "#fef3c7",
    borderRadius: "8px",
    fontWeight: 600,
    textAlign: "center",
  }
};