import Navbar from "../components/Navbar";

export default function Leaderboard() {
  return (
    <>
      <Navbar />

      <div style={{ padding: "2rem" }}>
        <h2>🏆 Leaderboard</h2>

        <table style={styles.table}>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Name</th>
              <th>Points</th>
              <th>Problems</th>
            </tr>
          </thead>
          <tbody>
            {[...Array(20)].map((_, i) => (
              <tr key={i}>
                <td>{i + 1}</td>
                <td>User {i + 1}</td>
                <td>{Math.floor(Math.random() * 500)}</td>
                <td>{Math.floor(Math.random() * 50)}</td>
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
  }
};
