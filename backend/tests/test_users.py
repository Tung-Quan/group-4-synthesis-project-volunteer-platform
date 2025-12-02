import pytest

def test_get_profile(student_auth):
    # Unpack 3 giá trị (Client, Headers, UserID)
    auth_client, headers, user_id = student_auth
    
    # Dùng auth_client để gọi
    res = auth_client.get("/users/profile/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["id"] == user_id
    assert res.json()["type"] == "STUDENT"

def test_update_profile(student_auth):
    auth_client, headers, _ = student_auth
    new_phone = "0123456789"
    
    res = auth_client.patch("/users/profile/me", json={
        "phone": new_phone
    }, headers=headers)
    
    assert res.status_code == 200
    assert res.json()["phone"] == new_phone

def test_update_profile_unauthorized(client):
    res = client.patch("/users/profile/me", json={"phone": "000"})
    assert res.status_code in [401, 403]