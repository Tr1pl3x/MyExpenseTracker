# 💰 Expense Tracker API - Complete Documentation

A serverless FastAPI backend for tracking personal expenses with user authentication and analytics, deployable on Vercel with Neon PostgreSQL database.

## 📋 Table of Contents

- [Features](#features)
- [Default Categories](#default-categories)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [API Routes Documentation](#api-routes-documentation)
  - [Root Endpoint](#root-endpoint)
  - [Authentication Routes](#authentication-routes)
  - [Expense Routes](#expense-routes)
  - [Statistics Routes](#statistics-routes)
- [Error Responses](#error-responses)
- [Testing](#testing)
- [Deployment](#deployment)

---

## ✨ Features

- 🔐 JWT-based user authentication
- 💵 Create, read, and delete expenses
- 📊 Expense analytics and statistics
- 🏷️ Predefined expense categories
- ⏰ Automatic timestamp tracking (date + time)
- 🔒 User-specific data isolation
- 🚀 Serverless deployment ready (Vercel)
- 🐘 PostgreSQL database support (Neon)

---

## 🏷️ Default Categories

Users can only use these predefined categories:

- `Food`
- `Transport`
- `Entertainment`
- `Shopping`
- `Bills`
- `Healthcare`
- `Education`
- `Others`

---

## 📁 Project Structure

```
expense-tracker-backend/
├── main.py                 # Main FastAPI application
├── models.py              # SQLAlchemy database models
├── database.py            # Database configuration
├── schemas.py             # Pydantic schemas
├── auth.py                # Authentication utilities
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── .env                  # Environment variables
├── .gitignore            # Git ignore file
├── test_api.py           # Testing script
└── README.md             # This file
```

---

## 🚀 Setup & Installation

### 1. Prerequisites

- Python 3.9+
- Neon PostgreSQL database account
- pip and virtualenv

### 2. Installation Steps

```bash
# Clone or create project directory
mkdir expense-tracker-backend
cd expense-tracker-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@host/database?sslmode=require
SECRET_KEY=your-super-secret-key-here
```

Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Run Locally

```bash
uvicorn main:app --reload
```

API will be available at: `http://localhost:8000`

Interactive docs at: `http://localhost:8000/docs`

---

## 📚 API Routes Documentation

Base URL (local): `http://localhost:8000`

---

## 🏠 Root Endpoint

### Get API Information

**Endpoint:** `GET /`

**Description:** Get basic API information and available expense categories.

**Authentication Required:** ❌ No

**Request Headers:** None

**Query Parameters:** None

**Request Body:** None

**Success Response (200):**
```json
{
  "message": "Expense Tracker API",
  "available_categories": [
    "Food",
    "Transport",
    "Entertainment",
    "Shopping",
    "Bills",
    "Healthcare",
    "Education",
    "Others"
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| message | string | API name/welcome message |
| available_categories | array | List of all valid expense categories |

**Use Case:** 
- Check if API is running
- Get list of valid categories for dropdowns/selects
- Health check endpoint

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/"
```

**JavaScript Example:**
```javascript
fetch('http://localhost:8000/')
  .then(response => response.json())
  .then(data => {
    console.log('API:', data.message);
    console.log('Categories:', data.available_categories);
  });
```

**Note:** This is a public endpoint that doesn't require authentication. It's useful for:
- Verifying the API is online
- Fetching the list of valid categories for your frontend
- API health monitoring

---

## 🔐 Authentication Routes

### 1. Register User

**Endpoint:** `POST /auth/register`

**Description:** Create a new user account.

**Authentication Required:** ❌ No

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Request Parameters:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| email | string | ✅ Yes | Valid email format |
| username | string | ✅ Yes | 3-50 characters |
| password | string | ✅ Yes | Minimum 6 characters |

**Success Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2025-10-04T10:30:00.123456"
}
```

**Error Responses:**

- **400 Bad Request** - Email already registered
```json
{
  "detail": "Email already registered"
}
```

- **422 Validation Error** - Invalid input
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

---

### 2. Login

**Endpoint:** `POST /auth/login`

**Description:** Authenticate user and receive JWT access token.

**Authentication Required:** ❌ No

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | ✅ Yes | User's email |
| password | string | ✅ Yes | User's password |

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token Details:**
- Token expires in 7 days
- Use in Authorization header: `Bearer <token>`

**Error Responses:**

- **401 Unauthorized** - Invalid credentials
```json
{
  "detail": "Incorrect email or password"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

---

### 3. Logout

**Endpoint:** `POST /auth/logout`

**Description:** Logout user (client-side token removal).

**Authentication Required:** ✅ Yes

**Request Headers:**
```
Authorization: Bearer <your_access_token>
```

**Request Body:** None

**Success Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

**Note:** With JWT, logout is handled client-side by deleting the token. This endpoint confirms the action.

**Error Responses:**

- **401 Unauthorized** - Invalid or missing token
```json
{
  "detail": "Invalid authentication credentials"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/auth/logout" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 💵 Expense Routes

### 4. Create Expense

**Endpoint:** `POST /expense/create_expense`

**Description:** Create a new expense entry with automatic timestamp.

**Authentication Required:** ✅ Yes

**Request Headers:**
```
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "amount": 50.00,
  "category": "Food",
  "description": "Lunch at Italian restaurant"
}
```

**Request Parameters:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| amount | float | ✅ Yes | Must be > 0 |
| category | string | ✅ Yes | One of the default categories |
| description | string | ❌ No | Optional note about expense |

**Success Response (200):**
```json
{
  "id": 15,
  "user_id": 1,
  "amount": 50.0,
  "category": "Food",
  "description": "Lunch at Italian restaurant",
  "date": "2025-10-04T14:23:45.123456"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique expense ID |
| user_id | integer | ID of the user who created it |
| amount | float | Expense amount |
| category | string | Expense category |
| description | string/null | Optional description |
| date | datetime | Creation timestamp (UTC) |

**Error Responses:**

- **400 Bad Request** - Invalid category
```json
{
  "detail": "Invalid category. Must be one of: Food, Transport, Entertainment, Shopping, Bills, Healthcare, Education, Others"
}
```

- **401 Unauthorized** - Invalid or missing token
```json
{
  "detail": "Invalid authentication credentials"
}
```

- **422 Validation Error** - Invalid amount
```json
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/expense/create_expense" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "category": "Food",
    "description": "Lunch at Italian restaurant"
  }'
```

---

### 5. Delete Expense

**Endpoint:** `DELETE /expense/delete_expense/{expense_id}`

**Description:** Delete a specific expense by ID (only if it belongs to the authenticated user).

**Authentication Required:** ✅ Yes

**Request Headers:**
```
Authorization: Bearer <your_access_token>
```

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| expense_id | integer | ✅ Yes | ID of expense to delete |

**Request Body:** None

**Success Response (200):**
```json
{
  "message": "Expense deleted successfully"
}
```

**Error Responses:**

- **404 Not Found** - Expense doesn't exist or doesn't belong to user
```json
{
  "detail": "Expense not found"
}
```

- **401 Unauthorized** - Invalid or missing token
```json
{
  "detail": "Invalid authentication credentials"
}
```

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/expense/delete_expense/15" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 6. List All Expenses

**Endpoint:** `GET /expense/list_expense`

**Description:** Get all expenses for the authenticated user, sorted by date (newest first).

**Authentication Required:** ✅ Yes

**Request Headers:**
```
Authorization: Bearer <your_access_token>
```

**Query Parameters:** None

**Success Response (200):**
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
    },
    {
      "id": 15,
      "user_id": 1,
      "amount": 50.0,
      "category": "Food",
      "description": "Lunch",
      "date": "2025-10-04T12:00:00.123456"
    }
  ],
  "count": 3
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| expenses | array | List of expense objects |
| count | integer | Total number of expenses |

**Note:** Expenses are automatically sorted by date in **descending order** (latest first).

**Error Responses:**

- **401 Unauthorized** - Invalid or missing token
```json
{
  "detail": "Invalid authentication credentials"
}
```

**Empty Response (no expenses):**
```json
{
  "expenses": [],
  "count": 0
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/expense/list_expense" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 7. List Expenses by Category

**Endpoint:** `GET /expense/list_expense_by_category`

**Description:** Get all expenses for a specific category, sorted by date (newest first).

**Authentication Required:** ✅ Yes

**Request Headers:**
```
Authorization: Bearer <your_access_token>
```

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| category | string | ✅ Yes | One of the default categories |

**Success Response (200):**
```json
{
  "expenses": [
    {
      "id": 17,
      "user_id": 1,
      "amount": 25.50,
      "category": "Food",
      "description": "Dinner at Thai restaurant",
      "date": "2025-10-04T19:30:00.123456"
    },
    {
      "id": 15,
      "user_id": 1,
      "amount": 50.0,
      "category": "Food",
      "description": "Lunch at Italian restaurant",
      "date": "2025-10-04T12:00:00.123456"
    }
  ],
  "count": 2
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| expenses | array | List of expense objects in that category |
| count | integer | Total number of expenses in that category |

**Note:** Results are sorted by date in **descending order** (latest first).

**Error Responses:**

- **400 Bad Request** - Invalid category
```json
{
  "detail": "Invalid category. Must be one of: Food, Transport, Entertainment, Shopping, Bills, Healthcare, Education, Others"
}
```

- **401 Unauthorized** - Invalid or missing token
```json
{
  "detail": "Invalid authentication credentials"
}
```

**Empty Response (no expenses in category):**
```json
{
  "expenses": [],
  "count": 0
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/expense/list_expense_by_category?category=Food" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 Statistics Routes

### 8. Get Total Statistics

**Endpoint:** `GET /stats/total`

**Description:** Get total amount spent and total number of expenses for the authenticated user.

**Authentication Required:** ✅ Yes

**Request Headers:**
```
Authorization: Bearer <your_access_token>
```

**Query Parameters:** None

**Success Response (200):**
```json
{
  "total_amount": 1250.75,
  "total_expenses": 15
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| total_amount | float | Sum of all expense amounts |
| total_expenses | integer | Total count of expenses |

**Error Responses:**

- **401 Unauthorized** - Invalid or missing token
```json
{
  "detail": "Invalid authentication credentials"
}
```

**No Expenses Response:**
```json
{
  "total_amount": 0,
  "total_expenses": 0
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/stats/total" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 9. Get Statistics by Category

**Endpoint:** `GET /stats/total_by_category`

**Description:** Get spending breakdown by category with totals and counts.

**Authentication Required:** ✅ Yes

**Request Headers:**
```
Authorization: Bearer <your_access_token>
```

**Query Parameters:** None

**Success Response (200):**
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
  },
  {
    "category": "Shopping",
    "total_amount": 350.25,
    "total_expenses": 5
  },
  {
    "category": "Bills",
    "total_amount": 250.00,
    "total_expenses": 3
  }
]
```

**Response:** Array of category statistics

**Each Category Object:**

| Field | Type | Description |
|-------|------|-------------|
| category | string | Category name |
| total_amount | float | Total spent in this category |
| total_expenses | integer | Number of expenses in this category |

**Note:** Only categories with expenses are included in the response.

**Error Responses:**

- **401 Unauthorized** - Invalid or missing token
```json
{
  "detail": "Invalid authentication credentials"
}
```

**No Expenses Response:**
```json
[]
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/stats/total_by_category" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## ⚠️ Error Responses

### Common HTTP Status Codes

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid data (wrong category, invalid format) |
| 401 | Unauthorized | Missing/invalid token, wrong credentials |
| 404 | Not Found | Expense doesn't exist or doesn't belong to user |
| 422 | Validation Error | Request body doesn't match schema |
| 500 | Internal Server Error | Server-side error (database, etc.) |

### Error Response Format

All errors follow this structure:

```json
{
  "detail": "Error message description"
}
```

Or for validation errors:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error description",
      "type": "error_type"
    }
  ]
}
```

---

## 🧪 Testing

### Using Interactive API Docs (Recommended)

1. Start server:
   ```bash
   uvicorn main:app --reload
   ```

2. Open browser:
   ```
   http://localhost:8000/docs
   ```

3. Test flow:
   - Register → Login → Get Token
   - Click "Authorize" button (🔒)
   - Paste token
   - Test all endpoints

### Using Test Script

```bash
python test_api.py
```

### Using cURL

See cURL examples in each route section above.

### Testing Checklist

- ✅ Check API is running (GET /)
- ✅ Register new user
- ✅ Login and receive token
- ✅ Create expenses with different categories
- ✅ List all expenses (check descending order)
- ✅ List expenses by category
- ✅ Get total statistics
- ✅ Get category statistics
- ✅ Delete an expense
- ✅ Try invalid category (should fail)
- ✅ Try without token (should fail with 401)
- ✅ Try with invalid token (should fail with 401)

---

## 🚀 Deployment to Vercel

### Prerequisites

- Vercel account
- Vercel CLI installed: `npm install -g vercel`

### Deployment Steps

1. **Login to Vercel:**
   ```bash
   vercel login
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Set Environment Variables in Vercel Dashboard:**
   - Go to Project Settings
   - Environment Variables
   - Add:
     - `DATABASE_URL`: Your Neon connection string
     - `SECRET_KEY`: Your JWT secret key

4. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

### Post-Deployment

Your API will be available at: `https://your-project.vercel.app`

Update `BASE_URL` in `test_api.py` to test production:
```python
BASE_URL = "https://your-project.vercel.app"
```

---

## 📝 Notes

### Important Points

1. **Authentication:**
   - All expense and stats routes require authentication
   - Token expires after 7 days
   - Include token in Authorization header: `Bearer <token>`

2. **Timestamps:**
   - All expenses include full datetime (date + time)
   - Timestamps are in UTC
   - Automatically added on creation

3. **Ordering:**
   - Expenses are always returned in descending order by date
   - Latest expenses appear first

4. **Categories:**
   - Only predefined categories are allowed
   - Invalid categories will return 400 error
   - Categories are case-sensitive

5. **Data Isolation:**
   - Users can only see/modify their own expenses
   - Attempting to delete another user's expense returns 404

### Security Best Practices

- Never commit `.env` file
- Use strong SECRET_KEY in production
- Keep DATABASE_URL secure
- Tokens should be stored securely on client-side
- Use HTTPS in production

---

## 🛠️ Troubleshooting

### Common Issues

**Database Connection Error:**
```
ValueError: DATABASE_URL environment variable is not set
```
**Fix:** Create `.env` file with valid DATABASE_URL

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
- Check if token is valid
- Check if token is expired (7 days)
- Verify token is in Authorization header
- Format: `Bearer <token>`

**400 Invalid Category:**
- Check spelling and capitalization
- Use exact category names from list
- Valid: `Food`, Invalid: `food`

---

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review error messages carefully
3. Check Vercel/Neon logs
4. Verify environment variables

---

## 📄 License

MIT License - Feel free to use in your projects!

---

## 🎯 Quick Reference

### All API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | ❌ | Get API info & categories |
| POST | `/auth/register` | ❌ | Register new user |
| POST | `/auth/login` | ❌ | Login & get token |
| POST | `/auth/logout` | ✅ | Logout |
| POST | `/expense/create_expense` | ✅ | Create expense |
| DELETE | `/expense/delete_expense/{id}` | ✅ | Delete expense |
| GET | `/expense/list_expense` | ✅ | List all expenses |
| GET | `/expense/list_expense_by_category` | ✅ | List by category |
| GET | `/stats/total` | ✅ | Get total stats |
| GET | `/stats/total_by_category` | ✅ | Get stats by category |

### Available Categories
`Food` | `Transport` | `Entertainment` | `Shopping` | `Bills` | `Healthcare` | `Education` | `Others`

### Base URLs
- **Local:** `http://localhost:8000`
- **Production:** `https://your-project.vercel.app`

### Interactive Docs
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

---

**Happy Expense Tracking! 💰**