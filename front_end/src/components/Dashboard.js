// src/components/Dashboard.js
import React, { useState } from "react";
import './Dashboard.css';

const Dashboard = ({ username }) => {
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1); // Mặc định là tháng hiện tại
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear()); // Mặc định là năm hiện tại
  const [date, setDate] = useState("");
  const [expenses, setExpenses] = useState({ food: "", transport: "" });
  const [income, setIncome] = useState({ salary: "", coffeeSales: "" });
  const [monthlyExpense, setMonthlyExpense] = useState(null);
  const [dailyExpenses, setDailyExpenses] = useState([]);
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
          date : date,
        },
        {
          daily_record: dailyRecordId,
          type: "expense",
          category: "transport",
          amount: parseFloat(expenses.transport),
          date : date,
        },
        {
          daily_record: dailyRecordId,
          type: "income",
          category: "salary",
          amount: parseFloat(income.salary),
          date : date,
        },
        {
          daily_record: dailyRecordId,
          type: "income",
          category: "coffeeSales",
          amount: parseFloat(income.coffeeSales),
          date : date,
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
      const response = await fetch(
        `http://127.0.0.1:8000/api/transactions/monthly/?month=${selectedMonth}&year=${selectedYear}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Token ${token}` : "",
          },
        }
      );
  
      if (!response.ok) {
        throw new Error("Failed to fetch monthly expense");
      }
  
      const data = await response.json();
      setMonthlyExpense(data); // Lưu tổng chi tiêu vào state
    } catch (error) {
      console.error("Error fetching monthly expense:", error);
      console.log("Failed to fetch monthly expense. Please try again.");
    }
  };

  const fetchDailyExpenses = async () => {
    const token = localStorage.getItem("token");
    const month = selectedMonth; // Giá trị tháng được chọn
    const year = selectedYear;   // Giá trị năm được chọn
  
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/transactions/daily-expenses/?month=${month}&year=${year}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Token ${token}` : "",
          },
        }
      );
  
      if (!response.ok) {
        throw new Error("Failed to fetch daily expenses");
      }
  
      const data = await response.json();
      setDailyExpenses(data.daily_expenses); // Lưu dữ liệu vào state
    } catch (error) {
      console.error("Error fetching daily expenses:", error);
    }
  };
  const SendReportToEmail = async () => {
    const token = localStorage.getItem("token");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/transactions/send-monthly-report/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Token ${token}` : "",
          },
        }
      );
  
      if (!response.ok) {
        throw new Error("Failed to send report to email");
      }
      
      alert("Report sent to email successfully!");
    } catch (error) {
      console.error("Error when sending e-mail:", error);
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
          <label>Month:</label>
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
          >
            {Array.from({ length: 12 }, (_, i) => (
              <option key={i + 1} value={i + 1}>
                {new Date(0, i).toLocaleString("default", { month: "long" })}
              </option>
            ))}
          </select>

          <label>Year:</label>
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
          >
            {Array.from({ length: 10 }, (_, i) => (
              <option key={i} value={new Date().getFullYear() - i}>
                {new Date().getFullYear() - i}
              </option>
            ))}
          </select>
        </div>

        <div>
            <button type="button" onClick={fetchMonthlyExpense}>Show Monthly Transaction</button>
            {monthlyExpense !== null && (
              <div>
                <h3>Total Expense This Month: {monthlyExpense.total_expense}</h3>
                <h3>Total Income This Month: {monthlyExpense.total_income}</h3>
                <h3>Total Net Balance This Month: {monthlyExpense.net_balance}</h3>
              </div>
            )}
        </div>

        <div>
          <button type="button" onClick={fetchDailyExpenses}>
            Show Daily Expenses
          </button>

          {dailyExpenses.length > 0 && (
            <table border="1">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Income</th>
                  <th>Expense</th>
                </tr>
              </thead>
              <tbody>
                {dailyExpenses.map((expense, index) => (
                  <tr key={index}>
                    <td>{expense.date}</td>
                    <td>{expense.income}</td>
                    <td>{expense.expense}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div>
          <button type="button" onClick={SendReportToEmail}>
            Send Monthly Transaction Report to Email
          </button>
        </div>
      </form>
    </div>

  );
};

export default Dashboard;