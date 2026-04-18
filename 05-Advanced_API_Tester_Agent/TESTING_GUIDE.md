# 🎯 Complete Testing Guide - Step by Step

## Part 1: Running Both Services

### Step 1: Start the Sample API (Terminal 1)

```bash
# Navigate to the project directory
cd api_tester_agent

# Run the sample API on port 8001
python sample_api.py
```

**Expected Output:**
```
============================================================
🚀 Sample API Server Starting...
============================================================

📚 Available Endpoints:
  - http://localhost:8001/
  - http://localhost:8001/docs (Interactive API Docs)
  - http://localhost:8001/users
  - http://localhost:8001/products
  - http://localhost:8001/auth/login

🔑 Test Credentials:
  - Email: john@example.com
  - Password: password123

🔐 API Key for Protected Endpoints:
  - X-API-Key: test-api-key-12345

============================================================

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

✅ Sample API is now running on http://localhost:8001

---

### Step 2: Start the API Tester Agent (Terminal 2)

Open a **NEW terminal** window and run:

```bash
# Navigate to the same directory
cd api_tester_agent

# Activate virtual environment if you created one
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Run the API Tester Agent on port 8000
python app.py
```

**Expected Output:**
```
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ API Tester Agent is now running on http://localhost:8000

---

## Part 2: Verify Both Services are Running

### Open a **third terminal** and test:

```bash
# Test Sample API
curl http://localhost:8001/health

# Test API Tester Agent
curl http://localhost:8000/health
```

Both should return healthy status! ✅

---

## Part 3: Interactive Testing (Browser)

### Option A: Using Swagger UI (Recommended for Beginners)

#### For Sample API:
1. Open: http://localhost:8001/docs
2. You'll see all available endpoints
3. Click on any endpoint to expand it
4. Click "Try it out" to test

#### For API Tester Agent:
1. Open: http://localhost:8000/docs
2. Click on **POST /api/test/natural**
3. Click "Try it out"
4. Enter test data and execute

---

## Part 4: Test the Sample API Directly

### Test 1: Get All Users
```bash
curl http://localhost:8001/users
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "is_active": true,
    "created_at": "2024-12-09T..."
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 25,
    "is_active": true,
    "created_at": "2024-12-09T..."
  }
]
```

### Test 2: Get Single User
```bash
curl http://localhost:8001/users/1
```

### Test 3: Get All Products
```bash
curl http://localhost:8001/products
```

### Test 4: Login
```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Test 5: Create New User
```bash
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Wonder",
    "email": "alice@example.com",
    "age": 28
  }'
```

---

## Part 5: Test Using the API Tester Agent

Now let's use our AI-powered agent to test the sample API!

### Test 1: Natural Language Test - Simple GET

```bash
curl -X POST http://localhost:8000/api/test/natural \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "Test the users endpoint on localhost:8001 and check if it returns user data with names and emails"
  }'
```

**What happens:**
1. Agent parses your instruction
2. Understands you want to GET /users
3. Executes the request
4. AI analyzes the response
5. Returns detailed insights

### Test 2: Natural Language Test - With Parameters

```bash
curl -X POST http://localhost:8000/api/test/natural \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "Get products from localhost:8001 filtered by Electronics category",
    "context": {
      "base_url": "http://localhost:8001"
    }
  }'
```

### Test 3: Structured Test - GET Users

```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Get All Users Test",
    "method": "GET",
    "url": "http://localhost:8001/users",
    "expected_status": 200,
    "expected_contains": ["email", "name", "id"],
    "timeout": 10
  }'
```

### Test 4: Structured Test - GET Single User

```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Get User By ID",
    "method": "GET",
    "url": "http://localhost:8001/users/1",
    "expected_status": 200,
    "expected_contains": ["John Doe", "john@example.com"]
  }'
```

### Test 5: Structured Test - POST (Create User)

```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Create New User Test",
    "method": "POST",
    "url": "http://localhost:8001/users",
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "name": "Test User",
      "email": "testuser@example.com",
      "age": 25
    },
    "expected_status": 201,
    "expected_contains": ["id", "email", "testuser@example.com"]
  }'
```

### Test 6: Test Login Endpoint

```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "User Login Test",
    "method": "POST",
    "url": "http://localhost:8001/auth/login",
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "email": "john@example.com",
      "password": "password123"
    },
    "expected_status": 200,
    "expected_contains": ["token", "success"]
  }'
```

### Test 7: Test Protected Endpoint

```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Protected Endpoint Test",
    "method": "GET",
    "url": "http://localhost:8001/protected/data",
    "headers": {
      "X-API-Key": "test-api-key-12345"
    },
    "expected_status": 200,
    "expected_contains": ["secret"]
  }'
```

### Test 8: Test Error Handling (404)

```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "404 Error Test",
    "method": "GET",
    "url": "http://localhost:8001/users/999",
    "expected_status": 404
  }'
```

### Test 9: Load Testing

```bash
curl -X POST http://localhost:8000/api/test/load \
  -H "Content-Type: application/json" \
  -d '{
    "test_config": {
      "name": "Load Test Users Endpoint",
      "method": "GET",
      "url": "http://localhost:8001/users"
    },
    "iterations": 20,
    "concurrent": true
  }'
```

### Test 10: Auto-Generate Test Cases

```bash
curl -X POST http://localhost:8000/api/test/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "User Creation",
    "method": "POST",
    "url": "http://localhost:8001/users",
    "body": {
      "name": "Test User",
      "email": "test@example.com",
      "age": 25
    },
    "expected_status": 201
  }'
```

---

## Part 6: Using Python Scripts

Create a file called `run_tests.py`:

```python
import requests
import json
import time

# Configuration
AGENT_URL = "http://localhost:8000"
SAMPLE_API_URL = "http://localhost:8001"

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def run_test(name, payload):
    """Run a test and print results"""
    print(f"🧪 Running: {name}")
    try:
        response = requests.post(
            f"{AGENT_URL}/api/test/run",
            json=payload,
            timeout=30
        )
        result = response.json()
        
        if result.get("success"):
            print("   ✅ PASSED")
        else:
            print("   ❌ FAILED")
        
        print(f"   Status: {result.get('status_code')}")
        print(f"   Time: {result.get('response_time_ms', 0):.2f}ms")
        
        if result.get("ai_analysis"):
            print(f"   AI: {result['ai_analysis'][:100]}...")
        
        return result
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return None

# Test Suite
def main():
    print_section("API TESTER AGENT - AUTOMATED TEST SUITE")
    
    # Test 1: Get Users
    print_section("TEST 1: GET ALL USERS")
    run_test("Get All Users", {
        "name": "Get All Users",
        "method": "GET",
        "url": f"{SAMPLE_API_URL}/users",
        "expected_status": 200,
        "expected_contains": ["email", "name"]
    })
    
    time.sleep(1)
    
    # Test 2: Get Single User
    print_section("TEST 2: GET SINGLE USER")
    run_test("Get User 1", {
        "name": "Get User 1",
        "method": "GET",
        "url": f"{SAMPLE_API_URL}/users/1",
        "expected_status": 200,
        "expected_contains": ["John Doe"]
    })
    
    time.sleep(1)
    
    # Test 3: Get Products
    print_section("TEST 3: GET PRODUCTS")
    run_test("Get All Products", {
        "name": "Get All Products",
        "method": "GET",
        "url": f"{SAMPLE_API_URL}/products",
        "expected_status": 200,
        "expected_contains": ["price", "name"]
    })
    
    time.sleep(1)
    
    # Test 4: Login
    print_section("TEST 4: USER LOGIN")
    run_test("User Login", {
        "name": "User Login",
        "method": "POST",
        "url": f"{SAMPLE_API_URL}/auth/login",
        "body": {
            "email": "john@example.com",
            "password": "password123"
        },
        "expected_status": 200,
        "expected_contains": ["token"]
    })
    
    time.sleep(1)
    
    # Test 5: Create User
    print_section("TEST 5: CREATE NEW USER")
    run_test("Create User", {
        "name": "Create User",
        "method": "POST",
        "url": f"{SAMPLE_API_URL}/users",
        "body": {
            "name": "Automated Test User",
            "email": f"auto-{int(time.time())}@example.com",
            "age": 30
        },
        "expected_status": 201
    })
    
    time.sleep(1)
    
    # Test 6: 404 Error Test
    print_section("TEST 6: ERROR HANDLING (404)")
    run_test("404 Test", {
        "name": "404 Test",
        "method": "GET",
        "url": f"{SAMPLE_API_URL}/users/999",
        "expected_status": 404
    })
    
    print_section("TEST SUITE COMPLETED")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python run_tests.py
```

---

## Part 7: Using Postman Collection

### Import into Postman:

1. Open Postman
2. Click "Import"
3. Create these requests:

#### Request 1: Test Sample API
- Method: POST
- URL: `http://localhost:8000/api/test/run`
- Body (JSON):
```json
{
  "name": "Get Users",
  "method": "GET",
  "url": "http://localhost:8001/users",
  "expected_status": 200
}
```

#### Request 2: Natural Language Test
- Method: POST
- URL: `http://localhost:8000/api/test/natural`
- Body (JSON):
```json
{
  "instruction": "Test the users API and check if it returns valid user data with emails"
}
```

---

## Part 8: Understanding the Results

### Success Response Structure:
```json
{
  "success": true,
  "status_code": 200,
  "response_time_ms": 45.6,
  "response_body": { /* actual API response */ },
  "response_headers": { /* response headers */ },
  "validations": [
    {
      "type": "status_code_match",
      "expected": 200,
      "actual": 200,
      "passed": true
    }
  ],
  "ai_analysis": "Detailed AI insights about the API response..."
}
```

### Error Response Structure:
```json
{
  "success": false,
  "status_code": 404,
  "response_time_ms": 23.1,
  "error": "User not found",
  "ai_analysis": "The API returned 404 because..."
}
```

---

## Part 9: Advanced Testing Scenarios

### Scenario 1: Complete User Workflow
```bash
# 1. Create user
# 2. Get the user
# 3. Update the user
# 4. Delete the user

# Each step uses the API Tester Agent
```

### Scenario 2: Security Testing
```bash
# Test protected endpoints without auth
# Test with invalid API keys
# Test SQL injection attempts
```

### Scenario 3: Performance Testing
```bash
# Run load tests with different concurrency levels
# Monitor response times
# Get AI performance recommendations
```

---

## Part 10: Troubleshooting

### Problem: "Connection refused"
**Solution:**
- Make sure both servers are running
- Check ports 8000 and 8001 are not used by other apps
- Verify URLs in your tests

### Problem: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "OpenAI API Error"
**Solution:**
- Check your API key in .env
- Verify you have credits
- Check internet connection

### Problem: Tests fail with timeout
**Solution:**
- Increase timeout in test config
- Check if sample API is responding
- Try: `curl http://localhost:8001/health`

---

## Part 11: Next Steps

Now that everything is working:

1. **Explore the Sample API**
   - Try different endpoints
   - Test with various parameters
   - Experiment with error cases

2. **Test Your Own APIs**
   - Replace URLs with your APIs
   - Add authentication headers
   - Customize validations

3. **Build Test Suites**
   - Create Python scripts with multiple tests
   - Automate regression testing
   - Set up CI/CD integration

4. **Analyze AI Insights**
   - Read the AI analysis carefully
   - Use suggestions to improve APIs
   - Learn from error explanations

---

## 🎉 Congratulations!

You now have:
- ✅ A running API Tester Agent
- ✅ A sample API to test
- ✅ Knowledge of how to test APIs
- ✅ AI-powered insights
- ✅ Automated testing capabilities

**Happy Testing! 🚀**
