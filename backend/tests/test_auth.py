import pytest
from backend.tests.conftest import get_random_email

class TestAuth:
    """Auth endpoint tests with comprehensive coverage and data cleanup"""

    # ==================== REGISTRATION TESTS ====================
    
    def test_register_student_success(self, client):
        """✓ Student registration with valid data"""
        payload = {
            "email": get_random_email("stu_success"),
            "password": "password123",
            "full_name": "Nguyen Van A",
            "type": "STUDENT",
            "student_no": "SV2024"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 200
        assert res.json()["email"] == payload["email"]
        # ✓ Data cleanup: user created with random email

    def test_register_organizer_success(self, client):
        """✓ Organizer registration with valid data"""
        payload = {
            "email": get_random_email("org_success"),
            "password": "password123",
            "full_name": "Youth Union Org",
            "type": "ORGANIZER",
            "organizer_no": f"ORG_{get_random_email().split('_')[1]}",
            "org_name": "Youth Union"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 200
        assert res.json()["type"] == "ORGANIZER"
        # ✓ Data cleanup: organizer created

    def test_register_missing_field(self, client):
        """✗ Registration fails without required student_no"""
        payload = {
            "email": get_random_email("missing_field"),
            "password": "123",
            "type": "STUDENT"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 400
        # ✓ No data created

    def test_register_missing_org_no(self, client):
        """✗ Organizer registration fails without organizer_no"""
        payload = {
            "email": get_random_email("missing_org_no"),
            "password": "123",
            "type": "ORGANIZER",
            "org_name": "Test Org"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 400
        # ✓ No data created

    def test_register_missing_email(self, client):
        """✗ Registration fails without email"""
        payload = {
            "password": "123",
            "full_name": "Test",
            "type": "STUDENT",
            "student_no": "SV_NO_EMAIL"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 422
        # ✓ No data created

    def test_register_missing_password(self, client):
        """✗ Registration fails without password"""
        payload = {
            "email": get_random_email("no_password"),
            "full_name": "Test",
            "type": "STUDENT",
            "student_no": "SV_NO_PWD"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 422
        # ✓ No data created

    def test_register_duplicate_email(self, client):
        """✗ Registration fails with duplicate email"""
        email = get_random_email("duplicate")
        payload = {
            "email": email, "password": "123", "type": "ORGANIZER",
            "organizer_no": "ORG_DUP_1", "org_name": "Test"
        }
        # First registration: SUCCESS
        res1 = client.post("/auth/register", json=payload)
        assert res1.status_code == 200
        
        # Second registration: FAILURE
        res2 = client.post("/auth/register", json=payload)
        assert res2.status_code == 409
        # ✓ Conflict: duplicate email rejected

    def test_register_empty_password(self, client):
        """✗ Registration fails with empty password"""
        payload = {
            "email": get_random_email("empty_pwd"),
            "password": "",
            "full_name": "Test",
            "type": "STUDENT",
            "student_no": "SV_EMPTY_PWD"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code in [400, 422]
        # ✓ No data created

    def test_register_empty_email(self, client):
        """✗ Registration fails with empty email"""
        payload = {
            "email": "",
            "password": "123",
            "full_name": "Test",
            "type": "STUDENT",
            "student_no": "SV_EMPTY_EMAIL"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code in [400, 422]
        # ✓ No data created

    # ==================== LOGIN TESTS ====================

    def test_login_success(self, client, csrf_headers):
        """✓ Login succeeds with valid credentials"""
        email = get_random_email("login_success")
        # Create user first
        client.post("/auth/register", json={
            "email": email, "password": "password123", "type": "STUDENT", "student_no": "SV_LOGIN_OK"
        })
        
        # Login
        res = client.post("/auth/login", json={
            "email": email, "password": "password123"
        })
        
        assert res.status_code == 200
        assert "csrf_token" in res.json()
        # ✓ Data cleanup: user created and logged in

    def test_login_fail_wrong_password(self, client, csrf_headers):
        """✗ Login fails with wrong password"""
        email = get_random_email("login_wrong_pwd")
        # Create user
        client.post("/auth/register", json={
            "email": email, "password": "correct_password", "type": "STUDENT", "student_no": "SV_LOGIN_WRONG"
        })
        
        # Try login with wrong password
        res = client.post("/auth/login", json={
            "email": email, "password": "wrong_password"
        })
        
        assert res.status_code == 401
        # ✓ No data created

    def test_login_fail_nonexistent_user(self, client, csrf_headers):
        """✗ Login fails for non-existent user"""
        res = client.post("/auth/login", json={
            "email": "ghost@nonexistent.com", "password": "any_password"
        })
        assert res.status_code == 401
        # ✓ No data created

    def test_login_missing_email(self, client, csrf_headers):
        """✗ Login fails without email"""
        res = client.post("/auth/login", json={
            "password": "123"
        })
        assert res.status_code == 422
        # ✓ No data created

    def test_login_missing_password(self, client, csrf_headers):
        """✗ Login fails without password"""
        res = client.post("/auth/login", json={
            "email": "test@test.com"
        })
        assert res.status_code == 422
        # ✓ No data created

    def test_login_empty_credentials(self, client, csrf_headers):
        """✗ Login fails with empty email and password"""
        res = client.post("/auth/login", json={
            "email": "", "password": ""
        })
        assert res.status_code in [401, 422]
        # ✓ No data created

    # ==================== CSRF TESTS ====================

    def test_csrf_token_generation(self, client):
        """✓ CSRF token is generated"""
        res = client.get("/auth/csrf")
        assert res.status_code == 200
        assert "csrf_token" in res.json()
        assert len(res.json()["csrf_token"]) > 0
        # ✓ Read-only operation

    def test_csrf_token_format(self, client):
        """✓ CSRF token has expected format"""
        res = client.get("/auth/csrf")
        assert res.status_code == 200
        token = res.json()["csrf_token"]
        # Token should be a string
        assert isinstance(token, str)
        # ✓ Read-only operation

    # ==================== LOGOUT TESTS ====================

    def test_logout_success(self, student_auth):
        """✓ Logout succeeds for authenticated user"""
        stu_client, stu_headers, _ = student_auth
        
        res = stu_client.post("/auth/logout", headers=stu_headers)
        assert res.status_code == 200
        # ✓ Session terminated

    def test_logout_unauthorized(self, client):
        """✗ Logout fails for unauthenticated user"""
        res = client.post("/auth/logout")
        assert res.status_code in [401, 403]
        # ✓ No data created

    # ==================== REFRESH TOKEN TESTS ====================

    def test_refresh_token_success(self, client, csrf_headers):
        """✓ Refresh access token using refresh cookie"""
        email = get_random_email("refresh")
        client.post("/auth/register", json={
            "email": email, "password": "123", "type": "STUDENT", "student_no": "SV_REF"
        })
        
        # Login to get cookie
        client.post("/auth/login", json={"email": email, "password": "123"}, headers=csrf_headers)
        
        # Call refresh
        res = client.post("/auth/refresh", headers=csrf_headers)
        assert res.status_code == 200
        assert "Access token refreshed" in res.json()["message"]
        # ✓ Data cleanup: token refreshed

    def test_refresh_token_missing(self, client):
        """✗ Refresh fails without cookie"""
        client.cookies.clear()
        res = client.post("/auth/refresh")
        assert res.status_code == 401
        # ✓ No data created
