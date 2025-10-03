# 🧭 Expense Tracker Backend Plan (FastAPI + Vercel)

## ⚙️ Stack

- **Framework:** FastAPI (Python)  
- **Database:** Postgres (Neon / Vercel Postgres)  
- **ORM:** SQLModel (SQLAlchemy + Pydantic)  
- **Auth:** JWT + bcrypt  
- **Deployment:** Vercel (serverless functions in `api/` folder)  
- **Migrations:** Alembic

---

## 🗄️ Database Schema (Example)

### **Users Table**
| Column          | Type         | Notes |
|-----------------|--------------|-------|
| `id`           | UUID (PK)   | Auto-generated |
| `username`     | TEXT (unique) | Required |
| `password_hash`| TEXT         | Bcrypt hash |
| `display_name` | TEXT         | |
| `created_at`   | TIMESTAMPTZ | Default: now |
| `updated_at`   | TIMESTAMPTZ | Default: now |

---

### **Categories Table**
| Column        | Type         | Notes |
|---------------|--------------|-------|
| `id`        | UUID (PK)   | |
| `user_id`   | UUID (FK → users.id, nullable) | `NULL` = global category |
| `name`      | TEXT        | Unique per user/global |
| `emoji`     | TEXT (optional) | |
| `created_at`| TIMESTAMPTZ | |

---

### **Expenses Table**
| Column         | Type         | Notes |
|----------------|--------------|-------|
| `id`         | UUID (PK)   | |
| `user_id`    | UUID (FK → users.id) | Indexed |
| `amount_cents`| INT         | Stored as cents |
| `currency`   | TEXT (e.g. AUD) | |
| `occurred_at`| TIMESTAMPTZ | Stored in UTC |
| `category_id`| UUID (FK → categories.id, nullable) | |
| `merchant`   | TEXT (optional) | |
| `note`       | TEXT (optional) | |
| `created_at` | TIMESTAMPTZ | |
| `updated_at` | TIMESTAMPTZ | |

---

### 📝 Example Records

**users**
```json
{
  "id": "8f14e45f-ea7a-4f0c-a1e9-12a18db4a4c3",
  "username": "pso",
  "password_hash": "$2b$12$...",
  "display_name": "Pyae",
  "created_at": "2025-06-01T10:00:00Z",
  "updated_at": "2025-06-01T10:00:00Z"
}
```

**expenses**
```json
{
  "id": "5b5c4c54-65d0-4a6b-a32c-7b23f4adf442",
  "user_id": "8f14e45f-ea7a-4f0c-a1e9-12a18db4a4c3",
  "amount_cents": 1200,
  "currency": "AUD",
  "occurred_at": "2025-06-30T01:53:00Z",
  "category_id": "9a0f4e12-bb32-4c44-87f2-43df0d8b9d2a",
  "merchant": "McDonald's",
  "note": "Late night snack",
  "created_at": "2025-06-30T01:53:00Z",
  "updated_at": "2025-06-30T01:53:00Z"
}
```

---

## 🧍 1. Auth Routes

| Method | Path              | Description |
|--------|---------------------|-------------|
| `POST` | `/auth/register`   | Create new user (hash password, store in DB, return JWT). |
| `POST` | `/auth/login`      | Verify credentials, return JWT. |
| `GET`  | `/auth/me`         | Return user profile using token. |

**Notes:**  
- Store only password hashes (bcrypt).  
- JWT includes `sub=user_id` and `exp`.  
- Optional: `POST /auth/refresh` for longer sessions.

---

## 💸 2. Expense Routes

| Method | Path                   | Description |
|--------|--------------------------|-------------|
| `POST` | `/expenses`            | Add new expense. |
| `GET`  | `/expenses`            | Get all user expenses. Supports filters: `?from=...&to=...&category=...&limit=...&cursor=...`. |
| `GET`  | `/expenses/{id}`       | Get single expense. |
| `PATCH`| `/expenses/{id}`       | Edit expense fields. |
| `DELETE`| `/expenses/{id}`     | Remove expense. |

**Notes:**  
- Use keyset pagination (cursor on `occurred_at`).  
- Convert dates to UTC before storing.  
- Validate category ownership.

---

## 🏷️ 3. Category Routes

| Method | Path                     | Description |
|--------|----------------------------|-------------|
| `GET`  | `/categories`            | List global + user categories. |
| `POST` | `/categories`            | Create user category. |
| `PATCH`| `/categories/{id}`       | Update name/emoji. |
| `DELETE`| `/categories/{id}`     | Delete category (handle reassignment). |

**Notes:**  
- Seed global categories (e.g., Food, Transport).  
- Enforce uniqueness per user/global scope.

---

## 📊 4. Report Routes *(Phase 2)*

| Method | Path                        | Description |
|--------|-------------------------------|-------------|
| `GET`  | `/reports/summary`         | Total spend, top categories, daily average. |
| `GET`  | `/reports/trends`          | Weekly/monthly breakdown for charts. |

**Notes:**  
- Use SQL aggregation (no need to store aggregates).  
- Return data formatted for frontend charting.

---

## 📁 Folder Structure

```
api/
  main.py
  routes/
    auth.py
    expenses.py
    categories.py
    reports.py
  models.py
  schemas.py
  database.py
  auth_utils.py
```

---

## 🧱 Build Phases

1. **Auth + DB Setup**  
   - User model, register/login routes, JWT.

2. **Expense CRUD**  
   - Expense model, basic CRUD endpoints.

3. **Categories**  
   - Category model + endpoints.

4. **Reports & Extras**  
   - Summary/trend routes, budgets, recurring rules (optional).

---

## ✅ Summary

This plan covers everything needed for a **fully functional FastAPI backend** on Vercel:
- Secure user authentication  
- Expense management with filtering & pagination  
- Category organization  
- Optional reporting features for future growth

Each phase is independent → you can deploy step by step.
