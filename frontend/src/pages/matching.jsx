

// this page basically interacts with flask 
// assuming backend returns a JSON like :
// {
//     "match": {
//       "name": "Bob",
//       "reason": "3 shared courses"
//     }
//   }
  


import { useEffect, useState } from "react";
import { api } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Matching() {
  const [loading, setLoading] = useState(true);
  const [match, setMatch] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function findMatch() {
      const res = await api.post("/match");
      setMatch(res.data.match);
      setLoading(false);
    }

    findMatch();
  }, []);

  if (loading) return <p>Finding a study buddy...</p>;

  return (
    <div>
      <h2>You got matched!</h2>
      <p>Partner: {match.name}</p>
      <p>Reason: {match.reason}</p>

      <button onClick={() => navigate("/challenge")}>
        Start Today’s Challenge
      </button>
    </div>
  );
}
