import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function Landing() {
  const nav = useNavigate();
  const isLoggedIn = Boolean(localStorage.getItem("user_id"));

  return (
    <>
      {isLoggedIn && <Navbar />}

      {/* Background gradient layer */}
      <div style={styles.background}></div>

      <div style={styles.wrapper}>
        <div style={styles.heroBox}>
          <h1 style={styles.title}>PairUp</h1>
          <p style={styles.subtitle}>Pair. Learn. Streak.</p>

          <button style={styles.cta} onClick={() => nav("/signup")}>
            Get Started →
          </button>

          {/* Feature Cards */}
          <div style={styles.features}>
            <div style={styles.featureCard}>🤝 Match with a buddy</div>
            <div style={styles.featureCard}>📘 Daily learning tasks</div>
            <div style={styles.featureCard}>🔥 Build unstoppable streaks</div>
          </div>
        </div>
      </div>
    </>
  );
}

const styles = {
  /* Soft gradient background */
  background: {
    position: "fixed",
    top: 0,
    left: 0,
    height: "100vh",
    width: "100vw",
    zIndex: -1,
    background:
      "linear-gradient(135deg, var(--accent-soft) 0%, #eef7f9 40%, var(--bg) 100%)",
  },

  wrapper: {
    width: "100%",
    maxWidth: "1000px",
    margin: "60px auto",
    padding: "0 20px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    animation: "fadeIn 0.6s ease",
  },

  heroBox: {
    width: "100%",
    maxWidth: "820px",
    padding: "60px 40px",
    borderRadius: "22px",

    background: "rgba(255,255,255,0.7)",
    backdropFilter: "blur(14px)",

    boxShadow: "0 16px 40px var(--shadow-light)",
    textAlign: "center",
    transition: "transform 0.25s ease, box-shadow 0.25s ease",
  },

  title: {
    fontSize: "3.4rem",
    fontWeight: 800,
    color: "var(--primary)",
    marginBottom: "6px",
    letterSpacing: "-0.02em",
  },

  subtitle: {
    fontSize: "1.35rem",
    color: "rgba(7,40,42,0.7)",
    marginBottom: "32px",
    fontWeight: 500,
  },

  cta: {
    padding: "14px 30px",
    background: "linear-gradient(90deg, var(--primary), var(--muted))",
    color: "#fff",
    border: "none",
    borderRadius: "14px",
    cursor: "pointer",
    fontSize: "1.1rem",
    fontWeight: 700,
    transition: "0.2s ease",
    boxShadow: "0 8px 26px rgba(0, 96, 120, 0.18)",
  },

  features: {
    marginTop: "42px",
    display: "flex",
    flexDirection: "row",
    gap: "18px",
    flexWrap: "wrap",
    justifyContent: "center",
  },

  featureCard: {
    flex: "0 1 200px",
    padding: "20px 16px",
    borderRadius: "14px",
    background: "rgba(255,255,255,0.95)",
    boxShadow: "0 6px 20px rgba(0,0,0,0.05)",
    fontWeight: 600,
    fontSize: "1.05rem",
    transition: "0.25s ease",
    cursor: "pointer",
  },
};

/* Add animation globally */
document.head.insertAdjacentHTML(
  "beforeend",
  `<style>
     @keyframes fadeIn {
       from { opacity: 0; transform: translateY(12px); }
       to { opacity: 1; transform: translateY(0); }
     }
   </style>`
);