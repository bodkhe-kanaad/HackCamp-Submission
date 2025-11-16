import { useNavigate } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing">
      <h1>DuoLearn</h1>
      <button onClick={() => navigate("/matching")}>
        Find Study Buddy
      </button>
    </div>
  );
}
