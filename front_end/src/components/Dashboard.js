// src/components/Dashboard.js
import React, { useState } from "react";

const Dashboard = ({ username }) => {
  const [date, setDate] = useState("");
  const [expenses, setExpenses] = useState({ food: "", transport: "" });
  const [income, setIncome] = useState({ salary: "", coffeeSales: "" });
  const [monthlyExpense, setMonthlyExpense] = useState(null);
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
  
    try {
      // Tạo DailyRecord trước
      const dailyRecordPayload = {
        date: date, // Ngày được chọn từ form
        total_income: parseFloat(income.salary) + parseFloat(income.coffeeSales),
        total_expense: parseFloat(expenses.food) + parseFloat(expenses.transport),
      };
  
      const dailyRecordResponse = await fetch("http://127.0.0.1:8000/api/daily-records/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Token ${token}` : "",
        },
        body: JSON.stringify(dailyRecordPayload),
      });
  
      if (!dailyRecordResponse.ok) {
        const errorDetails = await dailyRecordResponse.json();
        console.error("DailyRecord API Error:", errorDetails);
        throw new Error(`Failed to create DailyRecord: ${dailyRecordResponse.status} - ${dailyRecordResponse.statusText}`);
      }
  
      const dailyRecord = await dailyRecordResponse.json(); // Lấy DailyRecord vừa tạo
      const dailyRecordId = dailyRecord.id;
  
      // Tạo payload cho Transaction
      const transactionsPayload = [
        {
          daily_record: dailyRecordId,
          type: "expense",
          category: "food",
          amount: parseFloat(expenses.food),
        },
        {
          daily_record: dailyRecordId,
          type: "expense",
          category: "transport",
          amount: parseFloat(expenses.transport),
        },
        {
          daily_record: dailyRecordId,
          type: "income",
          category: "salary",
          amount: parseFloat(income.salary),
        },
        {
          daily_record: dailyRecordId,
          type: "income",
          category: "coffeeSales",
          amount: parseFloat(income.coffeeSales),
        },
      ];
  
      // Gửi từng giao dịch đến Transaction API
      for (const transaction of transactionsPayload) {
        const transactionResponse = await fetch("http://127.0.0.1:8000/api/transactions/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Token ${token}` : "",
          },
          body: JSON.stringify(transaction),
        });
  
        if (!transactionResponse.ok) {
          const errorDetails = await transactionResponse.json();
          console.error("Transaction API Error:", errorDetails);
          throw new Error(`Failed to create Transaction: ${transactionResponse.status} - ${transactionResponse.statusText}`);
        }
      }
  
      alert("Transactions saved successfully!");
    } catch (error) {
      console.log(`Error: ${error.message}`);
      console.log("Failed to save transactions. Please try again.");
    }
  };

  const fetchMonthlyExpense = async () => {
    const token = localStorage.getItem("token");
  
    try {
      const response = await fetch("http://127.0.0.1:8000/api/transactions/monthly/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Token ${token}` : "",
        },
      });
  
      if (!response.ok) {
        throw new Error("Failed to fetch monthly expense");
      }
  
      const data = await response.json();
      setMonthlyExpense(data.total_expense); // Lưu tổng chi tiêu vào state
    } catch (error) {
      console.error("Error fetching monthly expense:", error);
      console.log("Failed to fetch monthly expense. Please try again.");
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
        <div>
            <button type="button" onClick={fetchMonthlyExpense}>Show Monthly Expense</button>
            {monthlyExpense !== null && (
              <div>
                <h3>Total Expense This Month: {monthlyExpense}</h3>
              </div>
            )}
        </div>
      </form>
    </div>

  );
};

export default Dashboard;