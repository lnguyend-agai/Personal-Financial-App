// src/pages/LoginPage.js
import React, { useState } from "react";
import Login from "../components/Login";

const LoginPage = () => {
  const [isRegistering, setIsRegistering] = useState(false);

  return (
    <div className="login-page">
      {isRegistering ? (
        <h2>Trang đăng ký (Chưa làm)</h2>
      ) : (
        <Login onSwitch={() => setIsRegistering(true)} />
      )}
    </div>
  );
};

export default LoginPage;
