// src/components/Dashboard/ExpenseList.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import { CATEGORIES, CATEGORY_COLORS, CATEGORY_EMOJI } from '../../utils/constants';

const ExpenseList = ({ expenses, onDelete, onFilterCategory }) => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [timezone, setTimezone] = useState('Sydney');
  const navigate = useNavigate();

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
    if (category === 'All') {
      onFilterCategory(null);
    } else {
      onFilterCategory(category);
    }
  };

  const handleDelete = async (id) => {
    try {
      await onDelete(id);
      setDeleteConfirm(null);
    } catch (err) {
      console.error('Error deleting expense:', err);
    }
  };

  const formatDateWithTimezone = (dateString) => {
    try {
      // Backend returns UTC time without 'Z', so we need to append it
      const utcDateString = dateString.endsWith('Z') ? dateString : dateString + 'Z';
      const date = new Date(utcDateString);
      
      const timezoneMap = {
        'Sydney': 'Australia/Sydney',
        'NZ': 'Pacific/Auckland'
      };
      
      // Format in selected timezone
      const formattedDate = new Intl.DateTimeFormat('en-AU', {
        timeZone: timezoneMap[timezone],
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      }).format(date);
      
      return formattedDate;
    } catch {
      return dateString;
    }
  };

  const getRelativeTime = (dateString) => {
    try {
      // Backend returns UTC time without 'Z', so we need to append it
      const utcDateString = dateString.endsWith('Z') ? dateString : dateString + 'Z';
      const date = new Date(utcDateString);
      return formatDistanceToNow(date, { addSuffix: true });
    } catch {
      return '';
    }
  };

  return (
    <div className="expense-list-container">
      <div className="expense-list-header">
        <h2 className="section-title">Expense History</h2>
        <div className="expense-header-actions">
          <button 
            className="btn btn-outline btn-report"
            onClick={() => navigate('/report')}
          >
            Report Summary
          </button>
          <select 
            className="timezone-select"
            value={timezone}
            onChange={(e) => setTimezone(e.target.value)}
          >
            <option value="Sydney">Sydney Time</option>
            <option value="NZ">NZ Time</option>
          </select>
        </div>
      </div>
      
      <div className="category-filter">
        <button
          className={`filter-btn ${selectedCategory === 'All' ? 'active' : ''}`}
          onClick={() => handleCategoryFilter('All')}
        >
          All
        </button>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            className={`filter-btn ${selectedCategory === cat ? 'active' : ''}`}
            onClick={() => handleCategoryFilter(cat)}
          >
            {CATEGORY_EMOJI[cat]} {cat}
          </button>
        ))}
      </div>

      {expenses.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📊</div>
          <p>No expenses yet</p>
          <p className="empty-subtitle">Add your first expense to get started!</p>
        </div>
      ) : (
        <div className="expense-list">
          {expenses.map((expense) => (
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
                  <div className="expense-date">{formatDateWithTimezone(expense.date)}</div>
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
      )}
    </div>
  );
};

export default ExpenseList;