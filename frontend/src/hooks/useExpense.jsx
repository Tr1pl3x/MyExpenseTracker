// src/hooks/useExpenses.js

import { useState, useEffect } from 'react';
import { api } from '../services/api';

export const useExpenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [stats, setStats] = useState(null);
  const [categoryStats, setCategoryStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchExpenses = async () => {
    try {
      setLoading(true);
      const data = await api.listExpenses();
      setExpenses(data.expenses);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const [total, byCategory] = await Promise.all([
        api.getTotalStats(),
        api.getStatsByCategory(),
      ]);
      setStats(total);
      setCategoryStats(byCategory);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  useEffect(() => {
    fetchExpenses();
    fetchStats();
  }, []);

  const addExpense = async (amount, category, description) => {
    try {
      const newExpense = await api.createExpense(amount, category, description);
      setExpenses([newExpense, ...expenses]);
      await fetchStats(); // Refresh stats
      return newExpense;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const removeExpense = async (id) => {
    try {
      await api.deleteExpense(id);
      setExpenses(expenses.filter(exp => exp.id !== id));
      await fetchStats(); // Refresh stats
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const filterByCategory = async (category) => {
    try {
      setLoading(true);
      const data = await api.listExpensesByCategory(category);
      setExpenses(data.expenses);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    expenses,
    stats,
    categoryStats,
    loading,
    error,
    addExpense,
    removeExpense,
    filterByCategory,
    refetch: fetchExpenses,
  };
};