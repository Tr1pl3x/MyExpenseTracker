# 💰 Expense Tracker - Full Stack Application

A complete full-stack expense tracking application with a React frontend and FastAPI backend, featuring user authentication, expense management, and real-time analytics.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [API Documentation](#api-documentation)
- [Frontend Usage](#frontend-usage)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

A modern, full-stack expense tracking solution that allows users to manage their personal expenses with authentication, categorization, and analytics. The application features a minimalist React frontend and a serverless FastAPI backend deployed on Vercel with Neon PostgreSQL.

### Live Demo
- **Frontend:** `https://my-expense-tracker-iojs.vercel.app/`
- **Backend API:** `https://my-expense-tracker-rho.vercel.app/`
- **API Docs:** `https://my-expense-tracker-rho.vercel.app/docs`

---

## ✨ Features

### Core Functionality
- 🔐 **JWT-based Authentication** - Secure user registration and login
- ➕ **Expense Management** - Create, view, and delete expenses
- 📊 **Real-time Analytics** - Total spending and category breakdowns
- 🏷️ **8 Predefined Categories** - Food, Transport, Entertainment, Shopping, Bills, Healthcare, Education, Others
- ⏰ **Automatic Timestamps** - Track when expenses were created
- 🔒 **Data Isolation** - Users can only access their own expenses

### User Experience
- 🎨 **Clean, Minimalist UI** - Focus on functionality
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- 🔄 **Real-time Sync** - Instant updates between frontend and backend
- 🚀 **Fast & Serverless** - Quick load times with serverless architecture

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **React Router 6** - Client-side routing
- **date-fns** - Date formatting
- **lucide-react** - Icon library
- **CSS3** - Modern styling

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL (Neon)** - Cloud database
- **JWT** - Token-based authentication
- **bcrypt** - Password hashing
- **Uvicorn** - ASGI server

### Deployment
- **Vercel** - Serverless deployment (both frontend & backend)
- **Neon** - Serverless PostgreSQL database

---

## 📁 Project Structure

```
expense-tracker/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py              # Database models
│   ├── database.py            # DB configuration
│   ├── schemas.py             # Pydantic schemas
│   ├── auth.py                # Auth utilities
│   ├── requirements.txt       # Python dependencies
│   ├── vercel.json           # Vercel config
│   ├── .env                  # Environment variables
│   ├── test_api.py           # API tests
│   └── README.md             # Backend docs
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Register.jsx
│   │   │   ├── Dashboard/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── ExpenseForm.jsx
│   │   │   │   ├── ExpenseList.jsx
│   │   │   │   └── Stats.jsx
│   │   │   └── Layout/
│   │   │       ├── Header.jsx
│   │   │       └── ProtectedRoute.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   └── useExpenses.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── utils/
│   │   │   └── constants.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── .env
│   └── README.md             # Frontend docs
│
└── README.md                 # This file
```

---

## 📋 Prerequisites

### Required Software
- **Node.js** v16 or higher ([Download](https://nodejs.org/))
- **Python** 3.9+ ([Download](https://www.python.org/))
- **npm** or **yarn** (comes with Node.js)
- **Git** ([Download](https://git-scm.com/))

### Required Accounts
- **Neon PostgreSQL** account ([Sign up](https://neon.tech/))
- **Vercel** account for deployment ([Sign up](https://vercel.com/))

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

#### Configure Environment

Create `backend/.env`:

```env
DATABASE_URL=postgresql://username:password@host/database?sslmode=require
SECRET_KEY=your-super-secret-key-here
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Run Backend

```bash
uvicorn main:app --reload
```

Backend will run at `http://localhost:8000`  
API docs available at `http://localhost:8000/docs`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend

# Install packages
npm install
```

#### Configure Environment

Create `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000
```

#### Run Frontend

```bash
npm start
```

Frontend will run at `http://localhost:3000`

---

## 📚 API Documentation

### Base URL
- **Local:** `http://localhost:8000`
- **Production:** `https://your-backend.vercel.app`

### Available Endpoints

#### Authentication (No Auth Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get API info & categories |
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get JWT token |

#### Expenses (Auth Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expense/create_expense` | Create new expense |
| GET | `/expense/list_expense` | List all user's expenses |
| GET | `/expense/list_expense_by_category` | Filter by category |
| DELETE | `/expense/delete_expense/{id}` | Delete expense |

#### Statistics (Auth Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stats/total` | Get total spending stats |
| GET | `/stats/total_by_category` | Get breakdown by category |

### Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

**Token Lifetime:** 7 days

### Example Request

```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123"
  }'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'

# Create Expense
curl -X POST "http://localhost:8000/expense/create_expense" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "category": "Food",
    "description": "Lunch"
  }'
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints.

---

## 🎯 Frontend Usage

### Getting Started

1. **Register an Account**
   - Click "Sign up"
   - Enter email, username, and password
   - You'll be automatically logged in

2. **Add Your First Expense**
   - Enter amount (must be greater than 0)
   - Select a category from the dropdown
   - Add an optional description
   - Click "Add Expense"

3. **View Your Expenses**
   - All expenses are displayed sorted by newest first
   - Click category buttons to filter by category
   - See real-time statistics at the top

4. **Manage Expenses**
   - Click the × button to delete an expense
   - Changes are reflected immediately

### Available Categories

- Food
- Transport
- Entertainment
- Shopping
- Bills
- Healthcare
- Education
- Others

### Responsive Design

The app automatically adapts to your screen size:
- **Desktop:** > 768px - Full layout with side-by-side views
- **Tablet:** 481px - 768px - Stacked layout
- **Mobile:** ≤ 480px - Optimized for touch

---

## 🚀 Deployment

### Backend Deployment (Vercel)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy from backend directory:**
   ```bash
   cd backend
   vercel
   ```

4. **Set Environment Variables:**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add:
     - `DATABASE_URL` (from Neon)
     - `SECRET_KEY` (generated secure key)

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

### Frontend Deployment (Vercel)

1. **Deploy from frontend directory:**
   ```bash
   cd frontend
   vercel
   ```

2. **Set Environment Variable:**
   - Add `REACT_APP_API_URL` with your production backend URL
   - Example: `https://your-backend.vercel.app`

3. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

### Post-Deployment

1. Update CORS settings in backend to allow your frontend URL
2. Test all functionality in production
3. Update README with your production URLs

---

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Using test script
python test_api.py

# Using interactive docs
# Visit http://localhost:8000/docs
```

### Frontend Testing

```bash
cd frontend

# Run development server
npm start

# Build for production (test build)
npm run build
```

### Testing Checklist

- ✅ User registration
- ✅ User login
- ✅ Create expenses (all categories)
- ✅ View all expenses
- ✅ Filter by category
- ✅ View statistics
- ✅ Delete expenses
- ✅ Logout
- ✅ Token expiration handling
- ✅ Error handling
- ✅ Responsive design (mobile, tablet, desktop)

---

## 🐛 Troubleshooting

### Common Backend Issues

**Database Connection Error:**
```
ValueError: DATABASE_URL environment variable is not set
```
**Fix:** Create `.env` file with valid `DATABASE_URL` from Neon

**bcrypt Error:**
```
AttributeError: module 'bcrypt' has no attribute '__about__'
```
**Fix:**
```bash
pip uninstall bcrypt -y
pip install bcrypt==4.0.1
```

**401 Unauthorized:**
- Token expired (7 days limit) - login again
- Token format wrong - must be `Bearer <token>`
- Token missing in Authorization header

**400 Invalid Category:**
- Check spelling and capitalization
- Valid: `Food`, Invalid: `food`

### Common Frontend Issues

**CORS Error:**
```
Access to fetch has been blocked by CORS policy
```
**Fix:** Ensure backend CORS settings allow your frontend URL

**Token Issues:**
- Open browser console for error details
- Check if token exists: `localStorage.getItem('token')`
- Clear and re-login: `localStorage.clear()`

**Build Issues:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Connection Refused:**
- Verify backend is running on correct port
- Check `.env` file has correct `REACT_APP_API_URL`
- Ensure no firewall blocking connections

### General Issues

**"Cannot find module" errors:**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

**Port Already in Use:**
```bash
# Backend - use different port
uvicorn main:app --reload --port 8001

# Frontend - use different port
PORT=3001 npm start
```

---

## 🔒 Security Best Practices

### Development
- Never commit `.env` files
- Use strong passwords for testing
- Keep dependencies updated

### Production
- Use strong, random `SECRET_KEY`
- Enable HTTPS only
- Use environment variables for all secrets
- Regularly update dependencies
- Monitor logs for suspicious activity
- Set appropriate CORS origins
- Use strong password requirements
- Implement rate limiting (recommended)

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

- **Backend Documentation:** See `backend/README.md`
- **Frontend Documentation:** See `frontend/README.md`
- **API Documentation:** Visit `/docs` endpoint on your backend
- **Issues:** Open an issue on GitHub

---

## 🎯 Quick Start Commands

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start
```

Then visit:
- **Frontend:** `https://my-expense-tracker-iojs.vercel.app/`
- **Backend API:** `https://my-expense-tracker-rho.vercel.app/`
- **API Docs:** `https://my-expense-tracker-rho.vercel.app/docs`
---

**Happy expense tracking! 💰**

Made with ❤️ using React and FastAPI