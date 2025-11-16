import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

export default function Onboarding() {
  const nav = useNavigate();
  const courses = ["CPSC 110", "CPSC 121", "CPSC 210", "CPSC 213", "CPSC 221", "CPSC 320"];

  return (
    <>
      <Navbar />

      <div style={styles.wrapper}>
        <h2>Complete Your Profile</h2>

        <input placeholder="Name" style={styles.input} />

        <h3>Courses</h3>
        {courses.map(c => (
          <label key={c} style={styles.label}>
            <input type="checkbox" /> {c}
          </label>
        ))}

        <h3>Goal</h3>
        <label><input type="radio" name="goal" /> Interview Prep</label>
        <label><input type="radio" name="goal" /> Pass Classes</label>
        <label><input type="radio" name="goal" /> Get Better</label>

        <button style={styles.btn} onClick={() => nav("/dashboard")}>
          Complete Profile
        </button>
      </div>
    </>
  );
}

const styles = {
  wrapper: { width: "400px", margin: "2rem auto" },
  input: {
    width: "100%",
    padding: "0.75rem",
    marginBottom: "1rem",
    border: "1px solid #ccc",
    borderRadius: "8px"
  },
  label: { display: "block", marginBottom: "0.35rem" },
  btn: {
    marginTop: "1rem",
    padding: "0.75rem",
    background: "#3b82f6",
    border: "none",
    color: "#fff",
    width: "100%",
    borderRadius: "8px"
  }
};
