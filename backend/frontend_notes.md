# 📱 Frontend Developer Guide - Expense Tracker API

A complete guide for frontend developers to integrate with the Expense Tracker API.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [API Base URL](#api-base-url)
- [Authentication Flow](#authentication-flow)
- [Available Endpoints](#available-endpoints)
- [Code Examples](#code-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Common Workflows](#common-workflows)
- [TypeScript Types](#typescript-types)

---

## 🚀 Quick Start

### What You Need to Know

1. **Base URL:** `http://localhost:8000` (development) or `https://your-api.vercel.app` (production)
2. **Authentication:** JWT Bearer token (get from `/auth/login`)
3. **Token Storage:** Store in localStorage, sessionStorage, or secure cookie
4. **Token Format:** `Authorization: Bearer <token>`
5. **Token Expiry:** 7 days

### Quick Integration Steps

1. User registers or logs in
2. Store the JWT token
3. Include token in all protected requests
4. Handle token expiration (401 errors)

---

## 🌐 API Base URL

```javascript
// config.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default API_BASE_URL;
```

---

## 🔐 Authentication Flow

### 1. User Registration

**Endpoint:** `POST /auth/register`

**Request:**
```javascript
const register = async (email, username, password) => {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      username,
      password,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
};
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2025-10-04T10:30:00.123456"
}
```

---

### 2. User Login

**Endpoint:** `POST /auth/login`

**Request:**
```javascript
const login = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  const data = await response.json();
  
  // Store token in localStorage
  localStorage.setItem('token', data.access_token);
  
  return data;
};
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Important:** Save the `access_token` - you'll need it for all protected routes!

---

### 3. Using the Token

**Always include the token in protected requests:**

```javascript
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

// Example usage
const fetchProtectedData = async () => {
  const response = await fetch(`${API_BASE_URL}/expense/list_expense`, {
    headers: getAuthHeaders(),
  });
  return await response.json();
};
```

---

### 4. Logout

**Endpoint:** `POST /auth/logout`

**Request:**
```javascript
const logout = async () => {
  const response = await fetch(`${API_BASE_URL}/auth/logout`, {
    method: 'POST',
    headers: getAuthHeaders(),
  });

  // Clear token from localStorage
  localStorage.removeItem('token');
  
  return await response.json();
};
```

---

## 📚 Available Endpoints

### Public Endpoints (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get API info & categories |
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get token |

### Protected Endpoints (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/logout` | Logout user |
| POST | `/expense/create_expense` | Create expense |
| DELETE | `/expense/delete_expense/{id}` | Delete expense |
| GET | `/expense/list_expense` | List all expenses (sorted newest first) |
| GET | `/expense/list_expense_by_category?category=Food` | List expenses by category |
| GET | `/stats/total` | Get total statistics |
| GET | `/stats/total_by_category` | Get category breakdown |

---

## 💻 Code Examples

### Get Available Categories

```javascript
const getCategories = async () => {
  const response = await fetch(`${API_BASE_URL}/`);
  const data = await response.json();
  return data.available_categories;
};

// Usage in React
useEffect(() => {
  getCategories().then(categories => {
    setCategories(categories);
  });
}, []);
```

**Response:**
```json
{
  "message": "Expense Tracker API",
  "available_categories": ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Healthcare", "Education", "Others"]
}
```

---

### Create Expense

```javascript
const createExpense = async (amount, category, description) => {
  const response = await fetch(`${API_BASE_URL}/expense/create_expense`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({
      amount: parseFloat(amount),
      category,
      description,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
};
```

**Request Body:**
```json
{
  "amount": 50.00,
  "category": "Food",
  "description": "Lunch at restaurant"
}
```

**Response:**
```json
{
  "id": 15,
  "user_id": 1,
  "amount": 50.0,
  "category": "Food",
  "description": "Lunch at restaurant",
  "date": "2025-10-04T14:23:45.123456"
}
```

---

### List All Expenses

```javascript
const listExpenses = async () => {
  const response = await fetch(`${API_BASE_URL}/expense/list_expense`, {
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch expenses');
  }

  return await response.json();
};
```

**Response:**
```json
{
  "expenses": [
    {
      "id": 18,
      "user_id": 1,
      "amount": 100.0,
      "category": "Shopping",
      "description": "New shoes",
      "date": "2025-10-04T15:30:00.123456"
    },
    {
      "id": 17,
      "user_id": 1,
      "amount": 25.50,
      "category": "Food",
      "description": "Dinner",
      "date": "2025-10-04T14:20:00.123456"
    }
  ],
  "count": 2
}
```

**Note:** Expenses are automatically sorted by date (newest first)!

---

### List Expenses by Category

```javascript
const listExpensesByCategory = async (category) => {
  const response = await fetch(
    `${API_BASE_URL}/expense/list_expense_by_category?category=${category}`,
    {
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
};

// Usage
listExpensesByCategory('Food').then(data => {
  console.log(data.expenses);
  console.log(`Total: ${data.count}`);
});
```

---

### Delete Expense

```javascript
const deleteExpense = async (expenseId) => {
  const response = await fetch(
    `${API_BASE_URL}/expense/delete_expense/${expenseId}`,
    {
      method: 'DELETE',
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
};
```

**Response:**
```json
{
  "message": "Expense deleted successfully"
}
```

---

### Get Total Statistics

```javascript
const getTotalStats = async () => {
  const response = await fetch(`${API_BASE_URL}/stats/total`, {
    headers: getAuthHeaders(),
  });

  return await response.json();
};
```

**Response:**
```json
{
  "total_amount": 1250.75,
  "total_expenses": 15
}
```

---

### Get Statistics by Category

```javascript
const getStatsByCategory = async () => {
  const response = await fetch(`${API_BASE_URL}/stats/total_by_category`, {
    headers: getAuthHeaders(),
  });

  return await response.json();
};
```

**Response:**
```json
[
  {
    "category": "Food",
    "total_amount": 450.50,
    "total_expenses": 12
  },
  {
    "category": "Transport",
    "total_amount": 200.00,
    "total_expenses": 8
  }
]
```

---

## 🚨 Error Handling

### Common Errors

**401 Unauthorized - Token Invalid/Expired:**
```javascript
const handleResponse = async (response) => {
  if (response.status === 401) {
    // Token expired or invalid
    localStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Session expired. Please login again.');
  }

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'An error occurred');
  }

  return await response.json();
};
```

**400 Bad Request - Invalid Category:**
```javascript
try {
  await createExpense(50, 'InvalidCategory', 'Test');
} catch (error) {
  // Error: Invalid category. Must be one of: Food, Transport, ...
  console.error(error.message);
}
```

**422 Validation Error:**
```javascript
try {
  await createExpense(-50, 'Food', 'Test'); // Negative amount
} catch (error) {
  // Handle validation error
  console.error('Validation failed:', error);
}
```

### Error Handling Wrapper

```javascript
const apiRequest = async (url, options = {}) => {
  try {
    const response = await fetch(url, options);
    
    if (response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      throw new Error('Session expired');
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
```

---

## ✅ Best Practices

### 1. Token Management

```javascript
// Check if user is authenticated
const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};

// Protected route guard (React Router example)
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" />;
  }
  return children;
};
```

### 2. Centralized API Service

```javascript
// api.js
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
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: { ...this.getHeaders(), ...options.headers },
    });

    if (response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return await response.json();
  }

  // Auth methods
  register(email, username, password) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, username, password }),
    });
  }

  login(email, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }).then(data => {
      localStorage.setItem('token', data.access_token);
      return data;
    });
  }

  logout() {
    return this.request('/auth/logout', { method: 'POST' })
      .then(() => localStorage.removeItem('token'));
  }

  // Expense methods
  createExpense(amount, category, description) {
    return this.request('/expense/create_expense', {
      method: 'POST',
      body: JSON.stringify({ amount, category, description }),
    });
  }

  listExpenses() {
    return this.request('/expense/list_expense');
  }

  listExpensesByCategory(category) {
    return this.request(`/expense/list_expense_by_category?category=${category}`);
  }

  deleteExpense(id) {
    return this.request(`/expense/delete_expense/${id}`, {
      method: 'DELETE',
    });
  }

  // Stats methods
  getTotalStats() {
    return this.request('/stats/total');
  }

  getStatsByCategory() {
    return this.request('/stats/total_by_category');
  }

  // Utility
  getCategories() {
    return this.request('/').then(data => data.available_categories);
  }
}

export const api = new ExpenseAPI(API_BASE_URL);
```

**Usage:**
```javascript
import { api } from './api';

// Login
await api.login('user@example.com', 'password123');

// Create expense
await api.createExpense(50, 'Food', 'Lunch');

// List expenses
const { expenses } = await api.listExpenses();
```

### 3. React Hook Example

```javascript
// useExpenses.js
import { useState, useEffect } from 'react';
import { api } from './api';

export const useExpenses = () => {
  const [expenses, setExpenses] = useState([]);
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

  useEffect(() => {
    fetchExpenses();
  }, []);

  const addExpense = async (amount, category, description) => {
    try {
      const newExpense = await api.createExpense(amount, category, description);
      setExpenses([newExpense, ...expenses]); // Add to beginning (newest first)
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
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  return {
    expenses,
    loading,
    error,
    addExpense,
    removeExpense,
    refetch: fetchExpenses,
  };
};

// Usage in component
const ExpenseList = () => {
  const { expenses, loading, error, addExpense, removeExpense } = useExpenses();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {expenses.map(expense => (
        <div key={expense.id}>
          <span>{expense.description} - ${expense.amount}</span>
          <button onClick={() => removeExpense(expense.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
};
```

---

## 🔄 Common Workflows

### Workflow 1: User Registration & Login

```javascript
// 1. Register
const handleRegister = async (email, username, password) => {
  try {
    await api.register(email, username, password);
    
    // 2. Auto-login after registration
    await api.login(email, password);
    
    // 3. Redirect to dashboard
    navigate('/dashboard');
  } catch (error) {
    showError(error.message);
  }
};
```

### Workflow 2: Create Expense & Refresh List

```javascript
const handleCreateExpense = async (formData) => {
  try {
    // Create expense
    await api.createExpense(
      formData.amount,
      formData.category,
      formData.description
    );

    // Refresh expenses list (already sorted by backend)
    const { expenses } = await api.listExpenses();
    setExpenses(expenses);

    // Clear form
    resetForm();
  } catch (error) {
    showError(error.message);
  }
};
```

### Workflow 3: Dashboard Statistics

```javascript
const DashboardStats = () => {
  const [stats, setStats] = useState(null);
  const [categoryStats, setCategoryStats] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      const [total, byCategory] = await Promise.all([
        api.getTotalStats(),
        api.getStatsByCategory(),
      ]);

      setStats(total);
      setCategoryStats(byCategory);
    };

    fetchStats();
  }, []);

  return (
    <div>
      <h2>Total Spent: ${stats?.total_amount}</h2>
      <h3>Total Expenses: {stats?.total_expenses}</h3>

      <h3>By Category:</h3>
      {categoryStats.map(cat => (
        <div key={cat.category}>
          {cat.category}: ${cat.total_amount} ({cat.total_expenses} expenses)
        </div>
      ))}
    </div>
  );
};
```

### Workflow 4: Category Filter

```javascript
const ExpensesByCategory = () => {
  const [category, setCategory] = useState('Food');
  const [expenses, setExpenses] = useState([]);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    api.getCategories().then(setCategories);
  }, []);

  useEffect(() => {
    api.listExpensesByCategory(category)
      .then(data => setExpenses(data.expenses));
  }, [category]);

  return (
    <div>
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        {categories.map(cat => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>

      <div>
        {expenses.map(expense => (
          <div key={expense.id}>{expense.description} - ${expense.amount}</div>
        ))}
      </div>
    </div>
  );
};
```

---

## 📝 TypeScript Types

```typescript
// types.ts

export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface Expense {
  id: number;
  user_id: number;
  amount: number;
  category: string;
  description: string | null;
  date: string;
}

export interface ExpenseListResponse {
  expenses: Expense[];
  count: number;
}

export interface TotalStats {
  total_amount: number;
  total_expenses: number;
}

export interface CategoryStats {
  category: string;
  total_amount: number;
  total_expenses: number;
}

export interface ApiResponse {
  message: string;
  available_categories: string[];
}

export type Category = 
  | 'Food'
  | 'Transport'
  | 'Entertainment'
  | 'Shopping'
  | 'Bills'
  | 'Healthcare'
  | 'Education'
  | 'Others';

export interface CreateExpenseRequest {
  amount: number;
  category: Category;
  description?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}
```

**Usage:**
```typescript
import { api } from './api';
import { Expense, CreateExpenseRequest } from './types';

const createExpense = async (data: CreateExpenseRequest): Promise<Expense> => {
  return await api.createExpense(data.amount, data.category, data.description);
};
```

---

## 🎯 Quick Reference

### Valid Categories (Case-Sensitive!)

```javascript
const CATEGORIES = [
  'Food',
  'Transport',
  'Entertainment',
  'Shopping',
  'Bills',
  'Healthcare',
  'Education',
  'Others'
];
```

### Date Handling

All dates from the API are in **UTC ISO 8601 format**: `2025-10-04T14:23:45.123456`

```javascript
// Convert to local date
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

// Convert to local datetime
const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString();
};

// Example
const expense = { date: "2025-10-04T14:23:45.123456" };
console.log(formatDateTime(expense.date)); // "10/4/2025, 2:23:45 PM"
```

### Sorting

Expenses are **already sorted by the backend** in descending order (newest first). No need to sort on frontend!

```javascript
// Backend already returns sorted
const { expenses } = await api.listExpenses();
// expenses[0] is the newest expense
```

---

## 🔒 Security Considerations

1. **HTTPS Only in Production:** Always use HTTPS URLs in production
2. **Token Storage:** Consider using httpOnly cookies for better security
3. **Token Expiry:** Handle 401 errors gracefully and redirect to login
4. **Input Validation:** Validate user input before sending to API
5. **CORS:** Ensure your domain is whitelisted in backend CORS settings

### Example: Secure Token Storage with HttpOnly Cookie

```javascript
// If backend supports cookie-based auth
const loginWithCookie = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    credentials: 'include', // Include cookies
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  return await response.json();
};
```

---

## 📦 Complete Example: Expense Form Component

```javascript
import { useState } from 'react';
import { api } from './api';

const ExpenseForm = ({ onExpenseCreated }) => {
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('Food');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const CATEGORIES = [
    'Food', 'Transport', 'Entertainment', 'Shopping',
    'Bills', 'Healthcare', 'Education', 'Others'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const expense = await api.createExpense(
        parseFloat(amount),
        category,
        description
      );

      // Clear form
      setAmount('');
      setDescription('');
      
      // Notify parent
      onExpenseCreated(expense);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="number"
        step="0.01"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
        min="0.01"
      />

      <select 
        value={category} 
        onChange={(e) => setCategory(e.target.value)}
        required
      >
        {CATEGORIES.map(cat => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Add Expense'}
      </button>

      {error && <div className="error">{error}</div>}
    </form>
  );
};

export default ExpenseForm;
```

---

## 🐛 Debugging Tips

### 1. Check Token

```javascript
const debugToken = () => {
  const token = localStorage.getItem('token');
  console.log('Token exists:', !!token);
  console.log('Token:', token?.substring(0, 20) + '...');
};
```

### 2. Log API Requests

```javascript
const apiRequest = async (url, options) => {
  console.log('API Request:', url, options);
  
  const response = await fetch(url, options);
  
  console.log('API Response:', response.status, response.statusText);
  
  const data = await response.json();
  console.log('API Data:', data);
  
  return data;
};
```

### 3. Network Tab

- Open browser DevTools → Network tab
- Filter by "Fetch/XHR"
- Check request headers (Authorization header should be present)
- Check response status and body

---

## 📞 Need Help?

- Check API docs at `/docs` endpoint
- Verify token is being sent in Authorization header
- Ensure category names match exactly (case-sensitive)
- Check browser console for errors
- Verify API base URL is correct

---

**Happy Coding! 🚀**