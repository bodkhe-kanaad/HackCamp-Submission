import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import "./css/landing.css";

export default function Landing() {
  const nav = useNavigate();
  const isLoggedIn = Boolean(localStorage.getItem("user_id"));

  return (
    <>
      {isLoggedIn && <Navbar />}

      <div className="landing-wrapper">
        <div className="landing-hero">
          <h1>Find Your Coding Study Buddy</h1>
          <p>Pair with real students, solve problems daily, and stay accountable.</p>

          <button className="landing-cta" onClick={() => nav("/signup")}>
            Get Started
          </button>

          <div className="landing-how">
            <div className="landing-card">Match with a buddy</div>
            <div className="landing-card">Solve daily problems</div>
            <div className="landing-card">Win together</div>
          </div>
        </div>

        {/* <aside className="landing-side">
          <h3 className="lead-title">Why PairUp?</h3>
          <p className="lead">Daily practice • Real peers • Track your streaks</p>
        </aside> */}
      </div>
    </>
  );
}

