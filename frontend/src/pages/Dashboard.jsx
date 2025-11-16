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
    async function load() {
      const id = localStorage.getItem("user_id");
      if (!id) {
        setError("No user ID found — please sign in again.");
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
      setPairError("Pairing failed, try again.");
    }

    setLoadingPair(false);
  }

  return (
    <>
      <Navbar />

      <div style={styles.container}>

        <h2 style={styles.heading}>Dashboard</h2>

        {loadingUser && <div style={styles.skeletonCard}></div>}

        {error && <p style={styles.error}>{error}</p>}

        {!loadingUser && !error && user && (
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>Welcome, {user.username} 👋</h3>

            <div style={styles.row}>
              <div style={styles.label}>Courses:</div>
              <div>{user.courses.join(", ")}</div>
            </div>

            <div style={styles.row}>
              <div style={styles.label}>Interests:</div>
              <div>{user.interests.join(", ")}</div>
            </div>

            {!pairBasic && (
              <button
                style={styles.primaryButton}
                onClick={handlePair}
                disabled={loadingPair}
              >
                {loadingPair ? "Pairing..." : "Find Me a Study Partner"}
              </button>
            )}

            {pairBasic && pairFull && (
              <div style={styles.toggleRow}>
                <span style={styles.label}>AI Mode:</span>
                
                <label style={styles.switch}>
                  <input
                    type="checkbox"
                    checked={pairFull.ai_mode === true}
                    onChange={async (e) => {
                      try {
                        const newMode = e.target.checked;
                        await api.post("/pair/toggle-mode", {
                          user_id: user.user_id,
                          ai_mode: newMode,
                        });

                        setPairFull({ ...pairFull, ai_mode: newMode });
                      } catch {
                        alert("Failed to toggle AI mode.");
                      }
                    }}
                  />
                  <span className="slider" style={styles.slider}></span>
                </label>
              </div>
            )}

            {pairBasic && (
              <button
                style={styles.accentButton}
                onClick={() => nav(`/solve/${user.user_id}`)}
              >
                Start Today’s Task
              </button>
            )}

            {pairError && <p style={styles.error}>{pairError}</p>}
          </div>
        )}

        {pairFull && (
          <div style={styles.partnerCard}>
            <h3 style={styles.partnerTitle}>🎉 You’re Paired!</h3>

            <div style={styles.row}>
              <div style={styles.label}>Partner:</div>
              <div>{pairFull.partner.username}</div>
            </div>

            <div style={styles.row}>
              <div style={styles.label}>Courses:</div>
              <div>{pairFull.partner.courses.join(", ")}</div>
            </div>

            <div style={styles.row}>
              <div style={styles.label}>Interests:</div>
              <div>{pairFull.partner.interests.join(", ")}</div>
            </div>

            {/* UNCOMMENT THIS IF YOU WANT TO SHOW STREAK */}
            {/* <div style={styles.streakBox}>
              🔥 Streak: {pairFull.streak || 0} days
            </div> */}
          </div>
        )}
      </div>
    </>
  );
}

const styles = {
  container: {
    width: "60%",
    margin: "2rem auto",
    textAlign: "center",
  },

  heading: {
    fontSize: "1.9rem",
    fontWeight: 700,
    marginBottom: "1rem",
  },

  error: {
    color: "red",
    marginTop: "1rem",
  },

  skeletonCard: {
    height: "200px",
    background: "#e3e3e3",
    borderRadius: "12px",
    animation: "pulse 1.4s infinite",
  },

  card: {
    background: "#ffffff",
    padding: "1.5rem",
    borderRadius: "14px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
    textAlign: "left",
  },

  cardTitle: {
    fontSize: "1.4rem",
    fontWeight: 600,
    marginBottom: "1rem",
  },

  row: {
    display: "flex",
    marginBottom: "0.6rem",
    gap: "0.5rem",
  },

  label: {
    fontWeight: 600,
    minWidth: "100px",
  },

  toggleRow: {
    marginTop: "1rem",
    display: "flex",
    alignItems: "center",
    gap: "1rem",
  },

  primaryButton: {
    marginTop: "1.5rem",
    width: "100%",
    padding: "0.8rem",
    background: "#3b82f6",
    color: "#fff",
    borderRadius: "10px",
    border: "none",
    cursor: "pointer",
    fontWeight: 600,
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