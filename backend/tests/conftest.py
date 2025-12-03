import pytest
from fastapi.testclient import TestClient
from backend.main import app 
import random

# Helper function for random email pattern
def get_random_email(prefix="user"):
    return f"{prefix}_{random.randint(10000, 99999)}@test.com"

# --- Client for ORGANIZER ---
@pytest.fixture(scope="function")
def organizer_client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def organizer_auth(organizer_client):
    email = get_random_email("org")
    password = "123"
    
    # Register
    organizer_client.post("/auth/register", json={
        "email": email, "password": password, "full_name": "Test Org",
        "type": "ORGANIZER", 
        "organizer_no": f"ORG_{random.randint(1000,9999)}", 
        "org_name": "Youth Union"
    })
    
    # Login
    init_res = organizer_client.get("/auth/csrf")
    init_token = init_res.json()["csrf_token"]
    
    login_res = organizer_client.post("/auth/login", json={
        "email": email, "password": password
    }, headers={"X-CSRF-Token": init_token})
    
    new_token = login_res.json()["csrf_token"]
    user_id = login_res.json()["user"]["id"]
    
    # return logined CLIENT
    return organizer_client, {"X-CSRF-Token": new_token}, user_id

# --- Client for STUDENT ---
@pytest.fixture(scope="function")
def student_client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def student_auth(student_client):
    email = get_random_email("stu")
    password = "123"
    
    student_client.post("/auth/register", json={
        "email": email, "password": password, "full_name": "Test Stu",
        "type": "STUDENT", 
        "student_no": f"SV_{random.randint(1000,9999)}"
    })
    
    init_res = student_client.get("/auth/csrf")
    init_token = init_res.json()["csrf_token"]
    
    login_res = student_client.post("/auth/login", json={
        "email": email, "password": password
    }, headers={"X-CSRF-Token": init_token})
    
    new_token = login_res.json()["csrf_token"]
    user_id = login_res.json()["user"]["id"]
    
    return student_client, {"X-CSRF-Token": new_token}, user_id

# Client for simple test
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def csrf_headers(client):
    response = client.get("/auth/csrf")
    token = response.json()["csrf_token"]
    return {"X-CSRF-Token": token}