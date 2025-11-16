import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import "./css/auth.css";

export default function SignIn() {
  const nav = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin() {
    setError("");

    try {
      const res = await api.post("/login", {
        username: email,
        password: password
      });

      const success = res.data.authenticated === true;

      if (!success) {
        setError("Invalid email or password.");
        return;
      }

      // login success → proceed to dashboard
      nav("/dashboard");
    } catch (err) {
      setError("Login failed. Check backend.");
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="signin-card">
        <h2 className="card-title">Welcome Back</h2>
        <p className="muted">Sign in to continue</p>

        <div className="signin-form">
          <label className="field">
            <div className="field-label">Email</div>
            <input
              className="text-input"
              placeholder="Email"
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
            <button className="btn btn-primary" onClick={handleLogin}>
              Sign In
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => nav("/signup")}
            >
              Sign up
            </button>
          </div>

          {error && <p className="input-error">{error}</p>}

          <div className="divider">Or continue with</div>

          <div className="social-row">
            <button type="button" className="social-btn">Google</button>
            <button type="button" className="social-btn">GitHub</button>
          </div>
        </div>
      </div>
    </div>
  );
}