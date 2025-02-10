import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import RegisterPanel from "./components/Register/Register"; 
import Home from "./components/Home/Home"; 

function App() {
  return (
    <Routes>
      {/* Home Page - Detects if user is logged in */}
      <Route path="/" element={<Home />} />

      {/* Login Page */}
      <Route path="/login" element={<LoginPanel />} />

      {/* Registration Page */}
      <Route path="/register" element={<RegisterPanel />} />
    </Routes>
  );
}

export default App;