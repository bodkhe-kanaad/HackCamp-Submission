import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [match, setMatch] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);
  const [loadingPair, setLoadingPair] = useState(false);
  const [error, setError] = useState("");
  const [pairError, setPairError] = useState("");

  useEffect(() => {
    async function fetchUser() {
      setLoadingUser(true);
      setError("");

      const id = localStorage.getItem("user_id");

      if (!id) {
        setError("No user ID found. Please sign in again.");
        setLoadingUser(false);
        return;
      }

      try {
        const res = await api.get(`/user/${id}`);
        setUser(res.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load profile. Backend might be offline.");
      } finally {
        setLoadingUser(false);
      }
    }

    fetchUser();
  }, []);

  async function handlePair() {
    setLoadingPair(true);
    setPairError("");

    const id = localStorage.getItem("user_id");

    try {
      const res = await api.post("/pair", { user_id: id });
      setMatch(res.data);
    } catch (err) {
      console.error(err);
      setPairError("Pairing failed. Try again later.");
    } finally {
      setLoadingPair(false);
    }
  }

  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <h2>Your Dashboard</h2>

        {loadingUser ? (
          <p>Loading profile...</p>
        ) : error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : (
          <div style={styles.card}>
            <h3>Hello, {user.username} 👋</h3>

            <p>
              <strong>Courses:</strong>{" "}
              {Array.isArray(user.courses) ? user.courses.join(", ") : "None"}
            </p>

            <p>
              <strong>Interests:</strong>{" "}
              {Array.isArray(user.interests) ? user.interests.join(", ") : "None"}
            </p>

            <button
              style={styles.btn}
              onClick={handlePair}
              disabled={loadingPair}
            >
              {loadingPair ? "Pairing..." : "Pair Me"}
            </button>

            {pairError && <p style={{ color: "red" }}>{pairError}</p>}
          </div>
        )}

        {match && (
          <div style={styles.matchCard}>
            <h3>🎉 You’ve been paired!</h3>
            <p><strong>Partner:</strong> {match.partner_username}</p>
            <p><strong>Courses:</strong> {match.partner_courses.join(", ")}</p>
            <p><strong>Interests:</strong> {match.partner_interests.join(", ")}</p>
          </div>
        )}
      </div>
    </>
  );
}

const styles = {
  container: { width: "70%", margin: "2rem auto", textAlign: "center" },

  card: {
    background: "#f5f5f5",
    padding: "1.5rem",
    borderRadius: "12px",
    marginBottom: "1.5rem"
  },

  btn: {
    background: "#3b82f6",
    color: "#fff",
    padding: "0.75rem 1.25rem",
    borderRadius: "10px",
    border: "none",
    cursor: "pointer",
    marginTop: "1rem"
  },

  matchCard: {
    background: "#d1fae5",
    padding: "1.5rem",
    borderRadius: "12px",
    marginTop: "2rem"
  }
};
