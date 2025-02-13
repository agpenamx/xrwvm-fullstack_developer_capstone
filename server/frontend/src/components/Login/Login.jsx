import React, { useState } from 'react';
import "./Login.css";
import Header from '../Header/Header';

const Login = ({ onClose }) => {
  // ✅ State for username, password, and modal visibility
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [open, setOpen] = useState(true);

  // ✅ Define the login API endpoint
  // 🔧 SUGGESTION: Ensure the trailing slash is correct based on your Django URL configuration.
  let login_url = window.location.origin + "/djangoapp/login";

  const login = async (e) => {
    e.preventDefault();
    // 🔧 SUGGESTION: Consider adding error handling for network issues.
    const res = await fetch(login_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "userName": userName,
        "password": password
      }),
    });
    
    const json = await res.json();
    // 🔧 SUGGESTION: Ensure the backend returns "status" and "userName" exactly as expected.
    if (json.status != null && json.status === "Authenticated") {
      // Save username in sessionStorage upon successful login
      sessionStorage.setItem('username', json.userName);
      setOpen(false);        
    } else {
      alert("The user could not be authenticated.");
    }
  };

  // If login is successful (open is false), redirect to the home page
  if (!open) {
    window.location.href = "/";
  }

  return (
    <div>
      <Header />
      <div onClick={onClose}>
        <div
          onClick={(e) => {
            // Prevent click propagation so the modal doesn't close unexpectedly
            e.stopPropagation();
          }}
          className='modalContainer'
        >
          <form className="login_panel" onSubmit={login}>
            <div>
              <span className="input_field">Username </span>
              <input
                type="text"
                name="username"
                placeholder="Username"
                className="input_field"
                onChange={(e) => setUserName(e.target.value)}
              />
            </div>
            <div>
              <span className="input_field">Password </span>
              <input
                name="psw"
                type="password"
                placeholder="Password"
                className="input_field"
                onChange={(e) => setPassword(e.target.value)}
              />            
            </div>
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