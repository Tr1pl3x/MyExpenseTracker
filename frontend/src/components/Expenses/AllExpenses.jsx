// src/components/Expenses/AllExpenses.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import Header from '../Layout/Header';
import { useExpenses } from '../../hooks/useExpense.jsx';
import { CATEGORIES, CATEGORY_COLORS, CATEGORY_EMOJI } from '../../utils/constants';

const AllExpenses = () => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [timezone, setTimezone] = useState('Sydney');
  const [currentPage, setCurrentPage] = useState(1);
  const navigate = useNavigate();

  const ITEMS_PER_PAGE = 8;

  const {
    expenses,
    loading,
    error,
    removeExpense,
    filterByCategory,
    refetch,
  } = useExpenses();

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
    setCurrentPage(1); // Reset to first page when filtering
    if (category === 'All') {
      refetch();
    } else {
      filterByCategory(category);
    }
  };

  const handleDelete = async (id) => {
    try {
      await removeExpense(id);
      setDeleteConfirm(null);
    } catch (err) {
      console.error('Error deleting expense:', err);
    }
  };

  const formatDateWithTimezone = (dateString) => {
    try {
      const utcDateString = dateString.endsWith('Z') ? dateString : dateString + 'Z';
      const date = new Date(utcDateString);
      
      const timezoneMap = {
        'Sydney': 'Australia/Sydney',
        'NZ': 'Pacific/Auckland'
      };
      
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
      const utcDateString = dateString.endsWith('Z') ? dateString : dateString + 'Z';
      const date = new Date(utcDateString);
      return formatDistanceToNow(date, { addSuffix: true });
    } catch {
      return '';
    }
  };

  // Pagination calculations
  const totalPages = Math.ceil(expenses.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const paginatedExpenses = expenses.slice(startIndex, endIndex);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
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

  return (
    <>
      <Header />
      <div className="container">
        <div className="expense-list-container">
          <div className="expense-list-header">
            <h2 className="section-title">All Expenses</h2>
            <div className="expense-header-actions">
              <button 
                className="btn btn-outline"
                onClick={() => navigate('/dashboard')}
              >
                ← Back to Dashboard
              </button>
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
              <p>No expenses found</p>
              <p className="empty-subtitle">
                {selectedCategory !== 'All' 
                  ? `No expenses in ${selectedCategory} category`
                  : 'Add your first expense to get started!'}
              </p>
            </div>
          ) : (
            <div className="expense-list">
              {paginatedExpenses.map((expense) => (
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

          {/* Pagination */}
          {expenses.length > 0 && totalPages > 1 && (
            <div className="pagination">
              <button
                className="pagination-btn"
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
              >
                ← Previous
              </button>

              <div className="pagination-numbers">
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    className={`pagination-number ${currentPage === page ? 'active' : ''}`}
                    onClick={() => handlePageChange(page)}
                  >
                    {page}
                  </button>
                ))}
              </div>

              <button
                className="pagination-btn"
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
              >
                Next →
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default AllExpenses;