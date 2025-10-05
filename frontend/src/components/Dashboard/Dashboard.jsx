// src/components/Dashboard/Dashboard.jsx

import React, { useState } from 'react';
import Header from '../Layout/Header';
import ExpenseForm from './ExpenseForm';
import RecentExpenses from './RecentExpenses';
import { useExpenses } from '../../hooks/useExpense.jsx';
import { CATEGORY_EMOJI } from '../../utils/constants';

const Dashboard = () => {
  const [showModal, setShowModal] = useState(false);
  
  const {
    expenses,
    stats,
    categoryStats,
    loading,
    error,
    addExpense,
    removeExpense,
    refetch,
  } = useExpenses();

  const handleAddExpense = async (amount, category, description) => {
    await addExpense(amount, category, description);
    setShowModal(false);
  };

  const handleDeleteExpense = async (id) => {
    await removeExpense(id);
  };

  if (loading) {
    return (
      <>
        <Header />
        <div className="container">
          <div className="loading-state">
            <div className="loader"></div>
            <p>Loading expenses...</p>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header />
        <div className="container">
          <div className="error-state">
            <p>Error: {error}</p>
            <button onClick={refetch} className="btn btn-primary">
              Retry
            </button>
          </div>
        </div>
      </>
    );
  }

  // Get most spent category
  const mostSpentCategory = categoryStats && categoryStats.length > 0 ? categoryStats[0] : null;

  return (
    <>
      <Header />
      <div className="container">
        {/* Dashboard Header with Add Expense and Stats */}
        <div className="dashboard-header">
          <div className="header-actions">
            <button onClick={() => setShowModal(true)} className="btn btn-primary btn-add">
              + Add Expense
            </button>
          </div>
          <div className="stats-row">
            <div className="stat-card stat-card-total">
              <div className="stat-label">Total Spent This Month</div>
              <div className="stat-value">${stats?.total_amount?.toFixed(2) || '0.00'}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Most Spent Category</div>
              <div className="stat-value">
                {mostSpentCategory 
                  ? `${CATEGORY_EMOJI[mostSpentCategory.category] || '📦'} ${mostSpentCategory.category}`
                  : 'N/A'}
              </div>
            </div>
          </div>
        </div>

        {/* Recent Transactions */}
        <RecentExpenses
          expenses={expenses}
          onDelete={handleDeleteExpense}
        />

        {showModal && (
          <div className="modal-overlay" onClick={() => setShowModal(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <button className="modal-close" onClick={() => setShowModal(false)}>
                ×
              </button>
              <ExpenseForm onExpenseAdded={handleAddExpense} />
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default Dashboard;