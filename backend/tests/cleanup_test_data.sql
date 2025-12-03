-- Cleanup Test Data
-- This script removes all test data created during test execution
-- Test data is identified by full_name pattern 'Test _*' or similar patterns

-- Remove applications
DELETE FROM applications
WHERE student_user_id IN (
    SELECT id FROM users 
    WHERE email LIKE '%@test.com'
       OR full_name IN 'Test Stu'
);

-- Remove events created by test users
DELETE FROM events
WHERE organizer_user_id IN (
       SELECT id FROM users 
       WHERE email LIKE '%@test.com' 
          OR full_name = 'Test Org'
   );

-- Remove test users
DELETE FROM users
WHERE email LIKE '%@test.com'
  OR email in ('login_success', 'login_wrong_pwd')
   OR full_name IN ('Test Org', 'Test Stu', 'Login Test', 'Test');
