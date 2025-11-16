import { BrowserRouter, Routes, Route } from "react-router-dom";

import Landing from "./pages/Landing";
import SignUp from "./pages/SignUp";
import SignIn from "./pages/SignIn";
import Onboarding from "./pages/Onboarding";
import Dashboard from "./pages/Dashboard";
import Matching from "./pages/Matching";
import Solve from "./pages/Solve";
import Leaderboard from "./pages/Leaderboard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 1. Landing */}
        <Route path="/" element={<Landing />} />

        {/* 2. Auth */}
        <Route path="/signup" element={<SignUp />} />
        <Route path="/signin" element={<SignIn />} />

        {/* 3. Onboarding */}
        <Route path="/onboarding" element={<Onboarding />} />

        {/* 4. Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />

        {/* 5. Matchmaking */}
        <Route path="/matching" element={<Matching />} />

        {/* 6. Problem Solver (MCQ) */}
        <Route path="/solve/:problemId" element={<Solve />} />

        {/* 7. Leaderboard */}
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Routes>
    </BrowserRouter>
  );
}
