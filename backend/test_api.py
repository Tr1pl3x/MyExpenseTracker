import requests
import json

# Base URL - change this when deployed to Vercel
BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    print("\n1. Testing Registration...")
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_login():
    """Test user login"""
    print("\n2. Testing Login...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json().get("access_token")

def test_create_expense(token):
    """Test creating expenses"""
    print("\n3. Testing Create Expense...")
    
    expenses = [
        {"amount": 50.00, "category": "Food", "description": "Lunch"},
        {"amount": 30.00, "category": "Transport", "description": "Taxi"},
        {"amount": 100.00, "category": "Shopping", "description": "Clothes"},
        {"amount": 25.00, "category": "Food", "description": "Dinner"}
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    for expense in expenses:
        response = requests.post(
            f"{BASE_URL}/expense/create_expense",
            json=expense,
            headers=headers
        )
        print(f"Created: {expense['description']} - Status: {response.status_code}")

def test_list_expenses(token):
    """Test listing all expenses"""
    print("\n4. Testing List All Expenses...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/expense/list_expense",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_list_by_category(token):
    """Test listing expenses by category"""
    print("\n5. Testing List Expenses by Category (Food)...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/expense/list_expense_by_category?category=Food",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_total_stats(token):
    """Test getting total statistics"""
    print("\n6. Testing Total Statistics...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/stats/total",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_stats_by_category(token):
    """Test getting statistics by category"""
    print("\n7. Testing Statistics by Category...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/stats/total_by_category",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def main():
    print("=" * 60)
    print("Expense Tracker API Test Suite")
    print("=" * 60)
    
    try:
        # Test registration (might fail if user exists)
        try:
            test_register()
        except Exception as e:
            print(f"Registration skipped (user might exist): {e}")
        
        # Test login
        token = test_login()
        if not token:
            print("Login failed! Cannot continue tests.")
            return
        
        print(f"\nAccess Token: {token[:20]}...")
        
        # Test expense operations
        test_create_expense(token)
        test_list_expenses(token)
        test_list_by_category(token)
        test_total_stats(token)
        test_stats_by_category(token)
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API.")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()