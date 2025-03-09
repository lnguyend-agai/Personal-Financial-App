// src/pages/LoginPage.js
import React, { useState } from "react";
import Login from "../components/Login";
import Register from "../components/Register";

const LoginPage = () => {
  const [isRegistering, setIsRegistering] = useState(false);

  return (
    <div className="login-page">
      {isRegistering ? (
        <Register onSwitch={() => setIsRegistering(false)} />
      ) : (
        <Login onSwitch={() => setIsRegistering(true)} />
      )}
    </div>
  );
};

export default LoginPage;
