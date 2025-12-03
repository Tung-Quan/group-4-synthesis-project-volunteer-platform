# Test Suite Guide - Expanded Test Coverage

## Overview

The test suite has been expanded from **4 basic tests** to **70+ comprehensive tests** organized into 4 test files. Each test includes:
- ✓ Clear test purpose (marked with ✓ for success, ✗ for failure)
- ✓ Test name describing the scenario
- ✓ Assertions validating expected behavior

---

## File Structure

```
tests/
├── test_auth.py              # 21 auth tests
├── test_events.py            # 23 event tests
├── test_applications.py      # 20 application tests
├── test_users.py             # 19 user tests
├── conftest.py               # Fixtures & setup
└── TEST_GUIDE.md             # This file
```

---

## Test Execution

### Run All Tests
```bash
pytest backend/tests/ -v
```

### Run Specific File
```bash
pytest backend/tests/test_auth.py -v
pytest backend/tests/test_events.py -v
pytest backend/tests/test_applications.py -v
pytest backend/tests/test_users.py -v
```

### Run Specific Test Class
```bash
pytest backend/tests/test_auth.py::TestAuth -v
```

### Run Specific Test
```bash
pytest backend/tests/test_auth.py::TestAuth::test_register_student_success -v
```

### Run with Coverage
```bash
pytest backend/tests/ --cov=backend --cov-report=html
```

### Run with Output (see print statements)
```bash
pytest backend/tests/ -v -s
```

---

## Test Categories

### 1. Authentication Tests (`test_auth.py`) - 21 tests

#### Registration Tests (9)
- ✓ `test_register_student_success` - Valid student registration
- ✓ `test_register_organizer_success` - Valid organizer registration
- ✗ `test_register_missing_field` - Missing student_no
- ✗ `test_register_missing_org_no` - Missing organizer_no
- ✗ `test_register_missing_email` - Missing email
- ✗ `test_register_missing_password` - Missing password
- ✗ `test_register_duplicate_email` - Duplicate email (409)
- ✗ `test_register_empty_password` - Empty password
- ✗ `test_register_empty_email` - Empty email

#### Login Tests (6)
- ✓ `test_login_success` - Valid login with correct credentials
- ✗ `test_login_fail_wrong_password` - Wrong password (401)
- ✗ `test_login_fail_nonexistent_user` - Non-existent user (401)
- ✗ `test_login_missing_email` - Missing email (422)
- ✗ `test_login_missing_password` - Missing password (422)
- ✗ `test_login_empty_credentials` - Empty email and password

#### CSRF Tests (2)
- ✓ `test_csrf_token_generation` - CSRF token generated
- ✗ `test_csrf_token_format` - CSRF token is a string

#### Logout Tests (2)
- ✓ `test_logout_success` - Logout succeeds for authenticated user
- ✗ `test_logout_unauthorized` - Logout fails for unauthenticated user

#### Refresh Tests (2)
- ✓ `test_refresh_token_success` - Refresh access token using refresh cookie
- ✗ `test_refresh_token_missing` - Refresh fails without cookie

### 2. Event Tests (`test_events.py`) - 23 tests

#### Read Tests (2)
- ✓ `test_get_all_events` - Get all events list
- ✓ `test_get_all_events_empty` - Empty list handling

#### Create Tests (14)
- ✓ `test_create_event_organizer` - Organizer creates single-slot event
- ✓ `test_create_event_multiple_slots` - Multiple slots
- ✓ `test_create_event_large_capacity` - Large capacity (1000)
- ✓ `test_create_event_with_special_chars` - Special characters in title
- ✓ `test_create_event_zero_reward` - Zero reward (free event)
- ✗ `test_create_event_student_forbidden` - Student cannot create (403)
- ✗ `test_create_event_unauthenticated` - No auth (401/403)
- ✗ `test_create_event_missing_title` - Missing title (422)
- ✗ `test_create_event_empty_title` - Empty title (400/422)
- ✗ `test_create_event_missing_location` - Missing location (422)
- ✗ `test_create_event_no_slots` - No slots (400/201)
- ✗ `test_create_event_past_date` - Past date (400/422)
- ✗ `test_create_event_invalid_time_range` - End before start
- ✗ `test_create_event_zero_capacity` - Zero capacity
- ✗ `test_create_event_negative_capacity` - Negative capacity
- ✗ `test_create_event_negative_reward` - Negative reward

#### Search Tests (1)
- ✓ `test_search_event_basic` - Search by keyword
<!-- - ✓ `test_search_event_empty_query` - Empty query
- ✓ `test_search_event_special_chars` - Special characters -->

#### Slots Tests (3)
- ✓ `test_add_extra_slot` - Organizer adds a new slot to existing event
- ✓ `test_update_slot` - Organizer updates a slot
- ✓ `test_delete_slot` - Organizer deletes a slot

#### FILTER & OWN TESTS (3)
- ✓ `test_get_upcoming_events` - Get upcoming events
- ✓ `test_get_own_events` - Organizer gets their own events
- ✓ `test_get_slot_detail` - User gets slot detail

### 3. Application Tests (`test_applications.py`) - 20 tests

#### Full Workflow Tests (2)
- ✓ `test_full_application_flow` - Complete: create → apply → review → attend
- ✓ `test_full_flow_with_rejection` - Complete: create → apply → reject

#### Application Tests (8)
- ✓ `test_apply_to_event_success` - Student applies successfully
- ✗ `test_apply_missing_event_id` - Missing event_id (422)
- ✗ `test_apply_missing_slot_id` - Missing slot_id (422)
- ✗ `test_apply_nonexistent_event` - Non-existent event (404/400)
- ✓ `test_apply_to_full_slot` - Apply to full capacity slot
- ✗ `test_apply_without_auth` - No authentication (401/403)
- ✓ `test_apply_with_long_note` - Very long note
- ✓ `test_apply_empty_note` - Empty note

#### Review Tests (3)
- ✓ `test_review_approve` - Organizer approves
- ✓ `test_review_reject` - Organizer rejects
- ✗ `test_review_student_cannot_review` - Student cannot review (403)

#### Attendance Tests (3)
- ✓ `test_mark_attendance_present` - Mark as attended
- ✓ `test_mark_attendance_absent` - Mark as absent
- ✗ `test_attendance_student_cannot_mark` - Student cannot mark (403)

#### User Lists & Details (4)
- ✓ `test_student_cancel_application` - Student cancels their application
- ✓ `test_get_history_and_participating` - Get history and participating lists
- ✓ `test_get_history_details` - Get details of a specific history item
- ✓ `test_organizer_get_applications_per_slot` - Organizer views applicants for a slot

### 4. User Profile Tests (`test_users.py`) - 19 tests

#### Retrieval Tests (4)
- ✓ `test_get_profile` - Student gets own profile
- ✓ `test_get_profile_organizer` - Organizer gets own profile
- ✓ `test_get_profile_has_stats` - Profile includes stats
- ✗ `test_get_profile_unauthorized` - No auth (401/403)

#### Update Tests (10)
- ✓ `test_update_profile_phone` - Update phone
- ✓ `test_update_profile_full_name` - Update full name
- ✓ `test_update_profile_multiple_fields` - Update multiple fields
- ✓ `test_update_profile_empty_phone` - Empty phone
- ✓ `test_update_profile_unicode_name` - Unicode characters
- ✓ `test_update_profile_special_chars` - Special characters
- ✗ `test_update_profile_unauthorized` - No auth (401/403)
- ✗ `test_update_profile_cannot_change_email` - Email protection
- ✗ `test_update_profile_cannot_change_type` - Type protection
- ✓ `test_update_profile_empty_json` - Empty JSON

#### Statistics Tests (2)
- ✓ `test_profile_stats_initialized` - New user stats = 0
- ✓ `test_profile_stats_non_negative` - Stats non-negative

#### Field Validation Tests (3)
- ✓ `test_update_phone_various_formats` - Various phone formats
- ✓ `test_update_profile_null_values` - Null values
- ✓ `test_update_profile_numeric_string` - Numeric strings

---

## Test Naming Convention

### Pattern
`test_<feature>_<scenario>_<result>`

### Examples
- `test_register_student_success` → Student registers successfully ✓
- `test_register_duplicate_email` → Duplicate email rejected ✗
- `test_create_event_organizer` → Organizer can create ✓
- `test_create_event_student_forbidden` → Student cannot create ✗
- `test_apply_missing_event_id` → Apply fails without event_id ✗

### Symbols
- ✓ Success test (happy path)
- ✗ Failure test (error handling)

---

## Expected Status Codes

### Success Responses
```
200 OK              - Most successful operations
201 Created         - Event creation, successful registration
```

### Error Responses
```
400 Bad Request     - Invalid input (e.g., zero capacity)
401 Unauthorized    - Missing authentication
403 Forbidden       - Insufficient permissions, invalid CSRF
404 Not Found       - Non-existent resource
409 Conflict        - Duplicate entry (email)
422 Validation Error - Missing required fields
```

---

## Common Test Patterns

### Pattern 1: Simple Success Test
```python
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
    # User created with random email
```

### Pattern 2: With Authentication
```python
def test_create_event_organizer(self, organizer_auth):
    """✓ Organizer can create event"""
    auth_client, headers, _ = organizer_auth
    
    payload = {...}
    res = auth_client.post("/events/", json=payload, headers=headers)
    assert res.status_code == 201
    # Event created with random organizer
```

### Pattern 3: Error Scenario
```python
def test_apply_missing_event_id(self, student_auth):
    """✗ Apply fails without event_id"""
    stu_client, stu_headers, _ = student_auth
    
    res = stu_client.post("/applications/apply", json={
        "slot_id": "some_id", "note": "test"
    }, headers=stu_headers)
    
    assert res.status_code == 422
    # Invalid request, no application created
```

### Pattern 4: Full Workflow
```python
def test_full_application_flow(self, organizer_auth, student_auth):
    """✓ Complete workflow: create → apply → review → attend"""
    org_client, org_headers, _ = organizer_auth
    stu_client, stu_headers, stu_id = student_auth
    
    # Step 1: Create event
    # Step 2: Apply
    # Step 3: Review
    # Step 4: Attend
    # Full workflow completed
```

---

## Debugging Tips

### View Print Statements
```bash
pytest -s backend/tests/test_auth.py::TestAuth::test_login_success
```

### Stop on First Failure
```bash
pytest -x backend/tests/
```

### Run Last Failed Tests
```bash
pytest --lf backend/tests/
```

### Verbose Diff
```bash
pytest -vv backend/tests/test_auth.py::TestAuth::test_login_success
```

### Debugger on Failure
```bash
pytest --pdb backend/tests/test_auth.py::TestAuth::test_login_success
```

---

## Test Execution Order

Tests are independent and can run in any order:

```bash
# All tests (any order)
pytest backend/tests/ -v

# Class tests (in order)
pytest backend/tests/test_auth.py::TestAuth -v

# Specific test
pytest backend/tests/test_auth.py::TestAuth::test_register_student_success -v
```

---

## Coverage Report

Generate HTML coverage report:

```bash
pytest backend/tests/ --cov=backend --cov-report=html
```

Open `htmlcov/index.html` to view coverage details.

### Expected Coverage
- Auth endpoints: ~95%
- Event endpoints: ~90%
- Application endpoints: ~90%
- User endpoints: ~90%

---

## Test Maintenance

### Adding New Tests

1. Follow naming convention: `test_<feature>_<scenario>`
2. Add docstring with ✓/✗ indicator
3. Use fixtures for auth:
   ```python
   def test_new_feature(self, organizer_auth, student_auth):
       org_client, org_headers, _ = organizer_auth
       stu_client, stu_headers, _ = student_auth
   ```

### Updating Tests

- Maintain status code expectations
- Update assertions if API changes
- Keep test names descriptive

### Failing Tests

If a test fails:
1. Check error message
2. Verify fixture setup
3. Check database state
4. Review API response
5. Update assertions if needed

---

## Fixture Reference

From `conftest.py`:

```python
# Basic client (no auth)
client

# CSRF headers for POST/PATCH/DELETE
csrf_headers

# Organizer auth tuple (client, headers, user_id)
organizer_auth

# Student auth tuple (client, headers, user_id)
student_auth
```

---

## Summary

- **80+ comprehensive tests** across 4 test files
- **Clear test purposes** with ✓/✗ indicators
- **Organized by functionality** (auth, events, applications, users)
- **Error scenarios covered** for validation and security
- **Easy to maintain** with consistent naming and structure
- **Ready for CI/CD** integration

---

**Last Updated**: December 3, 2025  
**Total Tests**: 60+  
**Status**: ✅ Ready for Use
