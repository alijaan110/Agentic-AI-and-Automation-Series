# 🎬 Step-by-Step Visual Walkthrough

## Complete Guide from Installation to Testing

---

## 📍 PHASE 1: PREPARATION (5 minutes)

### Step 1.1: Check Prerequisites
```
┌─────────────────────────────────┐
│  Open Terminal/Command Prompt   │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Run: python --version          │
│  Should show: Python 3.11+      │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Run: pip --version             │
│  Should show pip version        │
└─────────────────────────────────┘
```

**Expected Output:**
```
$ python --version
Python 3.11.5

$ pip --version
pip 23.2.1
```

✅ **Success Criteria**: Both commands work without errors

---

### Step 1.2: Get OpenAI API Key
```
┌─────────────────────────────────┐
│  1. Go to platform.openai.com   │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  2. Sign up or Log in           │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  3. Go to API Keys section      │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  4. Create new secret key       │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  5. Copy key (starts with sk-)  │
└─────────────────────────────────┘
```

**Your key will look like:**
```
sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234
```

✅ **Success Criteria**: You have copied your API key

---

## 📦 PHASE 2: INSTALLATION (10 minutes)

### Step 2.1: Navigate to Project
```
Terminal Window
┌────────────────────────────────────────────┐
│ $ cd api_tester_agent                      │
│ $ ls                                       │
│                                            │
│ app.py                                     │
│ sample_api.py                              │
│ requirements.txt                           │
│ .env                                       │
│ README.md                                  │
│ ...                                        │
└────────────────────────────────────────────┘
```

✅ **Success Criteria**: You see all project files

---

### Step 2.2: Create Virtual Environment (Optional but Recommended)
```
Terminal Window
┌────────────────────────────────────────────┐
│ $ python -m venv venv                      │
│ Creating virtual environment...            │
│ Done!                                      │
│                                            │
│ $ source venv/bin/activate    # Mac/Linux │
│ OR                                         │
│ $ venv\Scripts\activate       # Windows   │
│                                            │
│ (venv) $                                   │
└────────────────────────────────────────────┘
```

**You'll notice `(venv)` appears before your prompt**

✅ **Success Criteria**: Prompt shows `(venv)`

---

### Step 2.3: Install Dependencies
```
Terminal Window
┌────────────────────────────────────────────┐
│ (venv) $ pip install -r requirements.txt   │
│                                            │
│ Collecting fastapi...                      │
│ Collecting uvicorn...                      │
│ Collecting langgraph...                    │
│ Collecting openai...                       │
│ ...                                        │
│ Successfully installed [packages]          │
└────────────────────────────────────────────┘
```

**This will take 1-2 minutes**

✅ **Success Criteria**: See "Successfully installed..."

---

### Step 2.4: Configure API Key
```
1. Open .env file in text editor
┌────────────────────────────────────────────┐
│ OPENAI_API_KEY=your_openai_api_key_here    │
│ HOST=0.0.0.0                               │
│ PORT=8000                                  │
└────────────────────────────────────────────┘

2. Replace with your actual key
┌────────────────────────────────────────────┐
│ OPENAI_API_KEY=sk-proj-abc123...          │
│ HOST=0.0.0.0                               │
│ PORT=8000                                  │
└────────────────────────────────────────────┘

3. Save the file
```

✅ **Success Criteria**: .env file has your real API key

---

## 🚀 PHASE 3: STARTING SERVICES (2 minutes)

### Step 3.1: Start Sample API (Terminal 1)
```
Terminal 1
┌────────────────────────────────────────────┐
│ (venv) $ python sample_api.py              │
│                                            │
│ ========================================   │
│ 🚀 Sample API Server Starting...          │
│ ========================================   │
│                                            │
│ 📚 Available Endpoints:                    │
│   - http://localhost:8001/                │
│   - http://localhost:8001/docs            │
│   - http://localhost:8001/users           │
│                                            │
│ INFO: Uvicorn running on 0.0.0.0:8001     │
└────────────────────────────────────────────┘
```

**KEEP THIS TERMINAL OPEN!**

✅ **Success Criteria**: See "Uvicorn running on..."

---

### Step 3.2: Start API Tester Agent (Terminal 2)
```
Open NEW Terminal Window

Terminal 2
┌────────────────────────────────────────────┐
│ $ cd api_tester_agent                      │
│ $ source venv/bin/activate    # if using  │
│                                            │
│ (venv) $ python app.py                     │
│                                            │
│ INFO: Starting API Tester Agent...        │
│ INFO: Uvicorn running on 0.0.0.0:8000     │
└────────────────────────────────────────────┘
```

**KEEP THIS TERMINAL OPEN TOO!**

✅ **Success Criteria**: See "Uvicorn running on 0.0.0.0:8000"

---

### Step 3.3: Verify Both Services (Terminal 3)
```
Open THIRD Terminal Window

Terminal 3
┌────────────────────────────────────────────┐
│ $ curl http://localhost:8000/health        │
│ {                                          │
│   "status": "healthy",                     │
│   "service": "API Tester Agent"            │
│ }                                          │
│                                            │
│ $ curl http://localhost:8001/health        │
│ {                                          │
│   "status": "healthy",                     │
│   "uptime": "running"                      │
│ }                                          │
└────────────────────────────────────────────┘
```

**Both should return JSON with "healthy" status**

✅ **Success Criteria**: Both health checks return 200 OK

---

## 🧪 PHASE 4: FIRST TEST (5 minutes)

### Step 4.1: Test Sample API Directly
```
Terminal 3
┌────────────────────────────────────────────┐
│ $ curl http://localhost:8001/users         │
│                                            │
│ [                                          │
│   {                                        │
│     "id": 1,                               │
│     "name": "John Doe",                    │
│     "email": "john@example.com",           │
│     "age": 30,                             │
│     "is_active": true                      │
│   },                                       │
│   {                                        │
│     "id": 2,                               │
│     "name": "Jane Smith",                  │
│     "email": "jane@example.com",           │
│     "age": 25,                             │
│     "is_active": true                      │
│   }                                        │
│ ]                                          │
└────────────────────────────────────────────┘
```

✅ **Success Criteria**: See array of users

---

### Step 4.2: Use Agent to Test (Natural Language)
```
Terminal 3
┌────────────────────────────────────────────┐
│ $ curl -X POST localhost:8000/api/test/... │
│   -H "Content-Type: application/json" \    │
│   -d '{                                     │
│     "instruction": "Test the users API"    │
│   }'                                       │
│                                            │
│ {                                          │
│   "success": true,                         │
│   "status_code": 200,                      │
│   "response_time_ms": 234.5,               │
│   "ai_analysis": "The API response is..."  │
│ }                                          │
└────────────────────────────────────────────┘
```

**This may take 2-3 seconds due to AI analysis**

✅ **Success Criteria**: See success: true and AI analysis

---

## 🌐 PHASE 5: BROWSER TESTING (Interactive!)

### Step 5.1: Open Browser Docs
```
┌─────────────────────────────────────┐
│  1. Open your web browser           │
└─────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  2. Go to:                          │
│     http://localhost:8000/docs      │
└─────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  3. You'll see Swagger UI           │
│     with all API endpoints          │
└─────────────────────────────────────┘
```

**You should see:**
```
┌──────────────────────────────────────────────┐
│  Advanced API Tester Agent                   │
│  Version 1.0.0                               │
│                                              │
│  ▼ Health                                    │
│    GET /health                               │
│                                              │
│  ▼ Testing                                   │
│    POST /api/test/natural                    │
│    POST /api/test/run                        │
│                                              │
│  ▼ Load Testing                              │
│    POST /api/test/load                       │
│                                              │
│  ▼ Test Generation                           │
│    POST /api/test/generate                   │
└──────────────────────────────────────────────┘
```

✅ **Success Criteria**: Swagger UI loads successfully

---

### Step 5.2: Test via Browser
```
In Browser (Swagger UI)
┌──────────────────────────────────────────────┐
│  1. Click: POST /api/test/natural            │
│  2. Click: "Try it out"                      │
│  3. Enter in Request body:                   │
│     {                                        │
│       "instruction": "Test users API"        │
│     }                                        │
│  4. Click: "Execute"                         │
│  5. Scroll down to see Response              │
└──────────────────────────────────────────────┘
```

**You'll see the response appear below!**

✅ **Success Criteria**: Response appears with success: true

---

## 🎯 PHASE 6: ADVANCED TESTING (10 minutes)

### Test 1: GET Request with Parameters
```
Terminal 3
┌────────────────────────────────────────────┐
│ $ curl -X POST localhost:8000/api/test/run \│
│   -H "Content-Type: application/json" \    │
│   -d '{                                     │
│     "name": "Get Single User",              │
│     "method": "GET",                        │
│     "url": "http://localhost:8001/users/1", │
│     "expected_status": 200,                 │
│     "expected_contains": ["John", "email"]  │
│   }'                                       │
└────────────────────────────────────────────┘
```

✅ **Success Criteria**: Returns user data for ID 1

---

### Test 2: POST Request (Create User)
```
Terminal 3
┌────────────────────────────────────────────┐
│ $ curl -X POST localhost:8000/api/test/run \│
│   -H "Content-Type: application/json" \    │
│   -d '{                                     │
│     "name": "Create New User",              │
│     "method": "POST",                       │
│     "url": "http://localhost:8001/users",   │
│     "body": {                               │
│       "name": "Alice Wonder",               │
│       "email": "alice@example.com",         │
│       "age": 28                             │
│     },                                      │
│     "expected_status": 201                  │
│   }'                                       │
└────────────────────────────────────────────┘
```

✅ **Success Criteria**: Creates new user, returns ID

---

### Test 3: Load Testing
```
Terminal 3
┌────────────────────────────────────────────┐
│ $ curl -X POST localhost:8000/api/test/... │
│   -H "Content-Type: application/json" \    │
│   -d '{                                     │
│     "test_config": {                        │
│       "name": "Load Test",                  │
│       "method": "GET",                      │
│       "url": "http://localhost:8001/users"  │
│     },                                      │
│     "iterations": 10,                       │
│     "concurrent": true                      │
│   }'                                       │
└────────────────────────────────────────────┘
```

**Returns performance metrics:**
```json
{
  "total_requests": 10,
  "successful": 10,
  "failed": 0,
  "avg_time_ms": 234.5,
  "requests_per_second": 15.2,
  "ai_performance_analysis": "..."
}
```

✅ **Success Criteria**: All 10 requests successful

---

## 🤖 PHASE 7: AUTOMATED TESTING

### Run Full Test Suite
```
Terminal 3
┌────────────────────────────────────────────┐
│ $ python run_tests.py                      │
│                                            │
│ ============================================│
│   🚀 API TESTER AGENT - AUTOMATED TESTS   │
│ ============================================│
│                                            │
│ STEP 1: SERVICE HEALTH CHECKS              │
│ ✓ API Tester Agent is running             │
│ ✓ Sample API is running                   │
│                                            │
│ STEP 2: RUNNING TEST SUITE                 │
│ ✓ PASS - Direct Sample API Test           │
│ ✓ PASS - Natural Language Test            │
│ ✓ PASS - Structured GET Test              │
│ ✓ PASS - Structured POST Test             │
│ ✓ PASS - Login Test                       │
│ ✓ PASS - Load Testing                     │
│ ✓ PASS - Error Handling Test              │
│                                            │
│ STEP 3: TEST RESULTS SUMMARY               │
│ Total Tests: 7                             │
│ ✓ Passed: 7                                │
│ ✓ Failed: 0                                │
│                                            │
│ ╔════════════════════════════════════════╗│
│ ║   🎉 ALL TESTS PASSED! EXCELLENT! 🎉  ║│
│ ╚════════════════════════════════════════╝│
└────────────────────────────────────────────┘
```

✅ **Success Criteria**: All tests pass

---

## 📊 PHASE 8: UNDERSTANDING RESULTS

### Reading Test Results
```
Successful Test Result Structure:
┌────────────────────────────────────────────┐
│ {                                          │
│   "success": true,          ← Overall pass │
│   "status_code": 200,       ← HTTP status  │
│   "response_time_ms": 234,  ← Performance  │
│   "response_body": {...},   ← API response │
│   "validations": [          ← Checks       │
│     {"type": "...", "passed": true}        │
│   ],                                       │
│   "ai_analysis": "..."      ← AI insights  │
│ }                                          │
└────────────────────────────────────────────┘

Failed Test Result Structure:
┌────────────────────────────────────────────┐
│ {                                          │
│   "success": false,         ← Test failed  │
│   "status_code": 404,       ← Error code   │
│   "response_time_ms": 123,                 │
│   "error": "Not found",     ← Error msg    │
│   "ai_analysis": "..."      ← Debug help   │
│ }                                          │
└────────────────────────────────────────────┘
```

---

## 🎓 PHASE 9: YOUR OWN APIS

### Testing Your Own API
```
Replace URL with your API:

Instead of:
"url": "http://localhost:8001/users"

Use:
"url": "https://your-api.com/endpoint"

Add authentication if needed:
{
  "name": "My API Test",
  "method": "GET",
  "url": "https://your-api.com/data",
  "headers": {
    "Authorization": "Bearer your-token"
  }
}
```

---

## ✅ SUCCESS CHECKLIST

Mark each as you complete:

- [ ] Python 3.11+ installed
- [ ] OpenAI API key obtained
- [ ] Dependencies installed
- [ ] .env configured with API key
- [ ] Sample API running (Terminal 1)
- [ ] API Tester Agent running (Terminal 2)
- [ ] Health checks pass for both
- [ ] Can test Sample API directly
- [ ] Can test via Agent (natural language)
- [ ] Can test via Agent (structured)
- [ ] Browser Swagger UI works
- [ ] Automated tests pass
- [ ] Understand result structure
- [ ] Ready to test own APIs

---

## 🎉 CONGRATULATIONS!

```
┌──────────────────────────────────────────────────┐
│                                                  │
│            🎊 YOU DID IT! 🎊                    │
│                                                  │
│  You now have a fully functional                │
│  AI-powered API testing agent!                  │
│                                                  │
│  What you can do now:                           │
│  ✓ Test any REST API                           │
│  ✓ Use natural language                         │
│  ✓ Get AI-powered insights                      │
│  ✓ Run load tests                               │
│  ✓ Generate test suites                         │
│  ✓ Automate your testing                        │
│                                                  │
│            Happy Testing! 🚀                     │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 📖 NEXT STEPS

1. **Explore More Features**
   - Try test generation
   - Experiment with load testing
   - Test different HTTP methods

2. **Read Documentation**
   - README.md - Overview
   - QUICK_REFERENCE.md - Commands
   - ARCHITECTURE.md - How it works

3. **Test Real APIs**
   - Test your own projects
   - Test public APIs
   - Build test suites

4. **Customize**
   - Modify prompts
   - Add custom validations
   - Extend functionality

---

**Remember**: Keep the visual diagrams from ARCHITECTURE.md handy!

**Need Help?** Check TROUBLESHOOTING.md
