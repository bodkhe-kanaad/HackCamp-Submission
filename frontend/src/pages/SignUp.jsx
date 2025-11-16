import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../services/api";
import "./css/auth.css";

export default function SignUp() {
  const nav = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [courses, setCourses] = useState([]);
  const [interests, setInterests] = useState([]);
  const [error, setError] = useState("");

  const COURSE_OPTIONS = [
    "CPSC 110", "CPSC 210", "CPSC 310",
    "CPSC 221", "CPSC 320",
    "MATH 100", "MATH 101",
    "CHEM 121", "CHEM 123",
    "BIOL 111", "BIOL 121"
  ];

  const INTEREST_OPTIONS = [
    "gaming", "sports", "coding", "hiking", "partying"
  ];

  function toggleSelect(option, list, setter) {
    if (list.includes(option)) {
      setter(list.filter(x => x !== option));
    } else {
      setter([...list, option]);
    }
  }

  async function handleSignup() {
    try {
      const res = await api.post("/signup", {
        username,
        password,
        courses,
        interests
      });

      if (!res.data.success) {
        setError(res.data.message || "Signup failed");
        return;
      }

      // Store user_id and redirect
      localStorage.setItem("user_id", res.data.user_id);
      nav("/dashboard");

    } catch (e) {
      setError("Signup failed. Check backend.");
    }
  }

  return (
    <>
      <Navbar />
      <div style={styles.card}>
        <h2>Create Account</h2>

        <input
          placeholder="Email"
          style={styles.input}
          value={username}
          onChange={e => setUsername(e.target.value)}
        />

        <input
          placeholder="Password"
          type="password"
          style={styles.input}
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        <div style={styles.section}>
          <h4>Select Courses</h4>
          <div style={styles.multiSelect}>
            {COURSE_OPTIONS.map(c => (
              <div
                key={c}
                style={{
                  ...styles.option,
                  background: courses.includes(c) ? "#3b82f6" : "#eee",
                  color: courses.includes(c) ? "white" : "black"
                }}
                onClick={() => toggleSelect(c, courses, setCourses)}
              >
                {c}
              </div>
            ))}
          </div>
        </div>

        <div style={styles.section}>
          <h4>Select Interests</h4>
          <div style={styles.multiSelect}>
            {INTEREST_OPTIONS.map(i => (
              <div
                key={i}
                style={{
                  ...styles.option,
                  background: interests.includes(i) ? "#3b82f6" : "#eee",
                  color: interests.includes(i) ? "white" : "black"
                }}
                onClick={() => toggleSelect(i, interests, setInterests)}
              >
                {i}
              </div>
            ))}
          </div>
        </div>

        <button style={styles.btn} onClick={handleSignup}>
          Sign Up
        </button>

        {error && <p style={{ color: "red" }}>{error}</p>}

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
  // 1. CARD: Main Container (Reducing padding and margin)
  card: {
    width: "90%",
    maxWidth: "300px", // ⬅️ FURTHER REDUCED MAX WIDTH (from 340px to 300px)
    
    // Minimal vertical margin, minimal padding
    margin: "20px auto", // Reduced top margin
    padding: "15px",    // ⬅️ MINIMAL PADDING (from 20px to 15px)
    
    borderRadius: "12px",
    background: "#fafafa",
    textAlign: "center"
  },
  
  // 2. INPUTS: Reducing vertical size
  input: {
    width: "100%",
    padding: "0.5rem",
    margin: "0.2rem 0",
    borderRadius: "8px",
    border: "1px solid #FFD4D1",
    boxSizing: "border-box", 

    // 🌟 THE FIX: Explicitly setting the background to white and text to black
    background: "white", 
    color: "black",
  },
  
  // 3. SECTIONS: Reducing space between content blocks
  section: { 
    textAlign: "left", 
    marginTop: "0.8rem" // ⬅️ REDUCED TOP MARGIN (from 1rem)
  },
  
  // 4. MULTI-SELECT TAGS: Tightening the space around tags
  multiSelect: {
    display: "flex",
    flexWrap: "wrap",
    gap: "4px",        // ⬅️ MINIMAL GAP
    marginTop: "4px"   // ⬅️ MINIMAL TOP MARGIN
  },
  
  // 5. TAG OPTIONS: Making individual tags smaller
  option: {
    padding: "3px 6px", // ⬅️ MINIMAL PADDING
    borderRadius: "6px",
    cursor: "pointer",
    border: "1px solid #ccc",
    fontSize: "0.8rem" // ⬅️ SMALLER FONT SIZE
  },

  // 6. BUTTON: Reducing button margin
  btn: {
    marginTop: "0.8rem", // ⬅️ REDUCED TOP MARGIN
    padding: "0.75rem",
    width: "100%",
    background: "#3b82f6",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer"
  },
  
  // 7. H2 (Create Account): Ensuring minimal top margin
  // (You don't have an H2 style, but if you did, you would target it)
  // Since it's directly inside the card, its margin is controlled by browser defaults.
  // We'll trust the reduced card padding is enough, but if H2 still has a large margin:
  // Add an inline style to the H2 tag in your JSX:
  // <h2 style={{marginTop: 0, marginBottom: '20px'}}>Create Account</h2>
};