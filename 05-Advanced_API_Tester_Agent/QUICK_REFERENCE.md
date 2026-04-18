# 📋 Quick Reference Cheat Sheet

## 🚀 Starting the Services

```bash
# Terminal 1: Sample API (port 8001)
python sample_api.py

# Terminal 2: API Tester Agent (port 8000)
python app.py
```

---

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Sample API | http://localhost:8001 | API to test |
| Sample API Docs | http://localhost:8001/docs | Interactive API docs |
| API Tester Agent | http://localhost:8000 | Testing service |
| Agent Docs | http://localhost:8000/docs | Interactive testing UI |
| Health Check (Sample) | http://localhost:8001/health | Check if sample API is up |
| Health Check (Agent) | http://localhost:8000/health | Check if agent is up |

---

## ⚡ Quick Tests (Copy & Paste)

### Test 1: Simple GET Request
```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quick Test",
    "method": "GET",
    "url": "http://localhost:8001/users",
    "expected_status": 200
  }'
```

### Test 2: Natural Language
```bash
curl -X POST http://localhost:8000/api/test/natural \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "Test the users endpoint and verify it returns user data"
  }'
```

### Test 3: POST Request
```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Create User",
    "method": "POST",
    "url": "http://localhost:8001/users",
    "body": {"name": "Test", "email": "test@example.com"},
    "expected_status": 201
  }'
```

### Test 4: Load Test
```bash
curl -X POST http://localhost:8000/api/test/load \
  -H "Content-Type: application/json" \
  -d '{
    "test_config": {
      "name": "Load Test",
      "method": "GET",
      "url": "http://localhost:8001/users"
    },
    "iterations": 10,
    "concurrent": true
  }'
```

---

## 🎯 Sample API Endpoints

### GET Endpoints
```bash
GET  /                          # Root
GET  /health                    # Health check
GET  /users                     # All users (paginated)
GET  /users/{id}                # Single user
GET  /products                  # All products (filterable)
GET  /products/{id}             # Single product
GET  /protected/data            # Protected (needs API key)
```

### POST Endpoints
```bash
POST /users                     # Create user
POST /auth/login                # Login
```

### PUT/PATCH/DELETE Endpoints
```bash
PUT    /users/{id}              # Update user (full)
PATCH  /users/{id}              # Update user (partial)
DELETE /users/{id}              # Delete user
```

---

## 🔐 Test Credentials

### Login
- **Email**: john@example.com
- **Password**: password123

### API Key (for protected endpoints)
- **Header**: X-API-Key
- **Value**: test-api-key-12345

---

## 📝 Request Body Templates

### Create User
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```

### Login
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

### Test Config (for Agent)
```json
{
  "name": "My Test",
  "method": "GET",
  "url": "http://localhost:8001/users",
  "headers": {},
  "params": {},
  "body": null,
  "expected_status": 200,
  "expected_contains": ["email"],
  "timeout": 30
}
```

---

## 🛠️ Common Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Check if Port is in Use
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

### Kill Process on Port
```bash
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>
```

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## 🐛 Debugging Tips

1. **Check logs** in the terminal where services are running
2. **Test directly** before using agent:
   ```bash
   curl http://localhost:8001/users
   ```
3. **Verify environment** variables in .env
4. **Check API docs** at /docs endpoints
5. **Use verbose curl** for more details:
   ```bash
   curl -v http://localhost:8000/health
   ```

---

## 📊 Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET request successful |
| 201 | Created | POST created new resource |
| 400 | Bad Request | Invalid data sent |
| 401 | Unauthorized | Missing/invalid credentials |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Internal server error |

---

## 💡 Pro Tips

1. **Start simple**: Test GET requests first
2. **Use the docs**: Both services have /docs endpoints
3. **Read AI analysis**: Valuable debugging insights
4. **Save configs**: Keep test configs in JSON files
5. **Automate**: Create Python scripts for repeated tests
6. **Check both terminals**: Logs appear in server terminals
7. **Test incrementally**: One endpoint at a time

---

## 🆘 Quick Fixes

### Services won't start
```bash
# Make sure ports are free
# Check for typos in .env
# Verify Python version: python --version
```

### Tests always fail
```bash
# Verify both services are running
# Test sample API directly first
# Check URLs in test configs
```

### OpenAI errors
```bash
# Verify API key in .env
# Check OpenAI account credits
# Try: echo $OPENAI_API_KEY (Linux/Mac)
```

---

## 📱 Browser Testing

### Interactive Testing (Easiest!)
1. Open http://localhost:8000/docs
2. Click any endpoint
3. Click "Try it out"
4. Fill in the form
5. Click "Execute"
6. See results instantly!

---

## 🎓 Learning Path

1. ✅ Install and run both services
2. ✅ Test health endpoints
3. ✅ Try sample API directly
4. ✅ Use agent for simple GET test
5. ✅ Try natural language testing
6. ✅ Test POST requests
7. ✅ Run load tests
8. ✅ Generate test cases
9. ✅ Create your own tests
10. ✅ Build test automation scripts

---

## 📞 Need Help?

1. Check TESTING_GUIDE.md for detailed examples
2. Check SETUP_GUIDE.md for installation help
3. Look at sample_api.py code for endpoint details
4. Review app.py for agent functionality
5. Check logs in both terminal windows

---

**Remember: Keep this sheet handy while testing! 📌**
