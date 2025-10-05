// src/components/Dashboard/Stats.jsx

import React from 'react';
import { CATEGORY_COLORS, CATEGORY_EMOJI } from '../../utils/constants';

const Stats = ({ stats, categoryStats }) => {
  return (
    <div className="stats-container">
      <div className="total-stats">
        <div className="stat-card stat-card-total">
          <div className="stat-label">Total Spent</div>
          <div className="stat-value">${stats?.total_amount?.toFixed(2) || '0.00'}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Total Expenses</div>
          <div className="stat-value">{stats?.total_expenses || 0}</div>
        </div>
      </div>

      {categoryStats && categoryStats.length > 0 && (
        <div className="category-stats">
          <h3 className="section-title">By Category</h3>
          <div className="category-grid">
            {categoryStats.map((cat) => (
              <div 
                key={cat.category} 
                className="category-card"
                style={{ borderLeftColor: CATEGORY_COLORS[cat.category] }}
              >
                <div className="category-header">
                  <span className="category-emoji">{CATEGORY_EMOJI[cat.category]}</span>
                  <span className="category-name">{cat.category}</span>
                </div>
                <div className="category-amount">${cat.total_amount.toFixed(2)}</div>
                <div className="category-count">{cat.total_expenses} expense{cat.total_expenses !== 1 ? 's' : ''}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Stats;