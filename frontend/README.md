# 💰 Expense Tracker Frontend

A minimalist, responsive expense tracking application built with React.

## ✨ Features

- 🔐 User authentication (Register/Login)
- ➕ Add, view, and delete expenses
- 📊 Real-time statistics and category breakdowns
- 🏷️ 8 predefined expense categories
- 🎨 Clean, minimalist UI
- 📱 Fully responsive (Desktop, Tablet, Mobile)
- 🔄 Real-time data synchronization with backend

## 🚀 Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. **Create React app:**
   ```bash
   npx create-react-app expense-tracker-frontend
   cd expense-tracker-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install react-router-dom date-fns lucide-react
   ```

3. **Create `.env` file in root:**
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Copy all source files** to their respective locations as indicated by the comments at the top of each file.

5. **Start the development server:**
   ```bash
   npm start
   ```

   The app will open at `http://localhost:3000`

## 📁 Project Structure

```
src/
├── components/
│   ├── Auth/
│   │   ├── Login.jsx
│   │   └── Register.jsx
│   ├── Dashboard/
│   │   ├── Dashboard.jsx
│   │   ├── ExpenseForm.jsx
│   │   ├── ExpenseList.jsx
│   │   └── Stats.jsx
│   └── Layout/
│       ├── Header.jsx
│       └── ProtectedRoute.jsx
├── hooks/
│   ├── useAuth.js
│   └── useExpenses.js
├── services/
│   └── api.js
├── utils/
│   └── constants.js
├── App.jsx
├── App.css
├── index.js
└── index.css
```

## 🎯 Usage

### Register/Login
1. Navigate to the app
2. Click "Sign up" to create a new account
3. After registration, you'll be automatically logged in
4. Or use "Sign in" if you already have an account

### Managing Expenses
1. **Add Expense:** Fill in amount, select category, add description (optional)
2. **View Expenses:** See all your expenses sorted by newest first
3. **Filter by Category:** Click category buttons to filter expenses
4. **Delete Expense:** Click the × button on any expense

### Statistics
- View total amount spent
- See total number of expenses
- Check spending breakdown by category

## 🎨 Customization

### Changing Categories
Edit `src/utils/constants.js`:
```javascript
export const CATEGORIES = [
  'Your Category 1',
  'Your Category 2',
  // ...
];
```

### Changing Colors
Edit color scheme in `src/index.css`:
```css
:root {
  --primary: #2563eb;
  --danger: #ef4444;
  /* ... */
}
```

## 🔧 Configuration

### Backend URL
Change in `.env`:
```env
REACT_APP_API_URL=https://your-production-api.com
```

### Port
Run on different port:
```bash
PORT=3001 npm start
```

## 📱 Responsive Breakpoints

- **Desktop:** > 768px
- **Tablet:** 481px - 768px
- **Mobile:** ≤ 480px

## 🐛 Troubleshooting

### CORS Error
Ensure backend allows `http://localhost:3000`:
```python
allow_origins=["http://localhost:3000"]
```

### Token Issues
- Check browser console for errors
- Verify token is stored in localStorage
- Clear localStorage and login again: `localStorage.clear()`

### Build Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📦 Building for Production

```bash
npm run build
```

Output will be in the `build/` folder.

## 🛠️ Tech Stack

- **React 18** - UI library
- **React Router 6** - Routing
- **date-fns** - Date formatting
- **lucide-react** - Icons (optional)
- **CSS3** - Styling

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Happy expense tracking! 💰**