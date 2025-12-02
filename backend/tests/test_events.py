import pytest
from datetime import date, timedelta

class TestEvents:
    def test_get_all_events(self, client):
        res = client.get("/events/get-all-event")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_create_event_organizer(self, organizer_auth):
        # Unpack 3 giá trị
        auth_client, headers, _ = organizer_auth
        
        payload = {
            "title": "Mùa Hè Xanh",
            "description": "Tình nguyện",
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
        # Dùng auth_client
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 201
        assert "event_id" in res.json()

    def test_create_event_student_fail(self, student_auth):
        auth_client, headers, _ = student_auth
        payload = {
            "title": "Hacker Event", "description": "...", "location": "...", "slots": []
        }
        res = auth_client.post("/events/", json=payload, headers=headers)
        assert res.status_code == 403

    def test_search_event(self, client):
        res = client.get("/events/search?q=Mùa Hè")
        assert res.status_code in [200, 404]