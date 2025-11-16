
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
import Navbar from "../components/Navbar";

export default function Matching() {
  const [loading, setLoading] = useState(true);
  const [match, setMatch] = useState(null);
  const nav = useNavigate();

  useEffect(() => {
    async function find() {
      const res = await api.post("/match");
      setMatch(res.data.match);
      setLoading(false);
    }
    find();
  }, []);

  if (loading) return <p>Finding a study buddy...</p>;

  return (
    <>
      <Navbar />

      <div style={{ padding: "2rem", textAlign: "center" }}>
        <h2>You got matched!</h2>
        <p>Partner: {match.name}</p>
        <p>Reason: {match.reason}</p>

        <button onClick={() => nav("/dashboard")}>Continue</button>
      </div>
    </>
  );
}
