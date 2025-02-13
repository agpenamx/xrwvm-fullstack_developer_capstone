import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css"; // 🔧 SUGGESTION: Create and customize Home.css for styling the home page
import Header from "../Header/Header";

const Home = () => {
  const navigate = useNavigate();
  // ✅ Retrieve the username from sessionStorage (if available)
  const [username, setUsername] = useState(sessionStorage.getItem("username") || "");

  // ✅ Update username when component mounts
  useEffect(() => {
    setUsername(sessionStorage.getItem("username"));
  }, []);

  // ✅ Handler for logout using React Router's navigation for smoother redirection
  const handleLogout = async () => {
    try {
      // 🔧 SUGGESTION: Ensure your logout endpoint URL is correct (trailing slash if needed)
      const logoutUrl = window.location.origin + "/djangoapp/logout";
      const res = await fetch(logoutUrl, { method: "GET" });
      const json = await res.json();
      if (json) {
        sessionStorage.removeItem("username");
        // 🔧 SUGGESTION: Use navigate to redirect instead of window.location.href for client-side routing
        navigate("/");
      } else {
        alert("Logout failed. Please try again.");
      }
    } catch (error) {
      console.error("Error during logout:", error);
      alert("An error occurred during logout.");
    }
  };

  return (
    <div className="home-container">
      <Header />
      <div className="home-content" style={{ padding: "20px", textAlign: "center" }}>
        <h1>Welcome to Best Cars Dealership</h1>
        {/* Display different options based on whether a user is logged in */}
        {username ? (
          <div>
            <p>Hello, {username}!</p>
            <button onClick={handleLogout} className="btn btn-secondary">Logout</button>
          </div>
        ) : (
          <div>
            <button onClick={() => navigate("/login")} className="btn btn-primary" style={{ marginRight: "10px" }}>
              Login
            </button>
            <button onClick={() => navigate("/register")} className="btn btn-success">
              Register
            </button>
          </div>
        )}
        <p style={{ marginTop: "20px" }}>
          Explore our dealer listings, read reviews, and find the best cars in North America.
        </p>
      </div>
    </div>
  );
};

export default Home;