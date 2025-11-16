
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
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

export default function Matching() {
  const [partnerId, setPartnerId] = useState(null);
  const [loading, setLoading] = useState(true);
  const nav = useNavigate();

  useEffect(() => {
    async function pair() {
      const res = await api.post("/pair", { user_id: 1 }); 
      setPartnerId(res.data.partner_id);
      setLoading(false);
    }
    pair();
  }, []);

  if (loading) return <p>Finding a study buddy...</p>;

  return (
    <>
      <Navbar />
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <h2>You're paired with user {partnerId}</h2>
        <button onClick={() => nav("/dashboard")}>Continue</button>
      </div>
    </>
  );
}
