BEGIN;

-- 1. Bật Extension để hash password
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 2. Làm sạch dữ liệu cũ theo thứ tự để tránh lỗi khóa ngoại
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
-- 3. TẠO USERS
-- Password mặc định cho tất cả là: 123456
-- =========================
INSERT INTO users (email, password_hash, full_name, phone, type)
VALUES
  -- 15 Volunteers (STUDENT)
  ('volunteer01@example.com', crypt('123456', gen_salt('bf')), 'Nguyen Van Vol 01', '+840100000001', 'STUDENT'),
  ('volunteer02@example.com', crypt('123456', gen_salt('bf')), 'Tran Thi Vol 02', '+840100000002', 'STUDENT'),
  ('volunteer03@example.com', crypt('123456', gen_salt('bf')), 'Le Van Vol 03', '+840100000003', 'STUDENT'),
  ('volunteer04@example.com', crypt('123456', gen_salt('bf')), 'Pham Thi Vol 04', '+840100000004', 'STUDENT'),
  ('volunteer05@example.com', crypt('123456', gen_salt('bf')), 'Hoang Van Vol 05', '+840100000005', 'STUDENT'),
  ('volunteer06@example.com', crypt('123456', gen_salt('bf')), 'Doan Thi Vol 06', '+840100000006', 'STUDENT'),
  ('volunteer07@example.com', crypt('123456', gen_salt('bf')), 'Vo Van Vol 07', '+840100000007', 'STUDENT'),
  ('volunteer08@example.com', crypt('123456', gen_salt('bf')), 'Bui Thi Vol 08', '+840100000008', 'STUDENT'),
  ('volunteer09@example.com', crypt('123456', gen_salt('bf')), 'Dang Van Vol 09', '+840100000009', 'STUDENT'),
  ('volunteer10@example.com', crypt('123456', gen_salt('bf')), 'Truong Thi Vol 10', '+840100000010', 'STUDENT'),
  ('volunteer11@example.com', crypt('123456', gen_salt('bf')), 'Ngo Van Vol 11', '+840100000011', 'STUDENT'),
  ('volunteer12@example.com', crypt('123456', gen_salt('bf')), 'Duong Thi Vol 12', '+840100000012', 'STUDENT'),
  ('volunteer13@example.com', crypt('123456', gen_salt('bf')), 'Ly Van Vol 13', '+840100000013', 'STUDENT'),
  ('volunteer14@example.com', crypt('123456', gen_salt('bf')), 'Ha Thi Vol 14', '+840100000014', 'STUDENT'),
  ('volunteer15@example.com', crypt('123456', gen_salt('bf')), 'Phan Van Vol 15', '+840100000015', 'STUDENT'),

  -- 15 Organizers (ORGANIZER)
  ('org01@example.com', crypt('123456', gen_salt('bf')), 'Doan Truong CNTT', '+840200000001', 'ORGANIZER'),
  ('org02@example.com', crypt('123456', gen_salt('bf')), 'CLB Moi Truong', '+840200000002', 'ORGANIZER'),
  ('org03@example.com', crypt('123456', gen_salt('bf')), 'Hoi Chu Thap Do', '+840200000003', 'ORGANIZER'),
  ('org04@example.com', crypt('123456', gen_salt('bf')), 'CLB Sach & Hanh Dong', '+840200000004', 'ORGANIZER'),
  ('org05@example.com', crypt('123456', gen_salt('bf')), 'Doi Cong Tac Xa Hoi', '+840200000005', 'ORGANIZER'),
  ('org06@example.com', crypt('123456', gen_salt('bf')), 'Organizer 06', '+840200000006', 'ORGANIZER'),
  ('org07@example.com', crypt('123456', gen_salt('bf')), 'Organizer 07', '+840200000007', 'ORGANIZER'),
  ('org08@example.com', crypt('123456', gen_salt('bf')), 'Organizer 08', '+840200000008', 'ORGANIZER'),
  ('org09@example.com', crypt('123456', gen_salt('bf')), 'Organizer 09', '+840200000009', 'ORGANIZER'),
  ('org10@example.com', crypt('123456', gen_salt('bf')), 'Organizer 10', '+840200000010', 'ORGANIZER'),
  ('org11@example.com', crypt('123456', gen_salt('bf')), 'Organizer 11', '+840200000011', 'ORGANIZER'),
  ('org12@example.com', crypt('123456', gen_salt('bf')), 'Organizer 12', '+840200000012', 'ORGANIZER'),
  ('org13@example.com', crypt('123456', gen_salt('bf')), 'Organizer 13', '+840200000013', 'ORGANIZER'),
  ('org14@example.com', crypt('123456', gen_salt('bf')), 'Organizer 14', '+840200000014', 'ORGANIZER'),
  ('org15@example.com', crypt('123456', gen_salt('bf')), 'Organizer 15', '+840200000015', 'ORGANIZER');

-- =========================
-- 4. ROLE TABLES (Students & Organizers)
-- =========================
-- Tạo Profile Students
INSERT INTO students (user_id, student_no, social_work_days)
SELECT id,
       'SV' || LPAD((ROW_NUMBER() OVER (ORDER BY email))::text, 5, '0'),
       0 -- Mặc định 0 ngày công
FROM users
WHERE type = 'STUDENT';

-- Tạo Profile Organizers
INSERT INTO organizers (user_id, organizer_no, org_name)
SELECT id,
       'ORG' || LPAD((ROW_NUMBER() OVER (ORDER BY email))::text, 3, '0'),
       full_name -- Lấy luôn tên từ users làm tên tổ chức cho tiện
FROM users
WHERE type = 'ORGANIZER';

-- Tạo Consents (Quyền riêng tư)
INSERT INTO consents (user_id, email_marketing, data_sharing)
SELECT id, TRUE, TRUE FROM users;

-- =========================
-- 5. EVENTS (10 events mẫu)
-- =========================
INSERT INTO events (organizer_user_id, title, description, location, status)
VALUES
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG001'), 'Mua He Xanh 2024', 'Chien dich tinh nguyen mua he', 'TP.HCM', 'published'),
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG001'), 'Tiep Suc Mua Thi', 'Ho tro thi sinh thi dai hoc', 'Quan 1', 'published'),
  
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG002'), 'Nhat rac cong vien', 'Lam sach moi truong', 'Cong vien Gia Dinh', 'published'),
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG002'), 'Trong cay xanh', 'Phu xanh do thi', 'Thu Duc', 'published'),
  
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG003'), 'Hien mau nhan dao', 'Moi giot mau cho di', 'Sanh A truong', 'published'),
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG003'), 'Tham mai am', 'Tham va tang qua nguoi gia', 'Go Vap', 'published'),
  
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG004'), 'Quyen gop sach', 'Tang sach cho tre em vung cao', 'Thu vien', 'published'),
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG004'), 'Day hoc tinh thuong', 'Day chu cho tre em', 'Binh Thanh', 'published'),
  
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG005'), 'Doi dieu phoi giao thong', 'Ho tro gio cao diem', 'Cong truong', 'published'),
  ((SELECT user_id FROM organizers WHERE organizer_no='ORG005'), 'Tap huan ky nang', 'Ky nang so cap cuu', 'Hoi truong B', 'published');

-- =========================
-- 6. EVENT SLOTS (Sửa lại cho khớp Schema mới: Date + Time riêng)
-- =========================
-- Mỗi event tạo 2 slot: Sáng (8h-11h) và Chiều (13h-16h) vào ngày mai
INSERT INTO event_slots (event_id, work_date, starts_at, ends_at, capacity, day_reward)
SELECT 
    id, 
    CURRENT_DATE + 1, -- Ngày mai
    '08:00:00', 
    '11:00:00', 
    20, 
    0.5 -- 0.5 ngày công
FROM events;

INSERT INTO event_slots (event_id, work_date, starts_at, ends_at, capacity, day_reward)
SELECT 
    id, 
    CURRENT_DATE + 1, 
    '13:00:00', 
    '16:00:00', 
    20, 
    0.5
FROM events;

-- =========================
-- 7. APPLICATIONS (Đăng ký)
-- =========================
-- Volunteer 1 -> 5 đăng ký Event 'Mua He Xanh 2024' (Slot sáng)
INSERT INTO applications (event_id, student_user_id, slot_id, note, status)
SELECT 
    e.id, 
    s.user_id, 
    (SELECT id FROM event_slots WHERE event_id = e.id AND starts_at = '08:00:00' LIMIT 1),
    'Dang ky tham gia',
    'applied'
FROM events e
JOIN students s ON s.student_no IN ('SV00001', 'SV00002', 'SV00003', 'SV00004', 'SV00005')
WHERE e.title = 'Mua He Xanh 2024';

-- Volunteer 6 -> 10 đăng ký Event 'Hien mau nhan dao' (Slot chiều)
INSERT INTO applications (event_id, student_user_id, slot_id, note, status)
SELECT 
    e.id, 
    s.user_id, 
    (SELECT id FROM event_slots WHERE event_id = e.id AND starts_at = '13:00:00' LIMIT 1),
    'Em muon hien mau',
    'applied'
FROM events e
JOIN students s ON s.student_no IN ('SV00006', 'SV00007', 'SV00008', 'SV00009', 'SV00010')
WHERE e.title = 'Hien mau nhan dao';

-- =========================
-- 8. WORKFLOW: DUYỆT & HOÀN THÀNH (Để test Trigger cộng điểm)
-- =========================

-- Duyệt (Approved) cho SV01, SV02 tại Mùa Hè Xanh
UPDATE applications 
SET status = 'approved', 
    decided_by = (SELECT user_id FROM organizers WHERE organizer_no='ORG001'),
    decided_at = NOW()
WHERE event_id = (SELECT id FROM events WHERE title = 'Mua He Xanh 2024')
  AND student_user_id IN (SELECT user_id FROM students WHERE student_no IN ('SV00001', 'SV00002'));

-- Hoàn thành (Attended) cho SV01 -> Kích hoạt Trigger cộng 0.5 điểm
UPDATE applications 
SET status = 'attended', 
    updated_at = NOW()
WHERE event_id = (SELECT id FROM events WHERE title = 'Mua He Xanh 2024')
  AND student_user_id = (SELECT user_id FROM students WHERE student_no = 'SV00001');

-- Từ chối (Rejected) SV05
UPDATE applications 
SET status = 'rejected', 
    reason = 'Da du so luong',
    decided_by = (SELECT user_id FROM organizers WHERE organizer_no='ORG001')
WHERE event_id = (SELECT id FROM events WHERE title = 'Mua He Xanh 2024')
  AND student_user_id = (SELECT user_id FROM students WHERE student_no = 'SV00005');

-- =========================
-- 9. DỮ LIỆU PHỤ (Bookmark, Rating, Notification)
-- =========================

-- Bookmark
INSERT INTO student_saved_events (student_user_id, event_id)
VALUES (
    (SELECT user_id FROM students WHERE student_no='SV00002'),
    (SELECT id FROM events WHERE title='Hien mau nhan dao')
);

-- Rating (Chỉ SV00001 đã attended mới rate được theo logic app, nhưng db vẫn cho phép insert)
INSERT INTO ratings (event_id, student_user_id, stars, comment)
VALUES (
    (SELECT id FROM events WHERE title='Mua He Xanh 2024'),
    (SELECT user_id FROM students WHERE student_no='SV00001'),
    5,
    'Chuong trinh rat y nghia!'
);

-- Notification
INSERT INTO notifications (type, payload, is_read, sender_user_id, receiver_user_id, event_id)
VALUES (
    'APPLICATION_APPROVED',
    '{"message": "Chuc mung ban da duoc duyet"}',
    FALSE,
    (SELECT user_id FROM organizers WHERE organizer_no='ORG001'),
    (SELECT user_id FROM students WHERE student_no='SV00001'),
    (SELECT id FROM events WHERE title='Mua He Xanh 2024')
);

COMMIT;