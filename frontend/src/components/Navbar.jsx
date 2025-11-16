import { Link } from "react-router-dom";

export default function Navbar({ center }) {
  return (
    <nav style={styles.nav}>
      <div style={styles.left}>
        <Link to="/" style={styles.logo}>DuoLearn</Link>
      </div>

      <div style={styles.center}>{center}</div>

      <div style={styles.right}>
        <Link to="/dashboard" style={styles.link}>Dashboard</Link>
        <Link to="/leaderboard" style={styles.link}>Leaderboard</Link>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    padding: "1rem 2rem",
    borderBottom: "1px solid #ddd",
    alignItems: "center"
  },
  left: { fontWeight: "bold", fontSize: "1.25rem" },
  center: {},
  right: { display: "flex", gap: "1rem" },
  link: { textDecoration: "none", color: "#333" },
  logo: { textDecoration: "none", color: "#333", fontWeight: "bold" }
};
