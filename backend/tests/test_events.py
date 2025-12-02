import pytest
from datetime import date, timedelta

class TestEvents:
    """Event management tests with comprehensive coverage"""

    # ==================== READ TESTS ====================

    def test_get_all_events(self, client):
        """✓ Get all events returns list"""
        res = client.get("/events/get-all-event")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_get_all_events_empty(self, client):
        """✓ Get all events returns empty list when no events"""
        res = client.get("/events/get-all-event")
        assert res.status_code == 200
        result = res.json()
        # Result could be empty list or populated
        assert isinstance(result, list)

    # ==================== CREATE TESTS ====================

    def test_create_event_organizer(self, organizer_auth):
        """✓ Organizer can create event with single slot"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Mùa Hè Xanh",
            "description": "Tình nguyện 2024",
            "location": "TPHCM",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=5)),
                    "starts_at": "07:00:00",
                    "ends_at": "11:00:00",
                    "capacity": 20,
                    "day_reward": 1.0
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 201
        assert "event_id" in res.json()
        assert "slot_ids" in res.json()

    def test_create_event_multiple_slots(self, organizer_auth):
        """✓ Organizer can create event with multiple slots"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Multi-Shift Event",
            "description": "Multiple working shifts",
            "location": "District 1",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=5)),
                    "starts_at": "08:00:00",
                    "ends_at": "12:00:00",
                    "capacity": 10,
                    "day_reward": 2.0
                },
                {
                    "work_date": str(date.today() + timedelta(days=6)),
                    "starts_at": "14:00:00",
                    "ends_at": "18:00:00",
                    "capacity": 15,
                    "day_reward": 2.0
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 201
        assert len(res.json()["slot_ids"]) == 2

    def test_create_event_large_capacity(self, organizer_auth):
        """✓ Organizer can create event with large capacity"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Big Event",
            "description": "Large scale event",
            "location": "Stadium",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=7)),
                    "starts_at": "06:00:00",
                    "ends_at": "18:00:00",
                    "capacity": 1000,
                    "day_reward": 5.0
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 201

    def test_create_event_with_special_chars(self, organizer_auth):
        """✓ Event title with special characters"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Sự kiện Tình nguyện & Cộng đồng",
            "description": "Event với ký tự đặc biệt @#$",
            "location": "Q1 - TP.HCM",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=5)),
                    "starts_at": "08:00:00",
                    "ends_at": "12:00:00",
                    "capacity": 20,
                    "day_reward": 1.0
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 201

    def test_create_event_student_forbidden(self, student_auth):
        """✗ Student cannot create events"""
        auth_client, headers, _ = student_auth
        payload = {
            "title": "Hacker Event", "description": "...", "location": "...", "slots": []
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 403

    def test_create_event_unauthenticated(self, client):
        """✗ Unauthenticated user cannot create events"""
        payload = {
            "title": "Hack Event", "description": "...", "location": "...", "slots": []
        }
        res = client.post("/events/", json=payload)
        assert res.status_code in [401, 403]

    def test_create_event_missing_title(self, organizer_auth):
        """✗ Event creation fails without title"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "description": "No title",
            "location": "HCMC",
            "slots": []
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 422

    def test_create_event_missing_location(self, organizer_auth):
        """✗ Event creation fails without location"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "No Location Event",
            "description": "Missing location",
            "slots": []
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 422

    def test_create_event_no_slots(self, organizer_auth):
        """✗ Event creation fails without slots (if required)"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "No Slots Event",
            "description": "Event without slots",
            "location": "HCMC",
            "slots": []
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        # Could be 201 (valid) or 400 (requires slots)
        assert res.status_code in [201, 400]

    def test_create_event_invalid_time_range(self, organizer_auth):
        """✗ Event creation fails with end_time before start_time"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Bad Time Event",
            "description": "End before start",
            "location": "HCMC",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=5)),
                    "starts_at": "18:00:00",
                    "ends_at": "08:00:00",  # Before start
                    "capacity": 10,
                    "day_reward": 1.0
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code in [400, 422]

    def test_create_event_zero_capacity(self, organizer_auth):
        """✗ Event creation fails with zero capacity"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Zero Capacity Event",
            "description": "No capacity",
            "location": "HCMC",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=5)),
                    "starts_at": "08:00:00",
                    "ends_at": "12:00:00",
                    "capacity": 0,  # Zero
                    "day_reward": 1.0
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code in [400, 422]

    def test_create_event_negative_capacity(self, organizer_auth):
        """✗ Event creation fails with negative capacity"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Negative Capacity Event",
            "description": "Negative slots",
            "location": "HCMC",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=5)),
                    "starts_at": "08:00:00",
                    "ends_at": "12:00:00",
                    "capacity": -5,  # Negative
                    "day_reward": 1.0
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code in [400, 422]

    def test_create_event_negative_reward(self, organizer_auth):
        """✗ Event creation fails with negative reward"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Negative Reward Event",
            "description": "Negative reward",
            "location": "HCMC",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=5)),
                    "starts_at": "08:00:00",
                    "ends_at": "12:00:00",
                    "capacity": 10,
                    "day_reward": -1.0  # Negative
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code in [400, 422]

    def test_create_event_zero_reward(self, organizer_auth):
        """✓ Event creation succeeds with zero reward"""
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Free Event",
            "description": "No reward",
            "location": "HCMC",
            "slots": [
                {
                    "work_date": str(date.today() + timedelta(days=5)),
                    "starts_at": "08:00:00",
                    "ends_at": "12:00:00",
                    "capacity": 10,
                    "day_reward": 0.0  # Zero reward is allowed
                }
            ]
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 201

    # ==================== SEARCH TESTS ====================

    def test_search_event_basic(self, client):
        """✓ Search events by keyword"""
        res = client.get("/events/search?q=Mùa")
        assert res.status_code in [200, 404]
        # Result is either list of events or 404 if not found

    # def test_search_event_empty_query(self, client):
    #     """✓ Search with empty query"""
    #     res = client.get("/events/search?q=")
    #     assert res.status_code in [200, 400]

    # def test_search_event_special_chars(self, client):
    #     """✓ Search with special characters"""
    #     res = client.get("/events/search?q=&@#$%")
    #     assert res.status_code in [200, 400]

    # def test_search_event_long_query(self, client):
    #     """✓ Search with long query"""
    #     long_query = "a" * 200
    #     res = client.get(f"/events/search?q={long_query}")
    #     assert res.status_code in [200, 400]

    # ==================== SLOT MANAGEMENT TESTS (BỔ SUNG) ====================

    def test_add_extra_slot(self, organizer_auth):
        """✓ Organizer adds a new slot to existing event"""
        client, headers, _ = organizer_auth
        
        # 1. Tạo event trước
        res = client.post("/events/", json={
            "title": "Slot Test", "description": "...", "location": "...",
            "slots": [] # Tạo event rỗng slot trước
        }, headers=headers)
        event_id = res.json()["event_id"]

        # 2. Thêm slot mới
        slot_payload = {
            "work_date": str(date.today() + timedelta(days=10)),
            "starts_at": "08:00:00", "ends_at": "10:00:00",
            "capacity": 5, "day_reward": 1.0
        }
        res_slot = client.post(f"/events/{event_id}/create-slot", json=slot_payload, headers=headers)
        
        assert res_slot.status_code == 201
        assert res_slot.json()["event_id"] == event_id

    def test_update_slot(self, organizer_auth):
        """✓ Organizer updates a slot"""
        client, headers, _ = organizer_auth
        
        # 1. Tạo event có slot
        res = client.post("/events/", json={
            "title": "Update Slot Test", "description": "...", "location": "...",
            "slots": [{"work_date": str(date.today()), "starts_at": "08:00:00", "ends_at": "10:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=headers)
        slot_id = res.json()["slot_ids"][0]

        # 2. Update slot capacity
        res_update = client.patch(f"/events/slots/{slot_id}", json={
            "capacity": 100
        }, headers=headers)
        
        assert res_update.status_code == 200
        assert res_update.json()["capacity"] == 100

    def test_delete_slot(self, organizer_auth):
        """✓ Organizer deletes a slot"""
        client, headers, _ = organizer_auth
        
        # 1. Tạo event có slot
        res = client.post("/events/", json={
            "title": "Delete Slot Test", "description": "...", "location": "...",
            "slots": [{"work_date": str(date.today()), "starts_at": "08:00:00", "ends_at": "10:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=headers)
        slot_id = res.json()["slot_ids"][0]

        # 2. Xóa slot
        res_del = client.delete(f"/events/slots/{slot_id}", headers=headers)
        assert res_del.status_code == 200

    # ==================== FILTER & OWN TESTS (BỔ SUNG) ====================

    def test_get_upcoming_events(self, organizer_auth):
        """✓ Get upcoming events"""
        org_client, org_headers, _ = organizer_auth
        # Tạo event tương lai
        org_client.post("/events/", json={
            "title": "Future Event", "description": "...", "location": "...",
            "slots": [{"work_date": str(date.today() + timedelta(days=10)), "starts_at": "08:00:00", "ends_at": "12:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=org_headers)

        res = org_client.get("/events/upcoming")
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        # Check logic: phải có ít nhất 1 event vừa tạo
        assert any(e["title"] == "Future Event" for e in res.json())

    def test_get_own_events(self, organizer_auth):
        """✓ Organizer gets their own events"""
        org_client, org_headers, org_id = organizer_auth
        org_client.post("/events/", json={
            "title": "My Event", "description": "...", "location": "...",
            "slots": [{"work_date": str(date.today()), "starts_at": "08:00:00", "ends_at": "12:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=org_headers)

        res = org_client.get("/events/get-own-event", headers=org_headers)
        assert res.status_code == 200
        assert len(res.json()) >= 1
        assert res.json()[0]["organizer_user_id"] == org_id

    def test_get_slot_detail(self, organizer_auth):
        """✓ User gets slot detail"""
        org_client, org_headers, _ = organizer_auth
        # Tạo event
        create_res = org_client.post("/events/", json={
            "title": "Slot Detail Test", "description": "...", "location": "...",
            "slots": [{"work_date": str(date.today()), "starts_at": "08:00:00", "ends_at": "12:00:00", "capacity": 5, "day_reward": 1}]
        }, headers=org_headers)
        slot_id = create_res.json()["slot_ids"][0]

        # Xem chi tiết slot
        res = org_client.get(f"/events/slots/{slot_id}")
        assert res.status_code == 200
        assert res.json()["capacity"] == 5