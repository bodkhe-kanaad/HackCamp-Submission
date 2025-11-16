import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function SignIn() {
  const nav = useNavigate();

  return (
    <>
      <Navbar />
      <div style={styles.card}>
        <h2>Welcome Back</h2>

        <input placeholder="Email" style={styles.input} />
        <input placeholder="Password" type="password" style={styles.input} />

        <button style={styles.btn}>Sign In</button>

        <p>
          Don't have an account?{" "}
          <span style={styles.link} onClick={() => nav("/signup")}>
            Sign up
          </span>
        </p>
      </div>
    </>
  );
}

const styles = {
    card: {
      width: "350px",
      margin: "3rem auto",
      padding: "2rem",
      borderRadius: "12px",
      background: "#f7f7f7",
      textAlign: "center"
    },
    input: {
      width: "100%",
      padding: "0.75rem",
      margin: "0.5rem 0",
      borderRadius: "8px",
      border: "1px solid #ccc"
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
    link: { color: "#3b82f6", cursor: "pointer" }
  };