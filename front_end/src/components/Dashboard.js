// src/components/Dashboard.js
import React from "react";

const Dashboard = ({ username }) => {
  return (
    <div className="dashboard">
      <h1>Hello {username}</h1>
    </div>
  );
};

export default Dashboard;