"""
Sample FastAPI Application for Testing
Medium-Grade API with various endpoints for comprehensive testing
"""

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, status, Query
from pydantic import BaseModel, EmailStr, Field
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Sample API for Testing",
    description="A medium-grade API to test the API Tester Agent",
    version="1.0.0"
)

# ========================================================================
# DATA MODELS
# ========================================================================

class User(BaseModel):
    """User model"""
    id: int
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)
    is_active: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class UserCreate(BaseModel):
    """User creation model"""
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)


class UserUpdate(BaseModel):
    """User update model"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    is_active: Optional[bool] = None


class Product(BaseModel):
    """Product model"""
    id: int
    name: str
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    in_stock: bool = True
    category: str


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginResponse(BaseModel):
    """Login response model"""
    success: bool
    token: Optional[str] = None
    message: str


class APIResponse(BaseModel):
    """Generic API response"""
    success: bool
    message: str
    data: Optional[dict] = None


# ========================================================================
# IN-MEMORY DATA STORAGE
# ========================================================================

# Sample users database
users_db = [
    User(id=1, name="John Doe", email="john@example.com", age=30),
    User(id=2, name="Jane Smith", email="jane@example.com", age=25),
    User(id=3, name="Bob Johnson", email="bob@example.com", age=35, is_active=False),
]

# Sample products database
products_db = [
    Product(id=1, name="Laptop", price=999.99, description="High-performance laptop", category="Electronics"),
    Product(id=2, name="Mouse", price=29.99, description="Wireless mouse", category="Electronics"),
    Product(id=3, name="Desk", price=299.99, description="Standing desk", category="Furniture"),
    Product(id=4, name="Chair", price=199.99, description="Ergonomic chair", category="Furniture", in_stock=False),
]

# Counter for generating IDs
user_id_counter = 4
product_id_counter = 5

# Valid API key for testing
VALID_API_KEY = "test-api-key-12345"

# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def verify_api_key(api_key: Optional[str]) -> bool:
    """Verify API key"""
    return api_key == VALID_API_KEY


def find_user_by_id(user_id: int) -> Optional[User]:
    """Find user by ID"""
    for user in users_db:
        if user.id == user_id:
            return user
    return None


def find_user_by_email(email: str) -> Optional[User]:
    """Find user by email"""
    for user in users_db:
        if user.email == email:
            return user
    return None


# ========================================================================
# ENDPOINTS - HEALTH & INFO
# ========================================================================

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Sample API for Testing",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "products": "/products",
            "auth": "/auth/login",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running"
    }


# ========================================================================
# ENDPOINTS - USERS (CRUD Operations)
# ========================================================================

@app.get("/users", response_model=List[User], tags=["Users"])
async def get_all_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    active_only: bool = Query(False, description="Return only active users")
):
    """
    Get all users with pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Number of records to return (default: 10)
    - **active_only**: Filter for active users only
    """
    filtered_users = users_db
    
    if active_only:
        filtered_users = [u for u in users_db if u.is_active]
    
    return filtered_users[skip:skip + limit]


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: int):
    """
    Get a specific user by ID
    
    - **user_id**: User ID to retrieve
    """
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user_data: UserCreate):
    """
    Create a new user
    
    - **name**: User's full name (2-50 characters)
    - **email**: Valid email address
    - **age**: User's age (0-150, optional)
    """
    global user_id_counter
    
    # Check if email already exists
    if find_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = User(
        id=user_id_counter,
        name=user_data.name,
        email=user_data.email,
        age=user_data.age
    )
    
    users_db.append(new_user)
    user_id_counter += 1
    
    return new_user


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(user_id: int, user_data: UserUpdate):
    """
    Update an existing user (full update)
    
    - **user_id**: ID of the user to update
    - **user_data**: Updated user information
    """
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Update fields if provided
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        # Check if new email is already taken by another user
        existing_user = find_user_by_email(user_data.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use by another user"
            )
        user.email = user_data.email
    if user_data.age is not None:
        user.age = user_data.age
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    return user


@app.patch("/users/{user_id}", response_model=User, tags=["Users"])
async def partial_update_user(user_id: int, user_data: UserUpdate):
    """
    Partially update a user (patch)
    
    - **user_id**: ID of the user to update
    - **user_data**: Partial user information to update
    """
    return await update_user(user_id, user_data)


@app.delete("/users/{user_id}", response_model=APIResponse, tags=["Users"])
async def delete_user(user_id: int):
    """
    Delete a user by ID
    
    - **user_id**: ID of the user to delete
    """
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    users_db.remove(user)
    
    return APIResponse(
        success=True,
        message=f"User {user_id} deleted successfully"
    )


# ========================================================================
# ENDPOINTS - PRODUCTS
# ========================================================================

@app.get("/products", response_model=List[Product], tags=["Products"])
async def get_all_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock status"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price")
):
    """
    Get all products with optional filters
    
    - **category**: Filter by product category
    - **in_stock**: Filter by stock availability
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    """
    filtered_products = products_db
    
    if category:
        filtered_products = [p for p in filtered_products if p.category.lower() == category.lower()]
    
    if in_stock is not None:
        filtered_products = [p for p in filtered_products if p.in_stock == in_stock]
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p.price >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p.price <= max_price]
    
    return filtered_products


@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
async def get_product(product_id: int):
    """
    Get a specific product by ID
    
    - **product_id**: Product ID to retrieve
    """
    for product in products_db:
        if product.id == product_id:
            return product
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with ID {product_id} not found"
    )


# ========================================================================
# ENDPOINTS - AUTHENTICATION
# ========================================================================

@app.post("/auth/login", response_model=LoginResponse, tags=["Authentication"])
async def login(credentials: LoginRequest):
    """
    User login endpoint
    
    - **email**: User's email address
    - **password**: User's password (min 6 characters)
    
    Valid test credentials:
    - Email: john@example.com, Password: password123
    - Email: jane@example.com, Password: password123
    """
    # Check if user exists
    user = find_user_by_email(credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Simple password check (in real apps, use proper hashing!)
    if credentials.password != "password123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate fake token
    token = f"fake-jwt-token-{user.id}-{datetime.now().timestamp()}"
    
    return LoginResponse(
        success=True,
        token=token,
        message="Login successful"
    )


# ========================================================================
# ENDPOINTS - PROTECTED (Require API Key)
# ========================================================================

@app.get("/protected/data", tags=["Protected"])
async def get_protected_data(api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """
    Protected endpoint requiring API key
    
    Add header: X-API-Key: test-api-key-12345
    """
    if not verify_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    
    return {
        "message": "This is protected data",
        "data": {
            "secret": "You have access!",
            "timestamp": datetime.now().isoformat()
        }
    }


# ========================================================================
# ENDPOINTS - ERROR TESTING
# ========================================================================

@app.get("/test/error-500", tags=["Testing"])
async def test_server_error():
    """
    Endpoint that always returns 500 error (for testing error handling)
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="This is a simulated internal server error"
    )


@app.get("/test/error-400", tags=["Testing"])
async def test_bad_request():
    """
    Endpoint that always returns 400 error (for testing validation)
    """
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This is a simulated bad request error"
    )


@app.get("/test/slow", tags=["Testing"])
async def test_slow_endpoint():
    """
    Slow endpoint for testing timeouts (delays 3 seconds)
    """
    import asyncio
    await asyncio.sleep(3)
    return {"message": "This endpoint took 3 seconds to respond"}


# ========================================================================
# SERVER STARTUP
# ========================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Sample API Server Starting...")
    print("="*60)
    print("\n📚 Available Endpoints:")
    print("  - http://localhost:8001/")
    print("  - http://localhost:8001/docs (Interactive API Docs)")
    print("  - http://localhost:8001/users")
    print("  - http://localhost:8001/products")
    print("  - http://localhost:8001/auth/login")
    print("\n🔑 Test Credentials:")
    print("  - Email: john@example.com")
    print("  - Password: password123")
    print("\n🔐 API Key for Protected Endpoints:")
    print("  - X-API-Key: test-api-key-12345")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        "sample_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
