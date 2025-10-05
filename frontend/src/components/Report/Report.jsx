// src/components/Report/Report.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../Layout/Header';
import { api } from '../../services/api';
import { CATEGORY_EMOJI } from '../../utils/constants';

const Report = () => {
  const [allExpenses, setAllExpenses] = useState([]);
  const [filteredExpenses, setFilteredExpenses] = useState([]);
  const [timeFilter, setTimeFilter] = useState('month');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchReportData();
  }, []);

  useEffect(() => {
    filterExpensesByTime();
  }, [timeFilter, allExpenses]);

  const fetchReportData = async () => {
    try {
      setLoading(true);
      const expensesData = await api.listExpenses();
      setAllExpenses(expensesData.expenses);
    } catch (err) {
      console.error('Error fetching report data:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterExpensesByTime = () => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    let filtered = [...allExpenses];

    switch (timeFilter) {
      case 'daily':
        filtered = allExpenses.filter(exp => {
          const expDate = new Date(exp.date);
          const expDay = new Date(expDate.getFullYear(), expDate.getMonth(), expDate.getDate());
          return expDay.getTime() === today.getTime();
        });
        break;
      
      case 'week':
        const weekAgo = new Date(today);
        weekAgo.setDate(today.getDate() - 7);
        filtered = allExpenses.filter(exp => {
          const expDate = new Date(exp.date);
          return expDate >= weekAgo;
        });
        break;
      
      case 'month':
        const monthAgo = new Date(today);
        monthAgo.setDate(today.getDate() - 30);
        filtered = allExpenses.filter(exp => {
          const expDate = new Date(exp.date);
          return expDate >= monthAgo;
        });
        break;
      
      case '3months':
        const threeMonthsAgo = new Date(today);
        threeMonthsAgo.setMonth(today.getMonth() - 3);
        filtered = allExpenses.filter(exp => {
          const expDate = new Date(exp.date);
          return expDate >= threeMonthsAgo;
        });
        break;
      
      case '6months':
        const sixMonthsAgo = new Date(today);
        sixMonthsAgo.setMonth(today.getMonth() - 6);
        filtered = allExpenses.filter(exp => {
          const expDate = new Date(exp.date);
          return expDate >= sixMonthsAgo;
        });
        break;
      
      case 'year':
        const yearStart = new Date(now.getFullYear(), 0, 1);
        filtered = allExpenses.filter(exp => {
          const expDate = new Date(exp.date);
          return expDate >= yearStart;
        });
        break;
      
      case 'all':
      default:
        filtered = allExpenses;
    }

    setFilteredExpenses(filtered);
  };

  const calculateStats = () => {
    const total = filteredExpenses.reduce((sum, exp) => sum + exp.amount, 0);
    return {
      total_amount: total,
      total_expenses: filteredExpenses.length
    };
  };

  const calculateCategoryStats = () => {
    const categoryMap = {};
    
    filteredExpenses.forEach(exp => {
      if (!categoryMap[exp.category]) {
        categoryMap[exp.category] = {
          category: exp.category,
          total_amount: 0,
          total_expenses: 0
        };
      }
      categoryMap[exp.category].total_amount += exp.amount;
      categoryMap[exp.category].total_expenses += 1;
    });

    return Object.values(categoryMap).sort((a, b) => b.total_amount - a.total_amount);
  };

  const getTopExpenses = () => {
    return [...filteredExpenses]
      .sort((a, b) => b.amount - a.amount)
      .slice(0, 3);
  };

  const getLargestExpense = () => {
    if (filteredExpenses.length === 0) return 0;
    return Math.max(...filteredExpenses.map(exp => exp.amount));
  };

  const getDailyAverage = () => {
    if (filteredExpenses.length === 0) return 0;
    
    // Get date range
    const dates = filteredExpenses.map(exp => new Date(exp.date).toDateString());
    const uniqueDays = new Set(dates).size;
    
    if (uniqueDays === 0) return 0;
    return stats.total_amount / uniqueDays;
  };

  const getTodayTotalSpent = () => {
    const now = new Date();
    // Get today's date in UTC
    const todayUTC = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
    
    const todayExpenses = allExpenses.filter(exp => {
      const expDate = new Date(exp.date);
      // Get expense date in UTC
      const expUTC = Date.UTC(expDate.getUTCFullYear(), expDate.getUTCMonth(), expDate.getUTCDate());
      return expUTC === todayUTC;
    });
    
    return todayExpenses.reduce((sum, exp) => sum + exp.amount, 0);
  };

  const getTodayAverage = () => {
    const now = new Date();
    // Get today's date in UTC
    const todayUTC = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
    
    const todayExpenses = allExpenses.filter(exp => {
      const expDate = new Date(exp.date);
      // Get expense date in UTC
      const expUTC = Date.UTC(expDate.getUTCFullYear(), expDate.getUTCMonth(), expDate.getUTCDate());
      return expUTC === todayUTC;
    });
    
    if (todayExpenses.length === 0) return 0;
    const todayTotal = todayExpenses.reduce((sum, exp) => sum + exp.amount, 0);
    return todayTotal / todayExpenses.length;
  };

  const getAverageExpense = (stats) => {
    if (stats.total_expenses === 0) return 0;
    return stats.total_amount / stats.total_expenses;
  };

  const getCategoryPercentage = (categoryAmount, totalAmount) => {
    if (totalAmount === 0) return 0;
    return ((categoryAmount / totalAmount) * 100).toFixed(1);
  };

  if (loading) {
    return (
      <>
        <Header />
        <div className="container">
          <div className="loading-state">
            <div className="loader"></div>
            <p>Loading report...</p>
          </div>
        </div>
      </>
    );
  }

  if (allExpenses.length === 0) {
    return (
      <>
        <Header />
        <div className="container">
          <div className="report-container">
            <button onClick={() => navigate('/dashboard')} className="btn btn-outline">
              ← Back to Dashboard
            </button>
            <div className="empty-state">
              <div className="empty-icon">📊</div>
              <p>No expenses to report</p>
              <p className="empty-subtitle">Add some expenses to see your report summary</p>
            </div>
          </div>
        </div>
      </>
    );
  }

  const stats = calculateStats();
  const categoryStats = calculateCategoryStats();
  const topExpenses = getTopExpenses();
  const dailyAverage = getDailyAverage();
  const todayTotalSpent = getTodayTotalSpent();
  const todayAverage = getTodayAverage();

  if (filteredExpenses.length === 0) {
    return (
      <>
        <Header />
        <div className="container">
          <div className="report-container">
            <div className="report-header">
              <button onClick={() => navigate('/dashboard')} className="btn btn-outline">
                ← Back to Dashboard
              </button>
              <select 
                className="time-filter-select"
                value={timeFilter}
                onChange={(e) => setTimeFilter(e.target.value)}
              >
                <option value="month">This Month</option>
                <option value="3months">Last 3 Months</option>
                <option value="6months">Last 6 Months</option>
                <option value="year">This Year</option>
                <option value="all">All Time</option>
              </select>
            </div>
            <div className="empty-state">
              <div className="empty-icon">📊</div>
              <p>No expenses in this time period</p>
              <p className="empty-subtitle">Try selecting a different time range</p>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <div className="container">
        <div className="report-container">
          <div className="report-header">
            <button onClick={() => navigate('/dashboard')} className="btn btn-outline">
              ← Back to Dashboard
            </button>
            <select 
              className="time-filter-select"
              value={timeFilter}
              onChange={(e) => setTimeFilter(e.target.value)}
            >
              <option value="daily">Today</option>
              <option value="month">This Month</option>
              <option value="3months">Last 3 Months</option>
              <option value="6months">Last 6 Months</option>
              <option value="year">This Year</option>
              <option value="all">All Time</option>
            </select>
          </div>

          {/* Overview Stats */}
          <div className="report-section">
            <h2 className="report-section-title">Overview</h2>
            <div className="report-stats-grid">
              <div className="report-stat-card">
                <div className="report-stat-label">Total Spent</div>
                <div className="report-stat-value">${stats.total_amount.toFixed(2)}</div>
              </div>
              <div className="report-stat-card">
                <div className="report-stat-label">Daily Average</div>
                <div className="report-stat-value">${dailyAverage.toFixed(2)}</div>
              </div>
              <div className="report-stat-card">
                <div className="report-stat-label">Today's Total Spent</div>
                <div className="report-stat-value">${todayTotalSpent.toFixed(2)}</div>
              </div>
              <div className="report-stat-card">
                <div className="report-stat-label">Today's Average</div>
                <div className="report-stat-value">${todayAverage.toFixed(2)}</div>
              </div>
            </div>
          </div>

          {/* Category Breakdown */}
          <div className="report-section">
            <h2 className="report-section-title">Spending by Category</h2>
            <div className="category-breakdown">
              {categoryStats.map((cat) => (
                <div key={cat.category} className="category-breakdown-item">
                  <div className="category-breakdown-header">
                    <div className="category-breakdown-info">
                      <span className="category-breakdown-emoji">
                        {CATEGORY_EMOJI[cat.category]}
                      </span>
                      <span className="category-breakdown-name">{cat.category}</span>
                    </div>
                    <div className="category-breakdown-amount">
                      <span className="category-breakdown-value">
                        ${cat.total_amount.toFixed(2)}
                      </span>
                      <span className="category-breakdown-percentage">
                        {getCategoryPercentage(cat.total_amount, stats.total_amount)}%
                      </span>
                    </div>
                  </div>
                  <div className="category-breakdown-bar">
                    <div
                      className="category-breakdown-fill"
                      style={{ width: `${getCategoryPercentage(cat.total_amount, stats.total_amount)}%` }}
                    ></div>
                  </div>
                  <div className="category-breakdown-count">
                    {cat.total_expenses} expense{cat.total_expenses !== 1 ? 's' : ''}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Insights */}
          {categoryStats.length > 0 && (
            <div className="report-section">
              <h2 className="report-section-title">Insights</h2>
              <div className="insights-grid">
                <div className="insight-card">
                  <div className="insight-icon">🎯</div>
                  <div className="insight-content">
                    <div className="insight-title">Most Spent Category</div>
                    <div className="insight-value">
                      {CATEGORY_EMOJI[categoryStats[0].category]} {categoryStats[0].category}
                    </div>
                    <div className="insight-subtitle">
                      ${categoryStats[0].total_amount.toFixed(2)} spent
                    </div>
                  </div>
                </div>
                
                <div className="insight-card">
                  <div className="insight-icon">💰</div>
                  <div className="insight-content">
                    <div className="insight-title">Highest Single Expense</div>
                    <div className="insight-value">${topExpenses[0].amount.toFixed(2)}</div>
                    <div className="insight-subtitle">
                      {topExpenses[0].category}
                    </div>
                  </div>
                </div>

                <div className="insight-card">
                  <div className="insight-icon">📊</div>
                  <div className="insight-content">
                    <div className="insight-title">Most Frequent Category</div>
                    <div className="insight-value">
                      {CATEGORY_EMOJI[categoryStats[0].category]} {categoryStats[0].category}
                    </div>
                    <div className="insight-subtitle">
                      {categoryStats[0].total_expenses} transactions
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Top Expenses */}
          {topExpenses.length > 0 && (
            <div className="report-section">
              <h2 className="report-section-title">Top {topExpenses.length} Transactions</h2>
              <div className="top-expenses-list">
                {topExpenses.map((expense, index) => (
                  <div key={expense.id} className="top-expense-item">
                    <div className="top-expense-rank">{index + 1}</div>
                    <div className="top-expense-info">
                      <div className="top-expense-category">
                        <span className="top-expense-emoji">
                          {CATEGORY_EMOJI[expense.category]}
                        </span>
                        <span>{expense.category}</span>
                      </div>
                      {expense.description && (
                        <div className="top-expense-description">{expense.description}</div>
                      )}
                    </div>
                    <div className="top-expense-amount">${expense.amount.toFixed(2)}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Report;