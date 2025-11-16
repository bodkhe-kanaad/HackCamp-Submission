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

  useEffect(() => {
    async function load() {
      const id = localStorage.getItem("user_id");
      if (!id) {
        setError("No user session found — please log in again.");
        return;
      }

      try {
        const userRes = await api.get(`/user/${id}`);
        setUser(userRes.data);
      } catch {
        setError("Failed to load user profile.");
      }

      try {
        const pairRes = await api.get(`/pair/status/${id}`);
        if (pairRes.data.pair_id !== null) {
          setPairBasic(pairRes.data);

          const mate = await api.get(`/pair/mate/${id}`);
          setPairFull(mate.data);
        }
      } catch {}

      setLoadingUser(false);
    }

    load();
  }, []);

  async function handlePair() {
    setLoadingPair(true);

    const id = localStorage.getItem("user_id");

    try {
      const res = await api.post("/pair", { user_id: id });
      setPairBasic(res.data);

      const mate = await api.get(`/pair/mate/${id}`);
      setPairFull(mate.data);
    } catch {
      setError("Pairing failed, try again.");
    }

    setLoadingPair(false);
  }

  return (
    <>
      <Navbar />

      {/* Background gradient */}
      <div style={styles.bg}></div>

      <div style={styles.container}>
        <h1 style={styles.pageTitle}>Your Dashboard</h1>

        {/* Error message */}
        {error && <p style={styles.error}>{error}</p>}

        {/* Loading skeleton */}
        {loadingUser && <div style={styles.skeleton}></div>}

        {/* Profile Card */}
        {!loadingUser && user && (
          <div style={styles.profileCard}>
            <h2 style={styles.sectionTitle}>👋 Welcome, {user.username}</h2>

            <div style={styles.profileRow}>
              <span style={styles.label}>Courses</span>
              <span>{user.courses.join(", ")}</span>
            </div>

            <div style={styles.profileRow}>
              <span style={styles.label}>Interests</span>
              <span>{user.interests.join(", ")}</span>
            </div>

            {!pairBasic && (
              <button
                style={styles.primary}
                onClick={handlePair}
                disabled={loadingPair}
              >
                {loadingPair ? "Finding best match..." : "Find Study Partner"}
              </button>
            )}
          </div>
        )}

        {/* Partner Card */}
        {pairFull && (
          <div style={styles.partnerCard}>
            <h2 style={styles.sectionTitle}>🤝 You’re Paired!</h2>

            <div style={styles.partnerInfo}>
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

                <p style={styles.streak}>
                  🔥 Streak: <strong>{pairFull.streak || 0}</strong> days
                </p>
              </div>
            </div>

            {/* AI Mode Toggle */}
            <div style={styles.toggleContainer}>
              <span style={styles.label}>AI Mode</span>
              <Toggle
                value={pairFull.ai_mode}
                onChange={async (v) => {
                  try {
                    await api.post("/pair/toggle-mode", {
                      user_id: user.user_id,
                      ai_mode: v,
                    });
                    setPairFull({ ...pairFull, ai_mode: v });
                  } catch {
                    alert("Failed to toggle.");
                  }
                }}
              />
            </div>
          </div>
        )}

        {/* Today's Task CTA */}
        {pairBasic && (
          <div style={styles.taskCard}>
            <h3 style={styles.taskTitle}>📘 Today’s Daily Challenge</h3>
            <p style={styles.taskDesc}>
              Solve one problem with your partner or using AI mode.
            </p>

            <button
              style={styles.startButton}
              onClick={() => nav(`/solve/${user.user_id}`)}
            >
              Start Task →
            </button>
          </div>
        )}
      </div>
    </>
  );
}

/* -------------------------------------------
   Toggle Component — iOS style
-------------------------------------------- */
function Toggle({ value, onChange }) {
  return (
    <div
      onClick={() => onChange(!value)}
      style={{
        width: "48px",
        height: "26px",
        borderRadius: "24px",
        background: value ? "#34d399" : "#d1d5db",
        position: "relative",
        cursor: "pointer",
        transition: "0.2s",
        boxShadow: "inset 0 0 4px rgba(0,0,0,0.15)",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "3px",
          left: value ? "24px" : "3px",
          width: "20px",
          height: "20px",
          background: "#fff",
          borderRadius: "50%",
          transition: "0.2s",
          boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
        }}
      />
    </div>
  );
}

/* -------------------------------------------
   Styles
-------------------------------------------- */
const styles = {
  bg: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    background:
      "linear-gradient(135deg, #eef2ff 0%, #fdf2f8 50%, #ecfdf5 100%)",
    zIndex: -1,
  },

  container: {
    width: "90%",
    maxWidth: "700px",
    margin: "2rem auto",
  },

  pageTitle: {
    fontSize: "2rem",
    fontWeight: 800,
    textAlign: "center",
    marginBottom: "1.5rem",
  },

  error: {
    color: "red",
    textAlign: "center",
    marginTop: "1rem",
  },

  skeleton: {
    height: "180px",
    background: "#e5e7eb",
    borderRadius: "14px",
    animation: "pulse 1.5s infinite",
  },

  profileCard: {
    background: "#fff",
    padding: "2rem",
    borderRadius: "14px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
    marginBottom: "1.5rem",
  },

  partnerCard: {
    background: "#ffffff",
    padding: "2rem",
    borderRadius: "14px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
    marginBottom: "1.5rem",
  },

  sectionTitle: {
    fontSize: "1.4rem",
    fontWeight: 700,
    marginBottom: "1.2rem",
  },

  profileRow: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "0.6rem",
  },

  label: {
    fontWeight: 600,
    opacity: 0.8,
  },

  primary: {
    marginTop: "1rem",
    width: "100%",
    padding: "0.9rem",
    background: "#3b82f6",
    color: "#fff",
    border: "none",
    borderRadius: "12px",
    cursor: "pointer",
    fontWeight: 600,
    fontSize: "1rem",
  },

  partnerInfo: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
    marginBottom: "1rem",
  },

  avatar: {
    width: "55px",
    height: "55px",
    background: "#3b82f6",
    color: "#fff",
    borderRadius: "50%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontSize: "1.5rem",
    fontWeight: 700,
  },

  partnerName: {
    margin: 0,
    fontSize: "1.3rem",
    fontWeight: 700,
  },

  partnerLine: {
    marginTop: "4px",
    opacity: 0.8,
  },

  streak: {
    marginTop: "0.5rem",
    fontSize: "1.1rem",
  },

  toggleContainer: {
    marginTop: "1.4rem",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },

  taskCard: {
    background: "#f0f9ff",
    padding: "1.5rem",
    borderRadius: "14px",
    textAlign: "center",
    boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
  },

  taskTitle: {
    fontSize: "1.3rem",
    fontWeight: 700,
  },

  taskDesc: {
    marginTop: "0.5rem",
    opacity: 0.8,
    fontSize: "0.95rem",
  },

  startButton: {
    marginTop: "1rem",
    padding: "0.8rem 1.4rem",
    background: "#10b981",
    color: "#fff",
    borderRadius: "10px",
    border: "none",
    cursor: "pointer",
    fontWeight: 600,
  },
};