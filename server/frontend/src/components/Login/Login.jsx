import React, { useState } from 'react';
import "./Login.css";
import Header from '../Header/Header';
import { useNavigate } from 'react-router-dom'; // ✅ Improved navigation handling

const Login = ({ onClose }) => {
  // ✅ State for username, password, errors, and modal visibility
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(true);
  const navigate = useNavigate(); // ✅ Enables redirecting users after login

  // ✅ Define the login API endpoint
  // 🔧 FIX: Ensure the correct Django login URL is used
  let login_url = window.location.origin + "/api/login/";

  // 🔧 FIX: Function to fetch CSRF token (Re-enabled for security compliance)
  const getCsrfToken = () => {
    const token = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return token ? token.split('=')[1] : '';
  };

  const login = async (e) => {
    e.preventDefault();
    setError(null);  // ✅ Clear any previous error messages

    try {
      const res = await fetch(login_url, {
        method: "POST",
        credentials: "include", // ✅ Ensures cookies (session) are sent
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(), // ✅ Fix potential CSRF issues
        },
        body: JSON.stringify({
          "userName": userName,
          "password": password
        }),
      });

      if (!res.ok) {
        // ✅ Handle potential errors like 401 Unauthorized or 500 Internal Server Error
        const errorText = await res.text();
        throw new Error(`HTTP error! status: ${res.status}, message: ${errorText}`);
      }

      const json = await res.json();
      if (json.status === "Authenticated") {
        sessionStorage.setItem('username', json.userName);
        setOpen(false);  // ✅ Close modal upon successful login
        navigate("/"); // ✅ Redirect to home page
      } else {
        setError("Invalid username or password. Please try again.");
      }
    } catch (error) {
      console.error("Login error:", error);
      setError(error.message || "An unexpected error occurred.");
    }
  };

  return (
    <div>
      <Header />
      <div onClick={onClose}>
        <div
          onClick={(e) => {
            // ✅ Prevent modal from closing when clicking inside it
            e.stopPropagation();
          }}
          className='modalContainer'
        >
          <form className="login_panel" onSubmit={login}>
            <h2>Login</h2>
            <div>
              <label className="input_field">Username</label>
              <input
                type="text"
                name="username"
                placeholder="Username"
                className="input_field"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="input_field">Password</label>
              <input
                name="password"
                type="password"
                placeholder="Password"
                className="input_field"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error && <div className="error-message">{error}</div>}
            <div>
              <input className="action_button" type="submit" value="Login" />
              <input className="action_button" type="button" value="Cancel" onClick={() => setOpen(false)} />
            </div>
            <a className="loginlink" href="/register">Register Now</a>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;