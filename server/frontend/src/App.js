// ✅ Import React (Fix: Required for JSX)
import React from "react";
import { Routes, Route } from "react-router-dom";
// Import LoginPanel component for user login
import LoginPanel from "./components/Login/Login";
// Import RegisterPanel component for user registration
import RegisterPanel from "./components/Register/Register"; 
// Import Home component which serves as the landing page
import Home from "./components/Home/Home"; 
// Import Dealers component to list all dealers
import Dealers from "./components/Dealers/Dealers";   // ✅ New Import
// Import Dealer component to show details and reviews for a specific dealer
import Dealer from "./components/Dealers/Dealer";     // ✅ New Import
// Import PostReview component to allow logged-in users to submit reviews
import PostReview from "./components/Dealers/PostReview";  // ✅ New Import

function App() {
  return (
    <Routes>
      {/* ✅ Home Page - Detects if user is logged in */}
      <Route path="/" element={<Home />} />

      {/* ✅ Login Page */}
      <Route path="/login" element={<LoginPanel />} />

      {/* ✅ Registration Page */}
      <Route path="/register" element={<RegisterPanel />} />

      {/* ✅ Dealers Page - Lists all dealers */}
      <Route path="/dealers" element={<Dealers />} />

      {/* ✅ Dealer Page - Shows details and reviews for a dealer */}
      <Route path="/dealer/:id" element={<Dealer />} />

      {/* ✅ Post Review Page - Allows logged-in users to submit reviews */}
      <Route path="/postreview/:id" element={<PostReview />} />
      {/* 🔧 SUGGESTION: Ensure your React Router version is compatible with your code setup */}
    </Routes>
  );
}

export default App;