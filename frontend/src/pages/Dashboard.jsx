import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { api } from "../services/api";
import { useNavigate } from "react-router-dom";
import "./css/dashboard.css";

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
    try {
      await api.post("/unpair", { user_id: userId });
    } catch (err) {
      console.error(err);
    } finally {
      setPartner(null);
    }
  };

  if (loading) return <div className="dash-loading">Loading dashboard...</div>;

  return (
    <>
      <Navbar center="Dashboard" />

      <main className="dash-root">
        <aside className="dash-hero">
          <h1 className="dash-hero-title">Welcome to PairUp</h1>
          <p className="dash-hero-sub">Pair. Learn. Streak.</p>
        </aside>

        <section className="dash-panel">
          <div className="card duo-card">
            <h3 className="card-title">Your Study Buddy</h3>

            {partner ? (
              <div className="partner-wrap">
                <div className="partner-info">
                  <div className="avatar">{String(partner)[0]}</div>
                  <div>
                    <div className="partner-name">User #{partner}</div>
                    <div className="partner-meta">Ready to code together</div>
                  </div>
                </div>

                <div className="card-actions">
                  <button className="btn btn-unpair" onClick={handleUnpair}>
                    Unpair
                  </button>
                  <button
                    className="btn btn-chat"
                    onClick={() => nav(`/solve/${partner}`)}
                  >
                    View Partner's Problem
                  </button>
                </div>
              </div>
            ) : (
              <div className="no-partner">
                <p className="muted">You don't have a study buddy yet.</p>
                <button className="btn btn-primary" onClick={handlePair}>
                  Pair Me
                </button>
              </div>
            )}
          </div>

          <div className="card challenge-card">
            <h3 className="card-title">Today's Challenge</h3>
            <p className="muted">A curated problem to practice with your buddy.</p>
            <div className="card-actions">
              <button
                className="btn btn-gradient"
                onClick={() => nav(`/solve/${userId}`)}
              >
                Load Today's Question
              </button>
            </div>
          </div>
        </section>
      </main>
    </>
  );
}

