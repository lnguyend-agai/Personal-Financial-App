// src/components/Login.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = ({ onSwitch }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });
      if (response.ok) {
        const data = await response.json();
        alert("Login successful");
        // Save token and username
        localStorage.setItem("token", data.token);
        localStorage.setItem("username", username);
        // Redirect to dashboard
        navigate("/dashboard");
      } else {
        alert("Login failed: Invalid username or password");
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Finance App</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <div className="password-container">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
          >
            👁
          </button>
        </div>
        <button type="submit" className="btn-login">Login</button>
        <button type="button" className="btn-register" onClick={onSwitch}>
          Register a new account
        </button>
      </form>
    </div>
  );
};

export default Login;