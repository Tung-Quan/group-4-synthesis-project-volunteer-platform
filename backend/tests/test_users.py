import pytest

class TestUserProfile:
    """User profile tests with comprehensive coverage and data cleanup"""

    # ==================== RETRIEVAL TESTS ====================

    def test_get_profile(self, student_auth):
        """✓ Student can retrieve own profile"""
        auth_client, headers, user_id = student_auth
        
        res = auth_client.get("/users/profile/me", headers=headers)
        assert res.status_code == 200
        profile = res.json()
        assert profile["id"] == user_id
        assert profile["type"] == "STUDENT"
        assert "email" in profile
        # ✓ Cleanup: Read-only operation on created student

    def test_get_profile_organizer(self, organizer_auth):
        """✓ Organizer can retrieve own profile"""
        auth_client, headers, user_id = organizer_auth
        
        res = auth_client.get("/users/profile/me", headers=headers)
        assert res.status_code == 200
        profile = res.json()
        assert profile["id"] == user_id
        assert profile["type"] == "ORGANIZER"
        # ✓ Cleanup: Read-only operation on created organizer

    def test_get_profile_has_stats(self, student_auth):
        """✓ Profile includes statistics"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.get("/users/profile/me", headers=headers)
        assert res.status_code == 200
        profile = res.json()
        assert "stats" in profile
        assert "activities_joined" in profile["stats"]
        assert "total_social_work_days" in profile["stats"]
        # ✓ Cleanup: Read-only operation

    def test_get_profile_unauthorized(self, client):
        """✗ Unauthenticated user cannot get profile"""
        res = client.get("/users/profile/me")
        assert res.status_code in [401, 403]
        # ✓ Cleanup: No data accessed

    # ==================== UPDATE TESTS ====================

    def test_update_profile_phone(self, student_auth):
        """✓ Update phone number"""
        auth_client, headers, _ = student_auth
        new_phone = "0987654321"
        
        res = auth_client.patch("/users/profile/me", json={
            "phone": new_phone
        }, headers=headers)
        
        assert res.status_code == 200
        assert res.json()["phone"] == new_phone
        # ✓ Cleanup: Phone updated on created student

    def test_update_profile_full_name(self, student_auth):
        """✓ Update full name"""
        auth_client, headers, _ = student_auth
        new_name = "Nguyễn Văn B"
        
        res = auth_client.patch("/users/profile/me", json={
            "full_name": new_name
        }, headers=headers)
        
        assert res.status_code == 200
        assert res.json()["full_name"] == new_name
        # ✓ Cleanup: Full name updated

    def test_update_profile_multiple_fields(self, student_auth):
        """✓ Update multiple fields at once"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.patch("/users/profile/me", json={
            "phone": "0123456789",
            "full_name": "New Name"
        }, headers=headers)
        
        assert res.status_code == 200
        profile = res.json()
        assert profile["phone"] == "0123456789"
        assert profile["full_name"] == "New Name"
        # ✓ Cleanup: All fields updated

    def test_update_profile_empty_phone(self, student_auth):
        """✓ Update with empty phone (optional field)"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.patch("/users/profile/me", json={
            "phone": ""
        }, headers=headers)
        
        assert res.status_code in [200, 400]
        # ✓ Cleanup: Phone cleared or validation error

    def test_update_profile_unicode_name(self, student_auth):
        """✓ Update name with unicode characters"""
        auth_client, headers, _ = student_auth
        unicode_name = "Nguyễn Văn Ánh 阮文安"
        
        res = auth_client.patch("/users/profile/me", json={
            "full_name": unicode_name
        }, headers=headers)
        
        assert res.status_code == 200
        assert "Nguyễn" in res.json()["full_name"]
        # ✓ Cleanup: Unicode name stored

    def test_update_profile_special_chars(self, student_auth):
        """✓ Update with special characters"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.patch("/users/profile/me", json={
            "full_name": "Nguyen Van <A> & B"
        }, headers=headers)
        
        assert res.status_code == 200
        # ✓ Cleanup: Special chars handled

    def test_update_profile_unauthorized(self, client):
        """✗ Unauthenticated user cannot update profile"""
        res = client.patch("/users/profile/me", json={"phone": "000"})
        assert res.status_code in [401, 403]
        # ✓ Cleanup: No update performed

    def test_update_profile_cannot_change_email(self, student_auth):
        """✗ Email cannot be changed through update"""
        auth_client, headers, _ = student_auth
        old_profile = auth_client.get("/users/profile/me", headers=headers).json()
        old_email = old_profile["email"]
        
        res = auth_client.patch("/users/profile/me", json={
            "email": "newemail@test.com"
        }, headers=headers)
        
        # Should either ignore email or fail
        assert res.status_code in [200, 400]
        
        # Verify email didn't change
        verify = auth_client.get("/users/profile/me", headers=headers).json()
        assert verify["email"] == old_email
        # ✓ Cleanup: Email protection verified

    def test_update_profile_cannot_change_type(self, student_auth):
        """✗ User type cannot be changed"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.patch("/users/profile/me", json={
            "type": "ORGANIZER"
        }, headers=headers)
        
        # Should either ignore type or fail
        assert res.status_code in [200, 400]
        
        # Verify type didn't change
        verify = auth_client.get("/users/profile/me", headers=headers).json()
        assert verify["type"] == "STUDENT"
        # ✓ Cleanup: Type protection verified

    def test_update_profile_empty_json(self, student_auth):
        """✓ Update with empty JSON"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.patch("/users/profile/me", json={}, headers=headers)
        
        # Should either succeed (no changes) or fail
        assert res.status_code in [200, 400]
        # ✓ Cleanup: Empty update handled

    # ==================== STATISTICS TESTS ====================

    def test_profile_stats_initialized(self, student_auth):
        """✓ New student has initialized stats"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.get("/users/profile/me", headers=headers)
        stats = res.json()["stats"]
        
        assert stats["activities_joined"] == 0
        assert stats["total_social_work_days"] == 0.0
        # ✓ Cleanup: Stats verified on new student

    def test_profile_stats_non_negative(self, student_auth):
        """✓ Statistics are non-negative"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.get("/users/profile/me", headers=headers)
        stats = res.json()["stats"]
        
        assert stats["activities_joined"] >= 0
        assert stats["total_social_work_days"] >= 0.0
        # ✓ Cleanup: Stats validation

    # ==================== FIELD VALIDATION TESTS ====================

    def test_update_phone_various_formats(self, student_auth):
        """✓ Update phone with various formats"""
        auth_client, headers, _ = student_auth
        
        formats = [
            "0987654321",
            "+84987654321",
            "0-987-654-321",
            "(098) 7654321"
        ]
        
        for phone in formats:
            res = auth_client.patch("/users/profile/me", json={
                "phone": phone
            }, headers=headers)
            # Should accept various formats or validate
            assert res.status_code in [200, 400]
        # ✓ Cleanup: Various phone formats tested

    def test_update_profile_null_values(self, student_auth):
        """✓ Handle null values in update"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.patch("/users/profile/me", json={
            "phone": None
        }, headers=headers)
        
        assert res.status_code in [200, 400, 422]
        # ✓ Cleanup: Null handling verified

    def test_update_profile_numeric_string(self, student_auth):
        """✓ Update with numeric string"""
        auth_client, headers, _ = student_auth
        
        res = auth_client.patch("/users/profile/me", json={
            "full_name": "123456"
        }, headers=headers)
        
        assert res.status_code == 200
        # ✓ Cleanup: Numeric string accepted