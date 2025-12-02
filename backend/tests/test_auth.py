import pytest
from backend.tests.conftest import get_random_email

class TestAuth:
    # 1. Test Đăng ký thành công (Student)
    def test_register_student_success(self, client):
        payload = {
            "email": get_random_email(),
            "password": "password123",
            "full_name": "Nguyen Van A",
            "type": "STUDENT",
            "student_no": "SV2024"
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 200
        assert res.json()["email"] == payload["email"]

    # 2. Test Đăng ký thất bại (Thiếu thông tin bắt buộc)
    def test_register_missing_field(self, client):
        payload = {
            "email": get_random_email(),
            "password": "123",
            "type": "STUDENT"
            # Thiếu student_no
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 400

    # 3. Test Đăng ký thất bại (Email trùng)
    def test_register_duplicate_email(self, client):
        email = get_random_email()
        payload = {
            "email": email, "password": "123", "type": "ORGANIZER", 
            "organizer_no": "ORG1", "org_name": "Test"
        }
        # Lần 1: Thành công
        client.post("/auth/register", json=payload)
        # Lần 2: Thất bại
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 409

    # 4. Test Đăng nhập
    def test_login_success(self, client, csrf_headers):
        # Tạo user trước
        email = get_random_email()
        client.post("/auth/register", json={
            "email": email, "password": "123", "type": "STUDENT", "student_no": "SV1"
        })
        
        # Login
        res = client.post("/auth/login", json={
            "email": email, "password": "123"
        }, headers=csrf_headers)
        
        assert res.status_code == 200
        assert "access_token" in client.cookies
        assert "csrf_token" in res.json() # Phải trả về token mới

    # 5. Test Đăng nhập sai mật khẩu
    def test_login_fail(self, client, csrf_headers):
        res = client.post("/auth/login", json={
            "email": "ghost@test.com", "password": "wrong"
        }, headers=csrf_headers)
        assert res.status_code == 401