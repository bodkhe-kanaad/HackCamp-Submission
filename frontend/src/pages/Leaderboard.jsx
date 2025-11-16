import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom"; 
import "./css/leaderboard.css";

import medal from "./medalImg/medal.png"; 
import silverMedal from "./medalImg/medalSilver.png";
import bronzeMedal from "./medalImg/medalBronze.png";

export default function Leaderboard() {
  const nav = useNavigate();

  // Temporary mock data
  const users = [...Array(20)].map((_, i) => ({
    rank: i + 1,
    name: `User ${i + 1}`,
    points: Math.floor(Math.random() * 500),
    problems: Math.floor(Math.random() * 50),
  }));

  const getMedalSrc = (rank) => {
    if (rank === 1) return medal;
    if (rank === 2) return silverMedal;
    if (rank === 3) return bronzeMedal;
    return null;
  };

  return (
    <>
      <Navbar />

      {/* Gradient background */}
      <div className="leaderboard-bg"></div>

      <div className="leaderboard-wrapper">
        <h2 className="leaderboard-title">🏆 Global Leaderboard</h2>

        <div className="leaderboard-card">
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>User</th>
                <th>Points</th>
                <th>Problems</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => (
                <tr
                  key={user.rank}
                  className={`lb-row ${user.rank <= 3 ? "lb-top" : ""}`}
                >
                  {/* Medal + Rank */}
                  <td className="lb-rank">
                    {user.rank <= 3 ? (
                      <div className="medal-box">
                        <img
                          src={getMedalSrc(user.rank)}
                          alt="medal"
                          className="medal-img"
                        />
                        <span className="rank-text">{user.rank}</span>
                      </div>
                    ) : (
                      <span className="rank-text">{user.rank}</span>
                    )}
                  </td>

                  {/* Name */}
                  <td className="lb-name">{user.name}</td>

                  {/* Points */}
                  <td className="lb-points">{user.points}</td>

                  {/* Problems */}
                  <td>{user.problems}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}