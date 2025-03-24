// src/components/Dashboard.js
import React, { useState } from "react";

const Dashboard = ({ username }) => {
  const [date, setDate] = useState("");
  const [expenses, setExpenses] = useState({ food: "", transport: "" });
  const [income, setIncome] = useState({ salary: "", coffeeSales: "" });

  const handleExpensesChange = (e) => {
    const { name, value } = e.target;
    setExpenses((prev) => ({ ...prev, [name]: value }));
  };

  const handleIncomeChange = (e) => {
    const { name, value } = e.target;
    setIncome((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    // Create payload for Transaction
    const transactionsPayload = [
      {
        type: "expense",
        category: "food",
        amount: parseFloat(expenses.food),
      },
      {
        type: "expense",
        category: "transport",
        amount: parseFloat(expenses.transport),
      },
      {
        type: "income",
        category: "salary",
        amount: parseFloat(income.salary),
      },
      {
        type: "income",
        category: "coffeeSales",
        amount: parseFloat(income.coffeeSales),
      },
    ];

    try {
      // Send each transaction to Transaction API
      for (const transaction of transactionsPayload) {
        const transactionResponse = await fetch("/api/transactions/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Token ${token}` : "",           },
          body: JSON.stringify(transaction),
        });

        if (!transactionResponse.ok) {
          const errorDetails = await transactionResponse.json();
          alert("Transaction API Error:", errorDetails);
          throw new Error(`Failed to create Transaction: ${transactionResponse.status} - ${transactionResponse.statusText}`);
        }
      }

      alert("Transactions saved successfully!");
    } catch (error) {
      alert(`Error: ${error.message}`);
      alert("Failed to save transactions. Please try again.");
    }
  };

  return (
    <div className="dashboard">
      <h1>Hello {username}</h1>
      <form onSubmit={handleSubmit}>
        {/* Date Input */}
        <div>
          <label>Date:</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </div>

        {/* Expenses Section */}
        <div>
          <h2>Expenses</h2>
          <div>
            <label>Food:</label>
            <input
              type="number"
              name="food"
              value={expenses.food}
              onChange={handleExpensesChange}
              placeholder="Enter food expenses"
              required
            />
          </div>
          <div>
            <label>Transport:</label>
            <input
              type="number"
              name="transport"
              value={expenses.transport}
              onChange={handleExpensesChange}
              placeholder="Enter transport expenses"
              required
            />
          </div>
        </div>

        {/* Income Section */}
        <div>
          <h2>Income</h2>
          <div>
            <label>Salary:</label>
            <input
              type="number"
              name="salary"
              value={income.salary}
              onChange={handleIncomeChange}
              placeholder="Enter salary income"
              required
            />
          </div>
          <div>
            <label>Coffee Sales:</label>
            <input
              type="number"
              name="coffeeSales"
              value={income.coffeeSales}
              onChange={handleIncomeChange}
              placeholder="Enter coffee sales income"
              required
            />
          </div>
        </div>

        {/* Submit Button */}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Dashboard;