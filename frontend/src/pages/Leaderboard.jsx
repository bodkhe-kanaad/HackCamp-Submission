import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom"; 
import "./css/leaderboard.css";
import { useState, useEffect } from "react";
import medal from './medalImg/medal.png'; // Assuming medal.png is gold (Rank 1)
import silverMedal from './medalImg/medalSilver.png'; // Assuming medal (1).png is silver (Rank 2)
import bronzeMedal from './medalImg/medalBronze.png';
import { api } from "../services/api";
// The 'styles' object must be defined at the bottom of the file
// to be accessed globally within the file.

export default function Leaderboard() {
  const nav = useNavigate(); 
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    async function loadLeaderboard() {
      try {
        const res = await api.get("/leaderboard"); // Fetch from API
        const leaderboard = res.data;

        // Add rank as a counter
        const ranked = leaderboard.map((pair, index) => ({
          rank: index + 1,
          ...pair, // contains names, pair_id, streak
        }));

        setUsers(ranked);
      } catch (err) {
        console.error("Failed to load leaderboard", err);
      } finally {
        setLoading(false);
      }
    }

    loadLeaderboard();
  }, []);
  // We'll simulate user data with random generation here


  // Function to determine medal class for the rank cell
  const getRankClass = (rank) => {
    if (rank === 1) return "medal-gold";
    if (rank === 2) return "medal-silver";
    if (rank === 3) return "medal-bronze";
    return "";
  };

  // Function to determine if a badge should be shown
  const getBadge = (user) => {
    if (user.problems > 40) {
      return <span className="badge badge-solver">Problem Solver</span>;
    }
    if (user.points > 450) {
        return <span className="badge badge-pro">High Scorer</span>;
    }
    return null;
  };

  const getMedalImageSrc = (rank) => {
    if (rank === 1) return medal;
    if (rank === 2) return silverMedal;
    if (rank === 3) return bronzeMedal;
    return null; 
  };

  return (
    <>
      <Navbar />

      {/* The external CSS file needs to define .leaderboard-container */}
      <div className="leaderboard-container"> 
        <h2>🏆 Leaderboard</h2>

        {/* The external CSS file needs to define .leaderboard-table */}
        <table className="leaderboard-table" style={styles.table}> 
          <thead>
             {/* This section is now correctly rendered */}
             <tr> 
              <th style={styles.th}>Rank</th>
              <th>Name</th>
              <th>Streak</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.rank} className={user.rank <= 3 ? "top-rank-row" : ""}>
                
                {/* 🥇 IMAGE MEDAL IMPLEMENTATION 🥈 */}
                {/* We are no longer using the CSS podium block, but a container for flex display */}
                <td>
                  {user.rank <= 3 ? (
                    <div className="medal-display"> 
                      <img 
                        src={getMedalImageSrc(user.rank)} 
                        alt={`${user.rank} Place Medal`} 
                        className="medal-icon"
                      />
                      <span className="rank-number">{user.rank}</span>
                    </div>
                  ) : (
                    user.rank
                  )}
                </td>
                {/* 🥉 END IMAGE MEDAL IMPLEMENTATION 🥉 */}

                {/* NOTE: You also removed the badge display logic from the Name cell */}
                <td>
                  {user.names}
                </td>

                <td>{user.streak}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

const styles = {
  table: {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: "1.5rem"
    // Other styles from the previous steps are handled by the external CSS
  },
  th: {
    textAlign: "center", 
  }
};