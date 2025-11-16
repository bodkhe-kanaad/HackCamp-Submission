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

  useEffect(() => {
    async function loadEverything() {
      const id = localStorage.getItem("user_id");
      if (!id) {
        setError("No user ID found. Please log in again.");
        return;
      }

      // Load profile
      try {
        const res = await api.get(`/user/${id}`);
        setUser(res.data);
      } catch {
        setError("Failed to load profile.");
      }

      // Load pair status
      try {
        const res = await api.get(`/pair/status/${id}`);

        if (res.data.pair_id !== null) {
          setPairBasic(res.data);

          // Now fetch full partner info
          const mate = await api.get(`/pair/mate/${id}`);
          setPairFull(mate.data);
        }
      } catch (err) {
        console.error("Pair status error:", err);
      }

      setLoadingUser(false);
    }

    loadEverything();
  }, []);

  async function handlePair() {
    setPairError("");
    setLoadingPair(true);

    const id = localStorage.getItem("user_id");

    try {
      const res = await api.post("/pair", { user_id: id });
      setPairBasic(res.data);

      // fetch partner details now
      const mate = await api.get(`/pair/mate/${id}`);
      setPairFull(mate.data);
    } catch (err) {
      setPairError("Pairing failed.");
    }

    setLoadingPair(false);
  }

  return (
    <>
      <Navbar />
      <div style={styles.container}>
        <h2>Your Dashboard</h2>

        {loadingUser ? (
          <p>Loading...</p>
        ) : error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : (
          <div style={styles.card}>
            <h3>Hello, {user.username} 👋</h3>

            <p>
              <strong>Courses:</strong> {user.courses.join(", ")}
            </p>
            <p>
              <strong>Interests:</strong> {user.interests.join(", ")}
            </p>

            {/* If unpaired → show Pair Me */}
            {!pairBasic && (
              <button
                style={styles.btn}
                onClick={handlePair}
                disabled={loadingPair}
              >
                {loadingPair ? "Pairing..." : "Pair Me"}
              </button>
            )}

            {/* If paired → AI toggle */}
            {pairBasic && pairFull && (
              <div style={{ marginTop: "1.5rem" }}>
                <label style={{ fontWeight: "bold" }}>
                  AI Mode:
                  <input
                    type="checkbox"
                    checked={pairFull.ai_mode === true}
                    onChange={async (e) => {
                      const newMode = e.target.checked;
                      try {
                        await api.post("/pair/toggle-mode", {
                          user_id: user.user_id,
                          ai_mode: newMode
                        });

                        // update UI immediately
                        setPairFull({
                          ...pairFull,
                          ai_mode: newMode
                        });
                      } catch (err) {
                        console.error(err);
                        alert("Failed to toggle AI mode.");
                      }
                    }}
                    style={{ marginLeft: "0.75rem" }}
                  />
                </label>
              </div>
            )}

            {/* If paired → show task button */}
            {pairBasic && (
              <button
                style={styles.taskBtn}
                onClick={() => nav(`/solve/${user.user_id}`)}
              >
                Today's Task
              </button>
            )}

            {pairError && <p style={{ color: "red" }}>{pairError}</p>}
          </div>
        )}

        {/* SHOW PARTNER INFO */}
        {pairFull && (
          <div style={styles.matchCard}>
            <h3>🎉 You’re paired!</h3>

            <p>
              <strong>Partner:</strong> {pairFull.partner.username}
            </p>

            <p>
              <strong>Courses:</strong>{" "}
              {pairFull.partner.courses.join(", ")}
            </p>

            <p>
              <strong>Interests:</strong>{" "}
              {pairFull.partner.interests.join(", ")}
            </p>
          </div>
        )}
      </div>
    </>
  );
}

const styles = {
<<<<<<< HEAD
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
=======
  container: { width: "70%", margin: "2rem auto", textAlign: "center" },
  card: { background: "#f5f5f5", padding: "1.5rem", borderRadius: "12px" },
  btn: {
    marginTop: "1rem",
    padding: "0.75rem 1.25rem",
>>>>>>> 403514e (Comits)
    background: "#3b82f6",
    color: "#fff",
    border: "none",
<<<<<<< HEAD
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
=======
>>>>>>> 403514e (Comits)
    borderRadius: "10px",
    cursor: "pointer"
  },
  taskBtn: {
    marginTop: "1rem",
    padding: "0.75rem 1.25rem",
    background: "#10b981",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer"
  },
  matchCard: {
    background: "#d1fae5",
    padding: "1.5rem",
    borderRadius: "12px",
    marginTop: "2rem"
  }
};