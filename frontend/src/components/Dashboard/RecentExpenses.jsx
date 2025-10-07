// src/components/Dashboard/RecentExpenses.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import { CATEGORY_COLORS, CATEGORY_EMOJI } from '../../utils/constants';

const RecentExpenses = ({ expenses, onDelete }) => {
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [timezone, setTimezone] = useState(() => {
    const saved = localStorage.getItem('timezone');
    return saved || 'Sydney';
  });
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.setItem('timezone', timezone);
  }, [timezone]);

  // Show only latest 5
  const recentExpenses = expenses.slice(0, 5);

  const handleDelete = async (id) => {
    try {
      await onDelete(id);
      setDeleteConfirm(null);
    } catch (err) {
      console.error('Error deleting expense:', err);
    }
  };

  const getRelativeTime = (dateString) => {
    try {
      const utcDateString = dateString.endsWith('Z') ? dateString : dateString + 'Z';
      const date = new Date(utcDateString);
      return formatDistanceToNow(date, { addSuffix: true });
    } catch {
      return '';
    }
  };

  const formatDate = (dateString) => {
    try {
      const utcDateString = dateString.endsWith('Z') ? dateString : dateString + 'Z';
      const date = new Date(utcDateString);
      
      const timezoneMap = {
        'Sydney': 'Australia/Sydney',
        'NZ': 'Pacific/Auckland'
      };
      
      return new Intl.DateTimeFormat('en-AU', {
        timeZone: timezoneMap[timezone],
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      }).format(date);
    } catch {
      return dateString;
    }
  };

  return (
    <div className="expense-list-container">
      <div className="expense-list-header">
        <h2 className="section-title">Recent Transactions</h2>
        <div className="expense-header-actions">
          <button 
            className="btn btn-outline"
            onClick={() => navigate('/expenses')}
          >
            All Expenses
          </button>
          <button 
            className="btn btn-outline btn-report"
            onClick={() => navigate('/report')}
          >
            Report Summary
          </button>
        </div>
      </div>

      {recentExpenses.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📊</div>
          <p>No expenses yet</p>
          <p className="empty-subtitle">Add your first expense to get started!</p>
        </div>
      ) : (
        <>
          <div className="expense-list">
            {recentExpenses.map((expense) => (
              <div
                key={expense.id}
                className="expense-item"
                style={{ borderLeftColor: CATEGORY_COLORS[expense.category] }}
              >
                <div className="expense-info">
                  <div className="expense-top">
                    <span className="expense-emoji">{CATEGORY_EMOJI[expense.category]}</span>
                    <span className="expense-category">{expense.category}</span>
                    <span className="expense-amount">${expense.amount.toFixed(2)}</span>
                  </div>
                  {expense.description && (
                    <div className="expense-description">{expense.description}</div>
                  )}
                  <div className="expense-date-wrapper">
                    <div className="expense-date">{formatDate(expense.date)}</div>
                    <div className="expense-relative-time">{getRelativeTime(expense.date)}</div>
                  </div>
                </div>
                <button
                  className="btn-delete"
                  onClick={() => setDeleteConfirm(expense.id)}
                  title="Delete expense"
                >
                  ✕
                </button>

                {deleteConfirm === expense.id && (
                  <div className="delete-confirm">
                    <p>Delete this expense?</p>
                    <div className="delete-actions">
                      <button
                        className="btn btn-danger-sm"
                        onClick={() => handleDelete(expense.id)}
                      >
                        Yes
                      </button>
                      <button
                        className="btn btn-outline-sm"
                        onClick={() => setDeleteConfirm(null)}
                      >
                        No
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="see-more-container">
            <button 
              className="btn btn-primary btn-see-more"
              onClick={() => navigate('/expenses')}
            >
              See All Expenses
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default RecentExpenses;