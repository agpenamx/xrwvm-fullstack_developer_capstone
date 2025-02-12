// ✅ Import React (Fix: Required for JSX)
import React from "react";
import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import RegisterPanel from "./components/Register/Register"; 
import Home from "./components/Home/Home"; 
import Dealers from "./components/Dealers/Dealers";   // ✅ New Import
import Dealer from "./components/Dealers/Dealer";     // ✅ New Import
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
    </Routes>
  );
}

export default App;