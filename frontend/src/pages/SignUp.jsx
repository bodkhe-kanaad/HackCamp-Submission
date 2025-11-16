import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import "./css/auth.css";

export default function SignUp() {
  const nav = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSignup() {
    setError("");
    try {
      await api.post("/api/auth/register", {
        username,
        email,
        password,
      });

      // success
      nav("/signin");
    } catch (err) {
      console.error(err);
      setError("Signup failed. Check backend.");
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="signup-card">
        <h2 className="card-title">Create Your Account</h2>
        <p className="muted">Sign up to get started</p>

        <div className="signup-form">
          <label className="field">
            <div className="field-label">Username</div>
            <input
              className="text-input"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </label>

          <label className="field">
            <div className="field-label">Email</div>
            <input
              className="text-input"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>

          <label className="field">
            <div className="field-label">Password</div>
            <input
              className="text-input"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>

          <div className="card-actions">
            <button className="btn btn-primary" onClick={handleSignup}>
              Sign Up
            </button>
            <button className="btn btn-secondary" onClick={() => nav("/signin")}>
              Sign in
            </button>
          </div>

          {error && <p className="input-error">{error}</p>}
        </div>
      </div>
    </div>
  );
}
