import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../services/api";

export default function SignUp() {
  const nav = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSignUp = async () => {
    try {
      const res = await api.post("/auth/signup", {
        username,
        password
      });

      if (res.data.status === "success") {
        localStorage.setItem("userId", res.data.user_id);
        nav("/onboarding");
      } else {
        alert("Signup failed");
      }
    } catch (err) {
      console.error(err);
      alert("Signup error — check backend");
    }
  };

  return (
    <>
      <Navbar />

      <div style={styles.card}>
        <h2>Create Your Account</h2>

        <input
          placeholder="Username"
          style={styles.input}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        {/* Email isn't used by backend — keep it visible, but ignore it */}
        <input
          placeholder="Email (Not required)"
          style={styles.input}
          disabled
        />

        <input
          placeholder="Password"
          type="password"
          style={styles.input}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={styles.btn} onClick={handleSignUp}>Sign Up</button>

        <p>
          Already have an account?{" "}
          <span style={styles.link} onClick={() => nav("/signin")}>
            Sign in
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
