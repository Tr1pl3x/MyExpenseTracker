// src/services/api.js

import { API_BASE_URL } from '../utils/constants';

class ExpenseAPI {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  getHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    };
  }

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers: { ...this.getHeaders(), ...options.headers },
      });

      if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
        throw new Error('Session expired. Please login again.');
      }

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'An error occurred');
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Auth methods
  async register(email, username, password) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, username, password }),
    });
  }

  async login(email, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    localStorage.setItem('token', data.access_token);
    return data;
  }

  async logout() {
    try {
      await this.request('/auth/logout', { method: 'POST' });
    } finally {
      localStorage.removeItem('token');
    }
  }

  // Expense methods
  async createExpense(amount, category, description) {
    return this.request('/expense/create_expense', {
      method: 'POST',
      body: JSON.stringify({ amount, category, description }),
    });
  }

  async listExpenses() {
    return this.request('/expense/list_expense');
  }

  async listExpensesByCategory(category) {
    return this.request(`/expense/list_expense_by_category?category=${encodeURIComponent(category)}`);
  }

  async deleteExpense(id) {
    return this.request(`/expense/delete_expense/${id}`, {
      method: 'DELETE',
    });
  }

  // Stats methods
  async getTotalStats() {
    return this.request('/stats/total');
  }

  async getStatsByCategory() {
    return this.request('/stats/total_by_category');
  }

  // Utility
  async getCategories() {
    const data = await this.request('/');
    return data.available_categories;
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!localStorage.getItem('token');
  }
}

export const api = new ExpenseAPI(API_BASE_URL);