import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Dashboard() {
  const nav = useNavigate();

  const [user, setUser] = useState(null);
  const [pairBasic, setPairBasic] = useState(null);
  const [pairFull, setPairFull] = useState(null); // includes ai_mode now
  const [loadingUser, setLoadingUser] = useState(true);
  const [loadingPair, setLoadingPair] = useState(false);
  const [error, setError] = useState("");
  const [pairError, setPairError] = useState("");
  const [togglingMode, setTogglingMode] = useState(false);

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

          // Fetch full pairmate info, which now includes ai_mode
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

      // fetch partner details now (includes ai_mode)
      const mate = await api.get(`/pair/mate/${id}`);
      setPairFull(mate.data);
    } catch (err) {
      setPairError("Pairing failed.");
    }

    setLoadingPair(false);
  }

  // 🔥 NEW: Toggle AI mode
  async function toggleAIMode(e) {
    const newValue = e.target.checked;
    const user_id = localStorage.getItem("user_id");

    if (!pairFull) return;

    setTogglingMode(true);

    try {
      await api.post("/pair/toggle-mode", {
        user_id: user_id,
        ai_mode: newValue,
      });

      // Update UI
      setPairFull((prev) => ({
        ...prev,
        ai_mode: newValue,
      }));
    } catch (err) {
      console.error("AI toggle failed:", err);
    }

    setTogglingMode(false);
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

            {/* If paired → show Today's Task button */}
            {pairBasic && (
              <>
                <button
                  style={styles.taskBtn}
                  onClick={() => nav(`/solve/${user.user_id}`)}
                >
                  Today's Task
                </button>

                {/* 🔥 AI MODE TOGGLE */}
                {pairFull && (
                  <div style={{ marginTop: "1rem" }}>
                    <label style={{ fontSize: "1rem", cursor: "pointer" }}>
                      <input
                        type="checkbox"
                        checked={pairFull.ai_mode === true}
                        onChange={toggleAIMode}
                        disabled={togglingMode}
                        style={{ marginRight: "0.5rem" }}
                      />
                      AI Mode
                    </label>
                  </div>
                )}
              </>
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

            <p>
              <strong>Similarity Score:</strong> {pairFull.similarity_score}
            </p>

            <p>
              <strong>AI Mode:</strong>{" "}
              {pairFull.ai_mode ? "ON 🤖" : "OFF 👤"}
            </p>
          </div>
        )}
      </div>
    </>
  );
}

const styles = {
  container: { width: "70%", margin: "2rem auto", textAlign: "center" },
  card: { background: "#f5f5f5", padding: "1.5rem", borderRadius: "12px" },
  btn: {
    marginTop: "1rem",
    padding: "0.75rem 1.25rem",
    background: "#3b82f6",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
  },
  taskBtn: {
    marginTop: "1rem",
    padding: "0.75rem 1.25rem",
    background: "#10b981",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
  },
  matchCard: {
    background: "#d1fae5",
    padding: "1.5rem",
    borderRadius: "12px",
    marginTop: "2rem",
  },
};
