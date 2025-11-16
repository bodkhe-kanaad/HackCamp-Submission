import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { api } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const nav = useNavigate();
  const userId = Number(localStorage.getItem("userId"));

  const [partner, setPartner] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load pairing status on page load
  useEffect(() => {
    const loadPartner = async () => {
      try {
        const res = await api.get(`/pair/${userId}`);
        if (res.data.paired) {
          setPartner(res.data.partner_id);
        } else {
          setPartner(null);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadPartner();
  }, [userId]);

  // Pair Me button
  const handlePair = async () => {
    try {
      const res = await api.post("/pair", { user_id: userId });
      if (res.data.paired) {
        setPartner(res.data.partner_id);
      } else {
        alert("No partner available yet");
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Unpair
  const handleUnpair = async () => {
    await api.post("/unpair", { user_id: userId });
    setPartner(null);
  };

  if (loading) return <div>Loading dashboard...</div>;

  return (
    <>
      <Navbar center="Dashboard" />

      <div style={styles.container}>
        {/* Duo Status */}
        <div style={styles.card}>
          <h3>Your Study Buddy</h3>

          {partner ? (
            <>
              <p>You are paired with user #{partner}</p>
              <button style={styles.unpairBtn} onClick={handleUnpair}>
                Unpair
              </button>
            </>
          ) : (
            <>
              <p>You don't have a study buddy yet.</p>
              <button style={styles.btn} onClick={handlePair}>
                Pair Me
              </button>
            </>
          )}
        </div>

        {/* Today's Challenge */}
        <div style={styles.card}>
          <h3>Today's Challenge</h3>
          <button
            style={styles.btn}
            onClick={() => nav(`/solve/${userId}`)}
          >
            Load Today's Question
          </button>
        </div>
      </div>
    </>
  );
}

const styles = {
  container: {
    width: "90%",
    maxWidth: "600px",
    margin: "2rem auto",
    display: "flex",
    flexDirection: "column",
    gap: "20px"
  },
  card: {
    padding: "1.5rem",
    borderRadius: "10px",
    background: "#f7f7f7",
    textAlign: "center",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
  },
  btn: {
    marginTop: "1rem",
    padding: "0.75rem",
    width: "100%",
    background: "#3b82f6",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer"
  },
  unpairBtn: {
    marginTop: "1rem",
    padding: "0.75rem",
    width: "100%",
    background: "#ef4444",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer"
  }
};
