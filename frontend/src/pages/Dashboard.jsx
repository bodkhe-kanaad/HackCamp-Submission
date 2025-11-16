import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [match, setMatch] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pairError, setPairError] = useState("");

  useEffect(() => {
    async function fetchUser() {
      const id = localStorage.getItem("user_id");
      if (!id) return;

      try {
        const res = await api.get(`/user/${id}`);
        setUser(res.data);
      } catch (err) {
        console.error(err);
      }
    }

    fetchUser();
  }, []);

  async function handlePair() {
    setLoading(true);
    setPairError("");

    const id = localStorage.getItem("user_id");

    try {
      const res = await api.post("/pair", { user_id: id });
      setMatch(res.data); // backend returns match info
    } catch (err) {
      console.error(err);
      setPairError("Pairing failed. Try again later.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <h2>Your Dashboard</h2>

        {!user ? (
          <p>Loading profile...</p>
        ) : (
          <div style={styles.card}>
            <h3>Hello, {user.username} 👋</h3>

            <p><strong>Courses:</strong> {user.courses.join(", ")}</p>
            <p><strong>Interests:</strong> {user.interests.join(", ")}</p>

            <button style={styles.btn} onClick={handlePair} disabled={loading}>
              {loading ? "Pairing..." : "Pair Me"}
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
