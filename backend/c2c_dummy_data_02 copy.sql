BEGIN;

-- Làm sạch dữ liệu cũ
TRUNCATE TABLE
  student_service_ledger,
  notifications,
  ratings,
  student_saved_events,
  applications,
  event_slots,
  events,
  organizers,
  students,
  consents,
  audit_logs,
  users
RESTART IDENTITY CASCADE;

-- =========================
-- 1) USERS: 15 volunteers (STUDENT) + 15 organizers (ORGANIZER)
-- =========================
-- Đã thêm cột 'type' khớp với ENUM('STUDENT', 'ORGANIZER') trong schema
INSERT INTO users (email, password_hash, full_name, phone, type)
VALUES
  -- Volunteers -> STUDENT
  ('volunteer01@example.com','hashed_pw','Volunteer 01','+840100000001', 'STUDENT'),
  ('volunteer02@example.com','hashed_pw','Volunteer 02','+840100000002', 'STUDENT'),
  ('volunteer03@example.com','hashed_pw','Volunteer 03','+840100000003', 'STUDENT'),
  ('volunteer04@example.com','hashed_pw','Volunteer 04','+840100000004', 'STUDENT'),
  ('volunteer05@example.com','hashed_pw','Volunteer 05','+840100000005', 'STUDENT'),
  ('volunteer06@example.com','hashed_pw','Volunteer 06','+840100000006', 'STUDENT'),
  ('volunteer07@example.com','hashed_pw','Volunteer 07','+840100000007', 'STUDENT'),
  ('volunteer08@example.com','hashed_pw','Volunteer 08','+840100000008', 'STUDENT'),
  ('volunteer09@example.com','hashed_pw','Volunteer 09','+840100000009', 'STUDENT'),
  ('volunteer10@example.com','hashed_pw','Volunteer 10','+840100000010', 'STUDENT'),
  ('volunteer11@example.com','hashed_pw','Volunteer 11','+840100000011', 'STUDENT'),
  ('volunteer12@example.com','hashed_pw','Volunteer 12','+840100000012', 'STUDENT'),
  ('volunteer13@example.com','hashed_pw','Volunteer 13','+840100000013', 'STUDENT'),
  ('volunteer14@example.com','hashed_pw','Volunteer 14','+840100000014', 'STUDENT'),
  ('volunteer15@example.com','hashed_pw','Volunteer 15','+840100000015', 'STUDENT'),

  -- Organizers -> ORGANIZER
  ('org01@example.com','hashed_pw','Organizer 01','+840200000001', 'ORGANIZER'),
  ('org02@example.com','hashed_pw','Organizer 02','+840200000002', 'ORGANIZER'),
  ('org03@example.com','hashed_pw','Organizer 03','+840200000003', 'ORGANIZER'),
  ('org04@example.com','hashed_pw','Organizer 04','+840200000004', 'ORGANIZER'),
  ('org05@example.com','hashed_pw','Organizer 05','+840200000005', 'ORGANIZER'),
  ('org06@example.com','hashed_pw','Organizer 06','+840200000006', 'ORGANIZER'),
  ('org07@example.com','hashed_pw','Organizer 07','+840200000007', 'ORGANIZER'),
  ('org08@example.com','hashed_pw','Organizer 08','+840200000008', 'ORGANIZER'),
  ('org09@example.com','hashed_pw','Organizer 09','+840200000009', 'ORGANIZER'),
  ('org10@example.com','hashed_pw','Organizer 10','+840200000010', 'ORGANIZER'),
  ('org11@example.com','hashed_pw','Organizer 11','+840200000011', 'ORGANIZER'),
  ('org12@example.com','hashed_pw','Organizer 12','+840200000012', 'ORGANIZER'),
  ('org13@example.com','hashed_pw','Organizer 13','+840200000013', 'ORGANIZER'),
  ('org14@example.com','hashed_pw','Organizer 14','+840200000014', 'ORGANIZER'),
  ('org15@example.com','hashed_pw','Organizer 15','+840200000015', 'ORGANIZER');

-- =========================
-- 2) ROLE TABLES (Students & Organizers)
-- =========================
-- Volunteers -> students table
INSERT INTO students (user_id, student_no, social_work_days)
SELECT id,
       'VOL' || LPAD((ROW_NUMBER() OVER (ORDER BY email))::text, 4, '0'),
       0
FROM users
WHERE type = 'STUDENT'; -- Lọc theo type vừa insert

-- Organizers -> organizers table
INSERT INTO organizers (user_id, organizer_no, org_name)
SELECT id,
       'ORG' || LPAD((ROW_NUMBER() OVER (ORDER BY email))::text, 4, '0'),
       'Organization ' || LPAD((ROW_NUMBER() OVER (ORDER BY email))::text, 2, '0')
FROM users
WHERE type = 'ORGANIZER'; -- Lọc theo type vừa insert

-- (Tuỳ chọn) consents cho 10 user đầu theo email
INSERT INTO consents (user_id, email_marketing, data_sharing)
SELECT id, (ROW_NUMBER() OVER (ORDER BY email)) % 2 = 0, TRUE
FROM users
ORDER BY email
LIMIT 10;

-- =========================
-- 3) EVENTS (10 events: org01..org05, mỗi org 2 event)
-- =========================
INSERT INTO events (organizer_user_id, title, description, location, status)
VALUES
  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org01@example.com'),
    'E1 Community Clean-up','Pick trash & recycle','District 1','published'),
  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org01@example.com'),
    'E2 Park Tree Care','Water & prune trees','District 3','published'),

  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org02@example.com'),
    'E3 Food Drive','Sort & pack food','District 5','published'),
  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org02@example.com'),
    'E4 Riverbank Cleanup','Remove debris','Thu Duc City','published'),

  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org03@example.com'),
    'E5 Elderly Support','Visit nursing home','Go Vap','published'),
  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org03@example.com'),
    'E6 School Painting','Paint classrooms','Binh Thanh','published'),

  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org04@example.com'),
    'E7 Library Sorting','Catalogue books','District 10','published'),
  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org04@example.com'),
    'E8 Beach Clean-up','Collect plastic waste','Can Gio','published'),

  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org05@example.com'),
    'E9 Traffic Safety','Assist crossings','District 7','published'),
  ((SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org05@example.com'),
    'E10 Blood Donation','Registration support','District 4','published');

-- =========================
-- 4) EVENT SLOTS (mỗi event 2 slot)
-- =========================
WITH ev AS (SELECT id FROM events)
INSERT INTO event_slots (event_id, starts_at, ends_at, capacity, day_reward)
SELECT id,
       (date_trunc('day', now()) + interval '1 day' + time '09:00'),
       (date_trunc('day', now()) + interval '1 day' + time '12:00'),
       20, 1.0
FROM ev
UNION ALL
SELECT id,
       (date_trunc('day', now()) + interval '1 day' + time '13:30'),
       (date_trunc('day', now()) + interval '1 day' + time '17:00'),
       20, 1.0
FROM ev;

-- =========================
-- 5) APPLICATIONS (volunteers apply vào các event/slot)
-- =========================
INSERT INTO applications (event_id, student_user_id, slot_id, note, status)
VALUES
  -- volunteer01..10 -> E1..E10 (slot 1)
  ((SELECT id FROM events WHERE title='E1 Community Clean-up'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer01@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E1 Community Clean-up' ORDER BY s1.starts_at LIMIT 1),
   'Ready to help','applied'),

  ((SELECT id FROM events WHERE title='E2 Park Tree Care'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer02@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E2 Park Tree Care' ORDER BY s1.starts_at LIMIT 1),
   'Love trees','applied'),

  ((SELECT id FROM events WHERE title='E3 Food Drive'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer03@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E3 Food Drive' ORDER BY s1.starts_at LIMIT 1),
   'Can lift boxes','applied'),

  ((SELECT id FROM events WHERE title='E4 Riverbank Cleanup'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer04@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E4 Riverbank Cleanup' ORDER BY s1.starts_at LIMIT 1),
   'Near my home','applied'),

  ((SELECT id FROM events WHERE title='E5 Elderly Support'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer05@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E5 Elderly Support' ORDER BY s1.starts_at LIMIT 1),
   'Have experience','applied'),

  ((SELECT id FROM events WHERE title='E6 School Painting'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer06@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E6 School Painting' ORDER BY s1.starts_at LIMIT 1),
   'OK with paint','applied'),

  ((SELECT id FROM events WHERE title='E7 Library Sorting'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer07@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E7 Library Sorting' ORDER BY s1.starts_at LIMIT 1),
   'Library fan','applied'),

  ((SELECT id FROM events WHERE title='E8 Beach Clean-up'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer08@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E8 Beach Clean-up' ORDER BY s1.starts_at LIMIT 1),
   'Can Gio volunteer','applied'),

  ((SELECT id FROM events WHERE title='E9 Traffic Safety'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer09@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E9 Traffic Safety' ORDER BY s1.starts_at LIMIT 1),
   'Available morning','applied'),

  ((SELECT id FROM events WHERE title='E10 Blood Donation'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer10@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E10 Blood Donation' ORDER BY s1.starts_at LIMIT 1),
   'Admin tasks OK','applied'),

  -- thêm vài volunteer ở slot 2
  ((SELECT id FROM events WHERE title='E1 Community Clean-up'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer11@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E1 Community Clean-up' ORDER BY s1.starts_at OFFSET 1 LIMIT 1),
   'Afternoon slot','applied'),

  ((SELECT id FROM events WHERE title='E3 Food Drive'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer12@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E3 Food Drive' ORDER BY s1.starts_at OFFSET 1 LIMIT 1),
   'PM works','applied'),

  ((SELECT id FROM events WHERE title='E5 Elderly Support'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer13@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E5 Elderly Support' ORDER BY s1.starts_at OFFSET 1 LIMIT 1),
   'Care tasks ok','applied'),

  ((SELECT id FROM events WHERE title='E7 Library Sorting'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer14@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E7 Library Sorting' ORDER BY s1.starts_at OFFSET 1 LIMIT 1),
   'Shelving books','applied'),

  ((SELECT id FROM events WHERE title='E9 Traffic Safety'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer15@example.com'),
   (SELECT s1.id FROM event_slots s1 JOIN events e ON e.id=s1.event_id
     WHERE e.title='E9 Traffic Safety' ORDER BY s1.starts_at OFFSET 1 LIMIT 1),
   'Flag warden','applied');

-- =========================
-- 6) DUYỆT & ĐIỂM DANH (kích hoạt trigger cộng ngày công)
-- =========================
UPDATE applications SET status='approved', decided_by=(
    SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org01@example.com'
  ), decided_at=now(), updated_at=now()
WHERE (event_id, student_user_id) IN (
  ( (SELECT id FROM events WHERE title='E1 Community Clean-up'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer01@example.com') ),
  ( (SELECT id FROM events WHERE title='E3 Food Drive'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer03@example.com') ),
  ( (SELECT id FROM events WHERE title='E5 Elderly Support'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer05@example.com') ),
  ( (SELECT id FROM events WHERE title='E7 Library Sorting'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer07@example.com') ),
  ( (SELECT id FROM events WHERE title='E9 Traffic Safety'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer09@example.com') )
);

-- Check-in thành 'attended' (trigger sẽ cộng social_work_days + ghi ledger)
UPDATE applications SET status='attended', updated_at=now()
WHERE (event_id, student_user_id) IN (
  ( (SELECT id FROM events WHERE title='E1 Community Clean-up'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer01@example.com') ),
  ( (SELECT id FROM events WHERE title='E5 Elderly Support'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer05@example.com') ),
  ( (SELECT id FROM events WHERE title='E9 Traffic Safety'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer09@example.com') )
);

-- Từ chối một hồ sơ (ví dụ)
UPDATE applications SET status='rejected', decided_by=(
    SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org02@example.com'
  ), decided_at=now(), reason='Over capacity', updated_at=now()
WHERE (event_id, student_user_id) IN (
  ( (SELECT id FROM events WHERE title='E3 Food Drive'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer12@example.com') )
);

-- =========================
-- 7) BOOKMARKS (saved)
-- =========================
INSERT INTO student_saved_events (student_user_id, event_id)
VALUES
  ((SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer02@example.com'),
   (SELECT id FROM events WHERE title='E1 Community Clean-up')),
  ((SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer04@example.com'),
   (SELECT id FROM events WHERE title='E6 School Painting')),
  ((SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer06@example.com'),
   (SELECT id FROM events WHERE title='E8 Beach Clean-up'));

-- =========================
-- 8) RATINGS (chỉ cho những cái attended)
-- =========================
INSERT INTO ratings (event_id, student_user_id, stars, comment)
VALUES
  ( (SELECT id FROM events WHERE title='E1 Community Clean-up'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer01@example.com'),
    5, 'Great impact!' ),
  ( (SELECT id FROM events WHERE title='E9 Traffic Safety'),
    (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer09@example.com'),
    4, 'Well organized.' );

-- =========================
-- 9) NOTIFICATIONS (ví dụ)
-- =========================
INSERT INTO notifications (type, payload, is_read, sender_user_id, receiver_user_id, event_id)
VALUES
  ('APPLICATION_APPROVED',
   jsonb_build_object('event','E1 Community Clean-up'),
   FALSE,
   (SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org01@example.com'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer01@example.com'),
   (SELECT id FROM events WHERE title='E1 Community Clean-up')
  ),
  ('APPLICATION_REJECTED',
   jsonb_build_object('event','E3 Food Drive','reason','Over capacity'),
   FALSE,
   (SELECT o.user_id FROM organizers o JOIN users u ON u.id=o.user_id WHERE u.email='org02@example.com'),
   (SELECT s.user_id FROM students s JOIN users u ON u.id=s.user_id WHERE u.email='volunteer12@example.com'),
   (SELECT id FROM events WHERE title='E3 Food Drive')
  );

COMMIT;